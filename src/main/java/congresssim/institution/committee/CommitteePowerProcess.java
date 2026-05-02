package congresssim.institution.committee;

import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.ChamberVoteResult;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;

public final class CommitteePowerProcess implements LegislativeProcess {
    private final String name;
    private final Chamber committee;
    private final LegislativeProcess innerProcess;
    private final double minorityHearingThreshold;
    private final CommitteePowerConfig config;

    public CommitteePowerProcess(
            String name,
            Chamber committee,
            LegislativeProcess innerProcess,
            double dischargeThreshold,
            double reportingDeadlinePressure,
            double amendmentStrength,
            double minorityHearingThreshold
    ) {
        this(
                name,
                committee,
                innerProcess,
                minorityHearingThreshold,
                new CommitteePowerConfig(
                        CommitteeRoleMode.DISCHARGE_TARGET,
                        dischargeThreshold,
                        1.0 - reportingDeadlinePressure,
                        0.58,
                        reportingDeadlinePressure,
                        0.18,
                        0.34,
                        0.44,
                        dischargeThreshold,
                        0.52,
                        minorityHearingThreshold,
                        0.30,
                        false,
                        amendmentStrength > 0.25
                )
        );
    }

    public CommitteePowerProcess(
            String name,
            Chamber committee,
            LegislativeProcess innerProcess,
            double minorityHearingThreshold,
            CommitteePowerConfig config
    ) {
        Values.requireRange("minorityHearingThreshold", minorityHearingThreshold, 0.0, 1.0);
        this.name = name;
        this.committee = committee;
        this.innerProcess = innerProcess;
        this.minorityHearingThreshold = minorityHearingThreshold;
        this.config = config == null ? CommitteePowerConfig.standard() : config;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        boolean hearing = bill.concentratedHarm() >= minorityHearingThreshold
                && bill.affectedGroupSupport() < 0.42;
        double queueDelay = queueDelay(bill, hearing);
        ChamberVoteResult committeeResult = committee.voteOn(bill, context);
        double gateScore = gateScore(bill, committeeResult, hearing);
        boolean certified = committeeResult.passed() && gateScore >= config.gatekeepingThreshold();
        boolean publicOverride = publicOverrideScore(bill, hearing) >= config.publicOverrideThreshold();

        if (certified || shouldFastTrack(bill, gateScore) || shouldAdvisoryPass(bill, publicOverride)) {
            Bill revised = revise(bill);
            double amendmentValue = amendmentValue(bill, revised);
            return innerProcess.consider(revised, context)
                    .withGateResult(committeeResult)
                    .withSignals(committeeSignals(bill, false, hearing, queueDelay, amendmentValue, false));
        }

        if (shouldDischarge(bill, hearing, publicOverride)) {
            return innerProcess.consider(bill, context)
                    .withGateResult(committeeResult)
                    .withSignals(committeeSignals(bill, true, hearing, queueDelay, 0.0, false));
        }

        return BillOutcome.committeeRejected(
                bill,
                context.currentPolicyPosition(),
                committeeResult,
                "buried by committee power"
        ).withSignals(committeeSignals(bill, false, hearing, queueDelay, 0.0, true));
    }

    private Bill revise(Bill bill) {
        double moderationTarget = 0.0;
        double revisedPosition = Values.clamp(
                bill.ideologyPosition() + (amendmentStrength() * 0.34 * (moderationTarget - bill.ideologyPosition())),
                -1.0,
                1.0
        );
        double supportSignal = amendmentStrength() * 0.26 * (bill.publicBenefit() - bill.publicSupport());
        double revisedSupport = Values.clamp(
                bill.publicSupport() + supportSignal + (bill.concentratedHarm() * amendmentStrength() * 0.05),
                0.0,
                1.0
        );
        double revisedBenefit = Values.clamp(
                bill.publicBenefit() - (config.reviewCost() * 0.050),
                0.0,
                1.0
        );
        Bill revised = bill.withAmendment(revisedPosition, revisedSupport, revisedBenefit);
        if (bill.concentratedHarm() < 0.28) {
            return revised;
        }

        double harmReduction = Values.clamp(amendmentStrength() * 0.36, 0.0, 0.72);
        double compensationCost = bill.compensationCost() * (0.28 + (0.28 * amendmentStrength()));
        return revised.withCompensation(
                Values.clamp(revised.publicBenefit() - compensationCost, 0.0, 1.0),
                Values.clamp(bill.affectedGroupSupport() + (harmReduction * 0.42), 0.0, 1.0),
                Values.clamp(bill.concentratedHarm() * (1.0 - harmReduction), 0.0, 1.0)
        );
    }

