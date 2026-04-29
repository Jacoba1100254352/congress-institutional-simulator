package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.Map;

public final class ProposalCreditProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final Map<String, Double> creditsByProposer = new HashMap<>();
    private final double initialCredits;
    private final double creditDrip;
    private final double creditCap;
    private final double baseCost;
    private final double riskCostWeight;
    private final double publicValueDiscount;
    private final double rewardScale;
    private final double penaltyScale;

    public ProposalCreditProcess(
            String name,
            LegislativeProcess innerProcess,
            double initialCredits,
            double creditDrip,
            double creditCap,
            double baseCost,
            double riskCostWeight,
            double publicValueDiscount,
            double rewardScale,
            double penaltyScale
    ) {
        Values.requireRange("initialCredits", initialCredits, 0.0, 10.0);
        Values.requireRange("creditDrip", creditDrip, 0.0, 10.0);
        Values.requireRange("creditCap", creditCap, 0.0, 10.0);
        Values.requireRange("baseCost", baseCost, 0.0, 10.0);
        Values.requireRange("riskCostWeight", riskCostWeight, 0.0, 10.0);
        Values.requireRange("publicValueDiscount", publicValueDiscount, 0.0, 10.0);
        Values.requireRange("rewardScale", rewardScale, 0.0, 10.0);
        Values.requireRange("penaltyScale", penaltyScale, 0.0, 10.0);
        if (creditCap < initialCredits) {
            throw new IllegalArgumentException("creditCap must be at least initialCredits.");
        }
        this.name = name;
        this.innerProcess = innerProcess;
        this.initialCredits = initialCredits;
        this.creditDrip = creditDrip;
        this.creditCap = creditCap;
        this.baseCost = baseCost;
        this.riskCostWeight = riskCostWeight;
        this.publicValueDiscount = publicValueDiscount;
        this.rewardScale = rewardScale;
        this.penaltyScale = penaltyScale;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double credits = availableCreditsAfterDrip(bill.proposerId());
        double risk = AdaptiveTrackProcess.riskScore(bill, context);
        double cost = proposalCost(bill, risk);
        if (credits < cost) {
            creditsByProposer.put(bill.proposerId(), credits);
            return BillOutcome.accessDenied(
                    bill,
                    context.currentPolicyPosition(),
                    "proposal credits insufficient"
            );
        }

        creditsByProposer.put(bill.proposerId(), credits - cost);
        BillOutcome outcome = innerProcess.consider(bill, context);
        updateCreditsAfterOutcome(bill, outcome, risk);
        return outcome;
    }

    private double creditsFor(String proposerId) {
        return creditsByProposer.getOrDefault(proposerId, initialCredits);
    }

    private double availableCreditsAfterDrip(String proposerId) {
        double updated = creditsFor(proposerId) + creditDrip;
        return Values.clamp(updated, 0.0, creditCap);
    }

    private double proposalCost(Bill bill, double risk) {
        double lobbyRisk = Math.max(0.0, bill.lobbyPressure());
        double publicValue = publicValue(bill);
        double rawCost = baseCost
                + (riskCostWeight * risk)
                + (0.18 * lobbyRisk)
                + (0.12 * bill.salience())
                - (publicValueDiscount * publicValue);
        return Values.clamp(rawCost, 0.15, creditCap);
    }

    private void updateCreditsAfterOutcome(Bill bill, BillOutcome outcome, double risk) {
        double quality = qualityScore(bill, risk);
        double adjustment = (quality - 0.50) * rewardScale;

        if (outcome.enacted()) {
            adjustment += 0.25 * rewardScale;
            if (outcome.averageYayShare() < 0.50) {
                adjustment -= 0.35 * penaltyScale;
            }
        } else {
            adjustment -= 0.18 * penaltyScale;
            if (bill.publicSupport() >= 0.60 && bill.publicBenefit() >= 0.55) {
                adjustment += 0.20 * rewardScale;
            }
        }

        if (bill.publicSupport() < 0.40) {
            adjustment -= ((0.40 - bill.publicSupport()) / 0.40) * 0.25 * penaltyScale;
        }
        if (bill.publicBenefit() < 0.35) {
            adjustment -= ((0.35 - bill.publicBenefit()) / 0.35) * 0.25 * penaltyScale;
        }
        adjustment -= Math.max(0.0, bill.lobbyPressure()) * 0.10 * penaltyScale;

        double current = creditsFor(bill.proposerId());
        creditsByProposer.put(bill.proposerId(), Values.clamp(current + adjustment, 0.0, creditCap));
    }

    private static double qualityScore(Bill bill, double risk) {
        double lobbyPenalty = Math.max(0.0, bill.lobbyPressure());
        return Values.clamp(
                (0.44 * bill.publicBenefit())
                        + (0.30 * bill.publicSupport())
                        + (0.18 * (1.0 - risk))
                        + (0.08 * (1.0 - lobbyPenalty)),
                0.0,
                1.0
        );
    }

    private static double publicValue(Bill bill) {
        return Values.clamp(
                (0.58 * bill.publicBenefit())
                        + (0.32 * bill.publicSupport())
                        + (0.10 * (1.0 - Math.abs(bill.lobbyPressure()))),
                0.0,
                1.0
        );
    }
}
