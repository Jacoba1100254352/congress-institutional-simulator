package congresssim.institution.accountability;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class QuadraticAttentionBudgetProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess downstreamProcess;
    private final Map<String, Double> creditsByLegislator;
    private final double initialCredits;
    private final int maxUnits;

    public QuadraticAttentionBudgetProcess(
            String name,
            LegislativeProcess downstreamProcess,
            List<Legislator> legislators,
            double initialCredits,
            int maxUnits
    ) {
        if (initialCredits <= 0.0) {
            throw new IllegalArgumentException("initialCredits must be positive.");
        }
        if (maxUnits <= 0) {
            throw new IllegalArgumentException("maxUnits must be positive.");
        }
        this.name = name;
        this.downstreamProcess = downstreamProcess;
        this.initialCredits = initialCredits;
        this.maxUnits = maxUnits;
        this.creditsByLegislator = new HashMap<>();
        for (Legislator legislator : legislators) {
            creditsByLegislator.put(legislator.id(), initialCredits);
        }
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double cost = proposalCost(bill, context.currentPolicyPosition());
        double available = creditsByLegislator.getOrDefault(bill.proposerId(), initialCredits);
        if (available + 0.000001 < cost) {
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "insufficient quadratic attention credits");
        }
        creditsByLegislator.put(bill.proposerId(), available - cost);
        return downstreamProcess.consider(bill.withAttentionSpend(cost), context);
    }

    private double proposalCost(Bill bill, double statusQuo) {
        double risk = Values.clamp(
                (0.32 * Math.abs(bill.ideologyPosition() - statusQuo))
                        + (0.24 * (1.0 - bill.publicSupport()))
                        + (0.20 * Math.max(0.0, bill.lobbyPressure()))
                        + (0.16 * bill.salience())
                        + (0.20 * bill.concentratedHarm()),
                0.0,
                1.0
        );
        int units = Math.clamp(1 + (int) Math.round(risk * maxUnits), 1, maxUnits);
        double publicDiscount = 1.0 - (0.18 * bill.publicSupport()) - (0.18 * bill.publicBenefit());
        double harmPremium = 1.0 + (0.24 * bill.concentratedHarm());
        return Math.max(1.0, units * units * publicDiscount * harmPremium);
    }
}
