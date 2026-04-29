package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.Map;

public final class ProposalBondProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final Map<String, Double> balancesByProposer = new HashMap<>();
    private final double initialBalance;
    private final double sessionDrip;
    private final double balanceCap;
    private final double baseBond;
    private final double riskWeight;
    private final double lobbyWeight;
    private final double publicValueDiscount;

    public ProposalBondProcess(
            String name,
            LegislativeProcess innerProcess,
            double initialBalance,
            double sessionDrip,
            double balanceCap,
            double baseBond,
            double riskWeight,
            double lobbyWeight,
            double publicValueDiscount
    ) {
        Values.requireRange("initialBalance", initialBalance, 0.0, 10.0);
        Values.requireRange("sessionDrip", sessionDrip, 0.0, 10.0);
        Values.requireRange("balanceCap", balanceCap, 0.0, 10.0);
        Values.requireRange("baseBond", baseBond, 0.0, 10.0);
        Values.requireRange("riskWeight", riskWeight, 0.0, 10.0);
        Values.requireRange("lobbyWeight", lobbyWeight, 0.0, 10.0);
        Values.requireRange("publicValueDiscount", publicValueDiscount, 0.0, 10.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.initialBalance = initialBalance;
        this.sessionDrip = sessionDrip;
        this.balanceCap = balanceCap;
        this.baseBond = baseBond;
        this.riskWeight = riskWeight;
        this.lobbyWeight = lobbyWeight;
        this.publicValueDiscount = publicValueDiscount;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double balance = balanceFor(bill.proposerId());
        double available = Values.clamp(balance + sessionDrip, 0.0, balanceCap);
        double requiredBond = requiredBond(bill, context);
        if (available < requiredBond) {
            balancesByProposer.put(bill.proposerId(), available);
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "proposal bond unavailable");
        }

        balancesByProposer.put(bill.proposerId(), available - requiredBond);
        BillOutcome outcome = innerProcess.consider(bill, context);
        double refund = requiredBond * refundRate(outcome);
        double forfeiture = requiredBond - refund;
        balancesByProposer.put(
                bill.proposerId(),
                Values.clamp(balanceFor(bill.proposerId()) + refund, 0.0, balanceCap)
        );
        return outcome.withSignals(OutcomeSignals.proposalBond(forfeiture));
    }

    private double balanceFor(String proposerId) {
        return balancesByProposer.getOrDefault(proposerId, initialBalance);
    }

    private double requiredBond(Bill bill, VoteContext context) {
        double risk = AdaptiveTrackProcess.riskScore(bill, context);
        double publicValue = (0.55 * bill.publicBenefit()) + (0.35 * bill.publicSupport()) + (0.10 * bill.affectedGroupSupport());
        double sponsorDiscount = Math.min(0.30, bill.outsideBlocCosponsorCount() * 0.05);
        return Values.clamp(
                baseBond
                        + (riskWeight * risk)
                        + (lobbyWeight * Math.max(0.0, bill.lobbyPressure()))
                        + (0.18 * bill.publicBenefitUncertainty())
                        - (publicValueDiscount * publicValue)
                        - sponsorDiscount,
                0.10,
                balanceCap
        );
    }

    private static double refundRate(BillOutcome outcome) {
        Bill bill = outcome.bill();
        double support = outcome.enacted() ? outcome.averageYayShare() : bill.publicSupport();
        double legitimacy = AffectedGroupScoring.legitimacy(bill, support);
        double refund = (0.40 * bill.publicSupport())
                + (0.36 * bill.publicBenefit())
                + (0.24 * legitimacy);
        if (outcome.enacted() && support < 0.50) {
            refund *= 0.55;
        }
        if (bill.lobbyPressure() > 0.55 && bill.publicBenefit() < 0.45) {
            refund *= 0.50;
        }
        if (AffectedGroupScoring.minorityHarm(bill) > 0.20) {
            refund *= 0.72;
        }
        return Values.clamp(refund, 0.0, 1.0);
    }
}