    private boolean shouldFastTrack(Bill bill, double gateScore) {
        return config.roleMode() == CommitteeRoleMode.FAST_TRACK_CERTIFIER
                && gateScore >= config.gatekeepingThreshold() * 0.86
                && bill.publicSupport() >= config.publicReferralThreshold();
    }

    private boolean shouldAdvisoryPass(Bill bill, boolean publicOverride) {
        return switch (config.roleMode()) {
            case SCRUTINY_AUDIT, PUBLIC_ACCOUNTS, LEGAL_DRAFTING_REVIEW -> publicOverride
                    && bill.publicBenefit() >= 0.46
                    && bill.concentratedHarm() < 0.64;
            default -> false;
        };
    }

    private boolean shouldDischarge(Bill bill, boolean hearing, boolean publicOverride) {
        if (config.roleMode() == CommitteeRoleMode.VETO_PLAYER) {
            return publicOverride && bill.publicSupport() >= 0.70;
        }
        if (config.roleMode() == CommitteeRoleMode.DISCHARGE_TARGET) {
            return dischargeScore(bill, hearing) >= config.publicOverrideThreshold();
        }
        return publicOverride && config.roleMode() != CommitteeRoleMode.PUBLIC_ACCOUNTS;
    }

    private double gateScore(Bill bill, ChamberVoteResult committeeResult, boolean hearing) {
        double observedBenefit = (config.informationAccuracy() * bill.publicBenefit())
                + ((1.0 - config.informationAccuracy()) * bill.publicSupport());
        double captureDrag = config.captureSusceptibility() * Math.max(0.0, bill.lobbyPressure());
        double chairDrag = config.chairNegativeAgendaPower() * Math.max(0.0, Math.abs(bill.ideologyPosition()) - 0.36);
        double hearingCredit = hearing ? 0.05 * config.hearingTransparency() : 0.0;
        double roleCredit = switch (config.roleMode()) {
            case FAST_TRACK_CERTIFIER -> 0.05;
            case SCRUTINY_AUDIT, PUBLIC_ACCOUNTS, LEGAL_DRAFTING_REVIEW -> -0.03;
            case DISCHARGE_TARGET -> 0.02;
            case VETO_PLAYER -> -0.06;
            case PRIORITY_QUEUE -> 0.0;
        };
        return Values.clamp(
                observedBenefit
                        + (0.18 * committeeResult.yayShare())
                        + hearingCredit
                        + roleCredit
                        - captureDrag
                        - chairDrag
                        - (0.10 * config.reviewCost()),
                0.0,
                1.0
        );
    }

    private double dischargeScore(Bill bill, boolean hearing) {
        double cosponsorSignal = Math.clamp(bill.cosponsorCount() / 12.0, 0.0, 1.0);
        double publicPressure = (0.42 * bill.publicSupport())
                + (0.20 * bill.salience())
                + (0.18 * cosponsorSignal)
                + (0.12 * (1.0 - bill.publicBenefitUncertainty()))
                + (hearing ? 0.08 : 0.0);
        return Values.clamp(publicPressure + (config.queueCapacity() * 0.12), 0.0, 1.0);
    }

    private double publicOverrideScore(Bill bill, boolean hearing) {
        return Values.clamp(
                (0.50 * bill.publicSupport())
                        + (0.20 * bill.salience())
                        + (0.15 * Math.clamp(bill.cosponsorCount() / 10.0, 0.0, 1.0))
                        + (hearing ? 0.08 : 0.0)
                        + (0.07 * config.transparencyLevel()),
                0.0,
                1.0
        );
    }

