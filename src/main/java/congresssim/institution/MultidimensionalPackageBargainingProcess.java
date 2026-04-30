package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.List;

public final class MultidimensionalPackageBargainingProcess implements LegislativeProcess {
    private static final List<String> TRADE_DOMAINS = List.of(
            "tax",
            "health",
            "energy",
            "technology",
            "labor",
            "housing",
            "democracy"
    );

    private final String name;
    private final LegislativeProcess innerProcess;
    private final double needThreshold;
    private final int maxIssueTrades;
    private final double tradeEffectiveness;
    private final double complexityCost;
    private final double coalitionBreadthWeight;

    public MultidimensionalPackageBargainingProcess(
            String name,
            LegislativeProcess innerProcess,
            double needThreshold,
            int maxIssueTrades,
            double tradeEffectiveness,
            double complexityCost,
            double coalitionBreadthWeight
    ) {
        Values.requireRange("needThreshold", needThreshold, 0.0, 1.0);
        if (maxIssueTrades < 1) {
            throw new IllegalArgumentException("maxIssueTrades must be positive.");
        }
        Values.requireRange("tradeEffectiveness", tradeEffectiveness, 0.0, 1.0);
        Values.requireRange("complexityCost", complexityCost, 0.0, 1.0);
        Values.requireRange("coalitionBreadthWeight", coalitionBreadthWeight, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.needThreshold = needThreshold;
        this.maxIssueTrades = maxIssueTrades;
        this.tradeEffectiveness = tradeEffectiveness;
        this.complexityCost = complexityCost;
        this.coalitionBreadthWeight = coalitionBreadthWeight;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double need = bargainingNeed(bill, context);
        if (need < needThreshold) {
            return innerProcess.consider(bill, context);
        }
        return innerProcess.consider(buildPackage(bill, context, need), context);
    }

    private Bill buildPackage(Bill bill, VoteContext context, double need) {
        int tradeCount = tradeCount(bill, need);
        double coalitionBreadth = Values.clamp(
                (bill.outsideBlocCosponsorCount() / 4.0) + (tradeCount * 0.10),
                0.0,
                1.0
        );
        double tradeQuality = 0.0;
        for (int index = 0; index < tradeCount; index++) {
            tradeQuality += issueTradeScore(bill, index);
        }
        tradeQuality /= tradeCount;

        double crossIssueSpread = Values.clamp(tradeCount / (double) maxIssueTrades, 0.0, 1.0);
        double outsideBlocBoost = Values.clamp((coalitionBreadth * 0.08) + (crossIssueSpread * 0.05), 0.0, 0.16);
        double exemptionRelief = Values.clamp(
                tradeEffectiveness * ((0.08 * tradeCount) + (0.18 * AffectedGroupScoring.minorityHarm(bill))),
                0.0,
                0.52
        );
        double phaseInConcession = Values.clamp(0.06 * need * (0.50 + bill.publicBenefitUncertainty()), 0.0, 0.12);
        double distributiveSidePayment = Values.clamp(
                complexityCost * (0.04 * tradeCount) * (0.35 + bill.concentratedHarm() + bill.privateGain()),
                0.0,
                0.26
        );
        double supportGain = tradeEffectiveness
                * ((0.10 * need)
                + (0.09 * tradeQuality)
                + (coalitionBreadthWeight * coalitionBreadth * 0.10)
                + outsideBlocBoost
                + phaseInConcession);
        double harmReduction = Values.clamp(
                tradeEffectiveness * (0.18 + (0.16 * tradeQuality) + (0.10 * coalitionBreadth))
                        + exemptionRelief,
                0.0,
                0.86
        );
        double implementationCost = complexityCost
                * tradeCount
                * (0.035 + (0.045 * bill.publicBenefitUncertainty()) + (0.025 * bill.salience()));
        double bargainingComplexity = implementationCost + distributiveSidePayment + (phaseInConcession * 0.35);
        double ideologyPull = (0.05 * tradeCount * need * (context.currentPolicyPosition() - bill.ideologyPosition()))
                + (0.025 * coalitionBreadth * (chamberCenter(context) - bill.ideologyPosition()));
        Bill revised = bill.withAmendment(
                Values.clamp(bill.ideologyPosition() + ideologyPull, -1.0, 1.0),
                Values.clamp(bill.publicSupport() + supportGain, 0.0, 1.0),
                Values.clamp(bill.publicBenefit() + (tradeQuality * 0.05) - bargainingComplexity, 0.0, 1.0)
        );
        double revisedHarm = Values.clamp(revised.concentratedHarm() * (1.0 - harmReduction), 0.0, 1.0);
        double affectedSupport = Values.clamp(
                revised.affectedGroupSupport()
                        + ((revised.concentratedHarm() - revisedHarm) * 0.66)
                        + (supportGain * 0.20)
                        + (phaseInConcession * 0.42),
                0.0,
                1.0
        );
        int addedCosponsors = Math.max(1, tradeCount + (int) Math.round(coalitionBreadth * 2.0));
        int addedOutsideBlocs = Math.max(1, (int) Math.ceil(crossIssueSpread * 2.0));
        double uncertaintyReduction = Values.clamp(
                (0.04 * tradeCount) + (0.08 * tradeQuality) + (0.04 * coalitionBreadth),
                0.0,
                0.38
        );
        return revised
                .withPublicBenefitUncertainty(Values.clamp(
                        revised.publicBenefitUncertainty() * (1.0 - uncertaintyReduction),
                        0.0,
                        1.0
                ))
                .withCosponsorship(
                        revised.cosponsorCount() + addedCosponsors,
                        revised.outsideBlocCosponsorCount() + addedOutsideBlocs,
                        revised.affectedGroupSponsor() || affectedSupport >= 0.55
                )
                .withCompensation(revised.publicBenefit(), affectedSupport, revisedHarm)
                .withAttentionSpend(tradeCount * (0.34 + (complexityCost * 0.62) + (crossIssueSpread * 0.18)));
    }

    private int tradeCount(Bill bill, double need) {
        double rawCount = 1.0 + (need * maxIssueTrades) + (bill.publicBenefitUncertainty() * 1.5);
        return Math.clamp((int) Math.round(rawCount), 1, maxIssueTrades);
    }

    private static double bargainingNeed(Bill bill, VoteContext context) {
        double lowSupport = Math.max(0.0, 0.60 - bill.publicSupport()) / 0.60;
        double harm = AffectedGroupScoring.minorityHarm(bill);
        double uncertainty = bill.publicBenefitUncertainty();
        double distance = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double mismatch = Math.max(0.0, bill.publicBenefit() - bill.publicSupport());
        return Values.clamp(
                (0.22 * lowSupport)
                        + (0.26 * harm)
                        + (0.18 * uncertainty)
                        + (0.16 * distance)
                        + (0.18 * mismatch),
                0.0,
                1.0
        );
    }

    private static double issueTradeScore(Bill bill, int index) {
        String otherDomain = TRADE_DOMAINS.get(Math.floorMod(bill.issueDomain().hashCode() + index + 1, TRADE_DOMAINS.size()));
        int hash = Math.floorMod((bill.id() + ":" + bill.issueDomain() + ":" + otherDomain + ":" + index).hashCode(), 1000);
        double compatibility = hash / 999.0;
        double domainDistance = bill.issueDomain().equals(otherDomain) ? 0.15 : 0.55;
        return Values.clamp((0.65 * compatibility) + (0.35 * domainDistance), 0.0, 1.0);
    }

    private static double chamberCenter(VoteContext context) {
        if (context.partyPositions().isEmpty()) {
            return context.currentPolicyPosition();
        }
        double sum = 0.0;
        for (double position : context.partyPositions().values()) {
            sum += position;
        }
        return sum / context.partyPositions().size();
    }
}
