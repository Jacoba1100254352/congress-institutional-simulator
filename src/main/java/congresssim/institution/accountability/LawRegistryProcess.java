package congresssim.institution.accountability;

import congresssim.institution.agenda.AdaptiveTrackProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public final class LawRegistryProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final int reviewDelayRounds;
    private final double provisionalRiskThreshold;
    private final double renewalThreshold;
    private final double rollbackRate;
    private final List<LawRecord> laws = new ArrayList<>();
    private int round;

    public LawRegistryProcess(
            String name,
            LegislativeProcess innerProcess,
            int reviewDelayRounds,
            double provisionalRiskThreshold,
            double renewalThreshold,
            double rollbackRate
    ) {
        if (reviewDelayRounds < 1) {
            throw new IllegalArgumentException("reviewDelayRounds must be positive.");
        }
        Values.requireRange("provisionalRiskThreshold", provisionalRiskThreshold, 0.0, 1.0);
        Values.requireRange("renewalThreshold", renewalThreshold, 0.0, 1.0);
        Values.requireRange("rollbackRate", rollbackRate, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.reviewDelayRounds = reviewDelayRounds;
        this.provisionalRiskThreshold = provisionalRiskThreshold;
        this.renewalThreshold = renewalThreshold;
        this.rollbackRate = rollbackRate;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        round++;
        BillOutcome outcome = innerProcess.consider(bill, context);
        if (outcome.enacted() && AdaptiveTrackProcess.riskScore(outcome.bill(), context) >= provisionalRiskThreshold) {
            ImplementationState implementation = implementationState(outcome.bill(), context);
            laws.add(new LawRecord(
                    outcome.bill(),
                    outcome.statusQuoBefore(),
                    outcome.statusQuoAfter(),
                    round,
                    round + implementation.delayRounds(),
                    round + reviewDelayRounds,
                    implementation.capacity(),
                    implementation.underfunded(),
                    implementation.nonenforced(),
                    implementation.stayed(),
                    implementation.renewalLobbyPressure(),
                    true
            ));
            outcome = outcome.withSignals(OutcomeSignals.diagnostics(Map.of(
                    "implementationDelay",
                    (double) implementation.delayRounds(),
                    "implementationCapacity",
                    implementation.capacity(),
                    "implementationFailureRisk",
                    implementation.failureRisk(),
                    "nonEnforcementRisk",
                    implementation.nonenforced() ? 1.0 : 0.0,
                    "underfundingRisk",
                    implementation.underfunded() ? 1.0 : 0.0,
                    "renewalLobbyPressure",
                    implementation.renewalLobbyPressure()
            )));
        }
        return reviewDueLaws(outcome, context);
    }

    private BillOutcome reviewDueLaws(BillOutcome outcome, VoteContext context) {
        OutcomeSignals signals = OutcomeSignals.none();
        double adjustedStatusQuo = outcome.statusQuoAfter();
        boolean changedStatusQuo = false;
        List<LawRecord> updated = new ArrayList<>(laws.size());

        for (LawRecord law : laws) {
            if (!law.active() || law.reviewDueRound() > round) {
                updated.add(law);
                continue;
            }

            if (law.effectiveRound() > round) {
                updated.add(law.withReviewDueRound(law.effectiveRound() + Math.max(1, reviewDelayRounds / 2)));
                signals = signals.plus(OutcomeSignals.diagnostics(Map.of(
                        "sunsetBeforeImplementationRate",
                        1.0,
                        "implementationDelay",
                        (double) Math.max(0, law.effectiveRound() - law.enactedRound())
                )));
                continue;
            }

            double reviewScore = reviewScore(law, context);
            boolean renewed = reviewScore >= renewalThreshold;
            boolean reversed = !renewed;
            if (reversed) {
                adjustedStatusQuo = rollback(adjustedStatusQuo, law);
                changedStatusQuo = true;
                updated.add(law.deactivate());
            } else {
                updated.add(new LawRecord(
                        law.sourceBill(),
                        law.previousStatusQuo(),
                        law.enactedPosition(),
                        law.enactedRound(),
                        law.effectiveRound(),
                        round + reviewDelayRounds,
                        law.implementationCapacity(),
                        law.underfunded(),
                        law.nonenforced(),
                        law.stayed(),
                        law.renewalLobbyPressure(),
                        true
                ));
            }
            signals = signals.plus(OutcomeSignals.lawReview(
                    reversed,
                    renewed,
                    activeLawWelfare(updated),
                    lowSupportActiveLawShare(updated),
                    round - law.enactedRound()
            )).plus(OutcomeSignals.diagnostics(Map.of(
                    "implementationCapacity",
                    law.implementationCapacity(),
                    "implementationFailureRisk",
                    implementationFailureRisk(law),
                    "nonEnforcementRisk",
                    law.nonenforced() ? 1.0 : 0.0,
                    "underfundingRisk",
                    law.underfunded() ? 1.0 : 0.0,
                    "renewalLobbyPressure",
                    law.renewalLobbyPressure()
            )));
        }

        laws.clear();
        laws.addAll(updated);
        if (!changedStatusQuo) {
            return outcome.withSignals(signals);
        }
        return new BillOutcome(
                outcome.bill(),
                outcome.statusQuoBefore(),
                Values.clamp(adjustedStatusQuo, -1.0, 1.0),
                outcome.enacted(),
                outcome.agendaDisposition(),
                outcome.gateResults(),
                outcome.chamberResults(),
                outcome.presidentialAction(),
                outcome.challenged(),
                outcome.signals().plus(signals),
                "law-registry review adjusted active law; " + outcome.finalReason()
        );
    }

    private double rollback(double currentStatusQuo, LawRecord law) {
        double enactedShift = law.enactedPosition() - law.previousStatusQuo();
        return currentStatusQuo - (rollbackRate * enactedShift);
    }

    private static double reviewScore(LawRecord law, VoteContext context) {
        Bill bill = law.sourceBill();
        double risk = AdaptiveTrackProcess.riskScore(bill, context);
        double harmPenalty = AffectedGroupScoring.minorityHarm(bill) * 0.18;
        double implementationPenalty = (0.16 * (1.0 - law.implementationCapacity()))
                + (law.underfunded() ? 0.08 : 0.0)
                + (law.nonenforced() ? 0.12 : 0.0)
                + (law.stayed() ? 0.10 : 0.0);
        double renewalPressureBias = 0.08 * law.renewalLobbyPressure();
        return Values.clamp(
                (0.42 * bill.publicBenefit())
                        + (0.30 * bill.publicSupport())
                        + (0.16 * bill.affectedGroupSupport())
                        + (0.12 * (1.0 - risk))
                        + renewalPressureBias
                        - harmPenalty
                        - implementationPenalty,
                0.0,
                1.0
        );
    }

    private ImplementationState implementationState(Bill bill, VoteContext context) {
        double gaussian = context.random().nextGaussian();
        int delayRounds = Math.max(1, (int) Math.round(
                1.0
                        + (reviewDelayRounds * (0.35 + (0.85 * bill.publicBenefitUncertainty())))
                        + (Math.max(0.0, bill.litigationThreatSpend()) * 0.08)
                        + gaussian
        ));
        double capacity = Values.clamp(
                0.58
                        + (0.18 * bill.publicBenefit())
                        + (0.14 * bill.publicSupport())
                        - (0.24 * bill.publicBenefitUncertainty())
                        - (0.12 * AffectedGroupScoring.minorityHarm(bill))
                        - (0.06 * bill.litigationThreatSpend() / 10.0)
                        + (context.random().nextGaussian() * 0.04),
                0.0,
                1.0
        );
        boolean underfunded = capacity < 0.48
                || (bill.publicBenefitUncertainty() > 0.62 && bill.publicSupport() < 0.56);
        boolean nonenforced = capacity < 0.34
                || (bill.lobbyPressure() > 0.55 && bill.publicBenefit() < 0.46);
        boolean stayed = bill.litigationThreatSpend() > 1.80
                || (AffectedGroupScoring.minorityHarm(bill) > 0.62 && bill.publicBenefitUncertainty() > 0.48);
        double renewalLobbyPressure = Values.clamp(
                (0.36 * Math.max(0.0, bill.privateGain() - bill.publicBenefit()))
                        + (0.24 * Math.max(0.0, bill.lobbyPressure()))
                        + (0.16 * bill.defensiveLobbySpend() / 10.0)
                        + (0.14 * bill.agendaLobbySpend() / 10.0)
                        + (0.10 * bill.litigationThreatSpend() / 10.0),
                0.0,
                1.0
        );
        return new ImplementationState(
                delayRounds,
                capacity,
                underfunded,
                nonenforced,
                stayed,
                renewalLobbyPressure
        );
    }

    private static double implementationFailureRisk(LawRecord law) {
        return Values.clamp(
                (0.45 * (1.0 - law.implementationCapacity()))
                        + (law.underfunded() ? 0.18 : 0.0)
                        + (law.nonenforced() ? 0.24 : 0.0)
                        + (law.stayed() ? 0.13 : 0.0),
                0.0,
                1.0
        );
    }

    private static double activeLawWelfare(List<LawRecord> records) {
        double sum = 0.0;
        int count = 0;
        for (LawRecord law : records) {
            if (!law.active()) {
                continue;
            }
            sum += law.sourceBill().publicBenefit();
            count++;
        }
        return count == 0 ? 0.0 : sum / count;
    }

    private static double lowSupportActiveLawShare(List<LawRecord> records) {
        int lowSupport = 0;
        int count = 0;
        for (LawRecord law : records) {
            if (!law.active()) {
                continue;
            }
            count++;
            if (law.sourceBill().publicSupport() < 0.50) {
                lowSupport++;
            }
        }
        return count == 0 ? 0.0 : (double) lowSupport / count;
    }

    private record ImplementationState(
            int delayRounds,
            double capacity,
            boolean underfunded,
            boolean nonenforced,
            boolean stayed,
            double renewalLobbyPressure
    ) {
        double failureRisk() {
            return Values.clamp(
                    (0.45 * (1.0 - capacity))
                            + (underfunded ? 0.18 : 0.0)
                            + (nonenforced ? 0.24 : 0.0)
                            + (stayed ? 0.13 : 0.0),
                    0.0,
                    1.0
            );
        }
    }
}
