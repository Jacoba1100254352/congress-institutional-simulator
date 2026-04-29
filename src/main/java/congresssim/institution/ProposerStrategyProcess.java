package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class ProposerStrategyProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final Map<String, ProposerState> stateByProposer = new HashMap<>();
    private final double adaptationStrength;
    private final double withdrawalThreshold;
    private final double cosponsorshipThreshold;

    public ProposerStrategyProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            double adaptationStrength,
            double withdrawalThreshold,
            double cosponsorshipThreshold
    ) {
        Values.requireRange("adaptationStrength", adaptationStrength, 0.0, 1.0);
        Values.requireRange("withdrawalThreshold", withdrawalThreshold, 0.0, 1.0);
        Values.requireRange("cosponsorshipThreshold", cosponsorshipThreshold, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.adaptationStrength = adaptationStrength;
        this.withdrawalThreshold = withdrawalThreshold;
        this.cosponsorshipThreshold = cosponsorshipThreshold;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        ProposerState state = stateByProposer.computeIfAbsent(bill.proposerId(), ignored -> new ProposerState());
        double risk = proposalRisk(bill, context);
        state.opportunities++;

        if (state.cooldown > 0 && risk >= state.riskTolerance && bill.publicBenefit() < 0.68) {
            state.cooldown--;
            state.proposalPace = Values.clamp(state.proposalPace + 0.02, 0.15, 1.35);
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "strategic proposer timing delay");
        }

        if (shouldSuppressVolume(bill, state, risk)) {
            state.delays++;
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "strategic proposer volume delay");
        }

        if (shouldWithdrawRiskyBill(bill, state, risk)) {
            state.withdrawals++;
            state.trust = Values.clamp(state.trust + 0.03, 0.0, 1.0);
            state.proposalPace = Values.clamp(state.proposalPace - 0.04, 0.15, 1.35);
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "strategic proposer withdrawal");
        }

        Bill revisedBill = adaptBill(bill, context, state, risk);
        BillOutcome outcome = innerProcess.consider(revisedBill, context);
        updateState(revisedBill, outcome, state, risk);
        return outcome;
    }

    private boolean shouldSuppressVolume(Bill bill, ProposerState state, double risk) {
        if (state.proposalPace >= 0.98 || bill.publicBenefit() >= 0.72 || bill.publicSupport() >= 0.64) {
            return false;
        }
        if (risk < state.riskTolerance) {
            return false;
        }
        double deterministicDraw = Math.floorMod((bill.id() + ":" + state.opportunities).hashCode(), 100) / 100.0;
        return deterministicDraw > state.proposalPace;
    }

    private boolean shouldWithdrawRiskyBill(Bill bill, ProposerState state, double risk) {
        if (risk < withdrawalThreshold || bill.publicBenefit() >= 0.68) {
            return false;
        }
        if (state.trust < 0.30) {
            return true;
        }
        return risk >= state.riskTolerance + 0.22
                && state.proposalPace < 0.56
                && bill.publicSupport() < 0.38;
    }

    private Bill adaptBill(Bill bill, VoteContext context, ProposerState state, double risk) {
        double moderationRate = Values.clamp(
                adaptationStrength * risk * (1.10 - state.trust) * (0.55 + state.concessionRate),
                0.0,
                0.82
        );
        double median = chamberMedian();
        double target = (0.55 * median) + (0.35 * context.currentPolicyPosition()) + (0.10 * bill.proposerIdeology());
        double revisedIdeology = Values.clamp(
                bill.ideologyPosition() + moderationRate * (target - bill.ideologyPosition()),
                -1.0,
                1.0
        );
        double moderationGain = Math.abs(bill.ideologyPosition()) - Math.abs(revisedIdeology);
        double revisedSupport = Values.clamp(
                bill.publicSupport()
                        + (Math.max(0.0, moderationGain) * 0.18)
                        + (moderationRate * bill.compensationCost() * 0.10),
                0.0,
                1.0
        );
        double revisedBenefit = Values.clamp(
                bill.publicBenefit() - (moderationRate * Math.max(0.0, bill.privateGain() - bill.publicBenefit()) * 0.08),
                0.0,
                1.0
        );
        Bill revisedBill = Math.abs(revisedIdeology - bill.ideologyPosition()) > 0.000001
                ? bill.withAmendment(revisedIdeology, revisedSupport, revisedBenefit)
                : bill;

        revisedBill = adaptLobbyExposure(revisedBill, state, risk);
        revisedBill = adaptAmendmentPosture(revisedBill, state, risk);

        if (risk >= cosponsorshipThreshold) {
            int outsideSponsors = outsideSponsorEstimate(revisedBill);
            if (outsideSponsors > 0) {
                revisedBill = revisedBill.withCosponsorship(
                        revisedBill.cosponsorCount() + outsideSponsors + 1,
                        revisedBill.outsideBlocCosponsorCount() + outsideSponsors,
                        revisedBill.affectedGroupSponsor() || revisedBill.affectedGroupSupport() >= 0.45
                );
            }
        }
        return revisedBill;
    }

    private Bill adaptLobbyExposure(Bill bill, ProposerState state, double risk) {
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double exposureCut = Values.clamp((1.0 - state.lobbyExposure) * (0.50 * risk + 0.50 * captureRisk), 0.0, 0.70);
        if (exposureCut <= 0.000001) {
            return bill;
        }
        double revisedLobbyPressure = bill.lobbyPressure() * (1.0 - (0.52 * exposureCut));
        double revisedPrivateGain = bill.privateGain() * (1.0 - (0.26 * exposureCut));
        double revisedPublicSupport = Values.clamp(bill.publicSupport() + (0.05 * exposureCut), 0.0, 1.0);
        double revisedPublicBenefit = Values.clamp(bill.publicBenefit() + (0.035 * exposureCut), 0.0, 1.0);
        return bill.withLobbyActivity(
                Values.clamp(revisedLobbyPressure, -1.0, 1.0),
                revisedPublicSupport,
                revisedPublicBenefit,
                Values.clamp(revisedPrivateGain, 0.0, 1.0),
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0
        );
    }

    private Bill adaptAmendmentPosture(Bill bill, ProposerState state, double risk) {
        if (bill.concentratedHarm() < 0.42 || bill.affectedGroupSupport() >= 0.52) {
            return bill;
        }
        double compensationWillingness = Values.clamp(
                state.concessionRate * risk * (0.70 + bill.compensationCost()),
                0.0,
                1.0
        );
        if (compensationWillingness < 0.28) {
            return bill;
        }
        double harmReduction = 0.22 + (0.38 * compensationWillingness);
        double revisedBenefit = Values.clamp(
                bill.publicBenefit() - (bill.compensationCost() * 0.10 * compensationWillingness),
                0.0,
                1.0
        );
        double revisedAffectedSupport = Values.clamp(
                bill.affectedGroupSupport() + (0.24 * compensationWillingness),
                0.0,
                1.0
        );
        double revisedHarm = Values.clamp(
                bill.concentratedHarm() * (1.0 - harmReduction),
                0.0,
                1.0
        );
        return bill.withCompensation(revisedBenefit, revisedAffectedSupport, revisedHarm);
    }

    private int outsideSponsorEstimate(Bill bill) {
        String proposerParty = proposerParty(bill.proposerId());
        int sponsors = 0;
        for (Legislator legislator : legislators) {
            if (legislator.id().equals(bill.proposerId()) || legislator.party().equals(proposerParty)) {
                continue;
            }
            double policyFit = 1.0 - Math.abs(legislator.ideology() - bill.ideologyPosition()) / 2.0;
            double sponsorScore = (0.42 * policyFit)
                    + (0.28 * bill.publicSupport())
                    + (0.18 * legislator.compromisePreference())
                    + (0.12 * (1.0 - Math.max(0.0, bill.lobbyPressure())));
            if (sponsorScore >= 0.58) {
                sponsors++;
            }
        }
        return Math.min(4, sponsors);
    }

    private String proposerParty(String proposerId) {
        for (Legislator legislator : legislators) {
            if (legislator.id().equals(proposerId)) {
                return legislator.party();
            }
        }
        return "";
    }

    private double chamberMedian() {
        if (legislators.isEmpty()) {
            return 0.0;
        }
        List<Double> ideologies = legislators.stream().map(Legislator::ideology).sorted().toList();
        int middle = ideologies.size() / 2;
        if (ideologies.size() % 2 == 1) {
            return ideologies.get(middle);
        }
        return (ideologies.get(middle - 1) + ideologies.get(middle)) / 2.0;
    }

    private static double proposalRisk(Bill bill, VoteContext context) {
        return Values.clamp(
                (0.22 * (1.0 - bill.publicSupport()))
                        + (0.22 * Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0)
                        + (0.18 * Math.max(0.0, bill.lobbyPressure()))
                        + (0.15 * bill.privateGain())
                        + (0.13 * bill.concentratedHarm())
                        + (0.10 * bill.publicBenefitUncertainty()),
                0.0,
                1.0
        );
    }

    private void updateState(Bill bill, BillOutcome outcome, ProposerState state, double risk) {
        double quality = (0.42 * bill.publicBenefit())
                + (0.28 * bill.publicSupport())
                + (0.18 * (1.0 - LobbyCaptureScoring.captureRisk(bill)))
                + (0.12 * bill.affectedGroupSupport());
        double enactedBonus = outcome.enacted() ? 0.08 : -0.05;
        double lowSupportPenalty = outcome.enacted() && bill.publicSupport() < 0.45 ? 0.12 : 0.0;
        double updated = state.trust + (0.18 * (quality - 0.50)) + enactedBonus - lowSupportPenalty;
        state.trust = Values.clamp(updated, 0.0, 1.0);

        boolean badOutcome = !outcome.enacted()
                || quality < 0.42
                || (outcome.enacted() && bill.publicSupport() < 0.45)
                || LobbyCaptureScoring.captureRisk(bill) > 0.62;
        if (badOutcome) {
            state.badStreak++;
            state.goodStreak = 0;
            state.proposalPace = Values.clamp(state.proposalPace - (0.07 + (0.05 * risk)), 0.15, 1.35);
            state.riskTolerance = Values.clamp(state.riskTolerance - 0.035, 0.22, 0.82);
            state.concessionRate = Values.clamp(state.concessionRate + 0.06, 0.18, 0.94);
            state.lobbyExposure = Values.clamp(state.lobbyExposure - 0.08, 0.12, 0.96);
            if (state.badStreak >= 2 && risk >= state.riskTolerance) {
                state.cooldown = Math.min(3, state.cooldown + 1);
            }
        } else {
            state.goodStreak++;
            state.badStreak = 0;
            state.proposalPace = Values.clamp(state.proposalPace + 0.05, 0.15, 1.35);
            state.riskTolerance = Values.clamp(state.riskTolerance + (bill.publicBenefit() >= 0.68 ? 0.025 : 0.010), 0.22, 0.82);
            state.concessionRate = Values.clamp(state.concessionRate - 0.025, 0.18, 0.94);
            state.lobbyExposure = Values.clamp(state.lobbyExposure + (bill.publicBenefit() >= bill.privateGain() ? 0.02 : -0.01), 0.12, 0.96);
            state.cooldown = Math.max(0, state.cooldown - 1);
        }
    }

    private static final class ProposerState {
        private double trust = 0.55;
        private double proposalPace = 1.0;
        private double riskTolerance = 0.55;
        private double concessionRate = 0.50;
        private double lobbyExposure = 0.72;
        private int cooldown;
        private int opportunities;
        private int delays;
        private int withdrawals;
        private int badStreak;
        private int goodStreak;
    }
}