    private double queueDelay(Bill bill, boolean hearing) {
        double delay = 0.10
                + (0.38 * (1.0 - config.queueCapacity()))
                + (0.16 * bill.salience())
                + (hearing ? 0.06 : 0.0)
                + (0.08 * config.reviewCost());
        return Values.clamp(delay, 0.0, 1.0);
    }

    private double amendmentStrength() {
        double roleAdjustment = switch (config.roleMode()) {
            case LEGAL_DRAFTING_REVIEW -> 0.16;
            case SCRUTINY_AUDIT, PUBLIC_ACCOUNTS -> 0.08;
            case FAST_TRACK_CERTIFIER -> -0.08;
            default -> 0.0;
        };
        return Values.clamp(
                (0.48 * config.informationAccuracy())
                        + (config.minorityAmendmentRight() ? 0.20 : 0.0)
                        + roleAdjustment,
                0.0,
                1.0
        );
    }

    private OutcomeSignals committeeSignals(
            Bill bill,
            boolean discharged,
            boolean hearing,
            double queueDelay,
            double amendmentValue,
            boolean rejected
    ) {
        double captureRisk = config.captureSusceptibility()
                * Math.max(0.0, bill.lobbyPressure())
                * (1.0 - (0.55 * config.transparencyLevel()));
        double sponsorDiversity = Math.clamp(
                bill.cosponsorCount() == 0 ? 0.0 : (double) bill.outsideBlocCosponsorCount() / bill.cosponsorCount(),
                0.0,
                1.0
        );
        double auditRole = switch (config.roleMode()) {
            case SCRUTINY_AUDIT, PUBLIC_ACCOUNTS, LEGAL_DRAFTING_REVIEW -> 1.0;
            default -> 0.0;
        };
        OutcomeSignals base = OutcomeSignals.committeePower(discharged, hearing, queueDelay, amendmentValue);
        return base.plus(OutcomeSignals.diagnostics(Map.ofEntries(
                Map.entry("committeeAgendaConcentration", Values.clamp(config.chairNegativeAgendaPower() * (1.0 - config.quorumPartyBalanceRequirement()), 0.0, 1.0)),
                Map.entry("committeeCaptureIndex", Values.clamp(captureRisk, 0.0, 1.0)),
                Map.entry("committeeExpertiseScore", Values.clamp(config.informationAccuracy(), 0.0, 1.0)),
                Map.entry("minorityCommitteeAccessRate", hearing ? 1.0 : 0.0),
                Map.entry("committeeFalsePositiveRate", rejected && bill.publicBenefit() >= 0.66 ? 1.0 : 0.0),
                Map.entry("committeeFalseNegativeRate", !rejected && bill.publicBenefit() < 0.34 && bill.publicSupport() < 0.45 ? 1.0 : 0.0),
                Map.entry("reportedBillSponsorDiversity", sponsorDiversity),
                Map.entry("oppositionAmendmentSuccessRate", config.minorityAmendmentRight() && amendmentValue > 0.02 ? 1.0 : 0.0),
                Map.entry("hearingDiversity", hearing ? Values.clamp(config.hearingTransparency() + (0.25 * config.quorumPartyBalanceRequirement()), 0.0, 1.0) : 0.0),
                Map.entry("auditFollowThroughRate", Values.clamp(auditRole * config.transparencyLevel() * config.informationAccuracy(), 0.0, 1.0)),
                Map.entry("scandalDetectionRate", Values.clamp(auditRole * captureRisk * (0.50 + (0.50 * config.informationAccuracy())), 0.0, 1.0))
        )));
    }

    private static double amendmentValue(Bill original, Bill revised) {
        double supportGain = Math.max(0.0, revised.publicSupport() - original.publicSupport());
        double harmReduction = Math.max(0.0, original.concentratedHarm() - revised.concentratedHarm());
        double benefitLoss = Math.max(0.0, original.publicBenefit() - revised.publicBenefit());
        return Values.clamp(supportGain + harmReduction - (0.50 * benefitLoss), 0.0, 1.0);
    }
}
