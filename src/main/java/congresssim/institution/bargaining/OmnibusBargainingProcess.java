package congresssim.institution.bargaining;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;

public final class OmnibusBargainingProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final int maxLineItems;
    private final double sidePaymentEfficiency;
    private final double transparency;
    private final double jurisdictionalFlexibility;

    public OmnibusBargainingProcess(
            String name,
            LegislativeProcess innerProcess,
            int maxLineItems,
            double sidePaymentEfficiency,
            double transparency,
            double jurisdictionalFlexibility
    ) {
        if (maxLineItems < 1) {
            throw new IllegalArgumentException("maxLineItems must be positive.");
        }
        Values.requireRange("sidePaymentEfficiency", sidePaymentEfficiency, 0.0, 1.0);
        Values.requireRange("transparency", transparency, 0.0, 1.0);
        Values.requireRange("jurisdictionalFlexibility", jurisdictionalFlexibility, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.maxLineItems = maxLineItems;
        this.sidePaymentEfficiency = sidePaymentEfficiency;
        this.transparency = transparency;
        this.jurisdictionalFlexibility = jurisdictionalFlexibility;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double need = bargainingNeed(bill, context);
        if (need < 0.22) {
            return innerProcess.consider(bill, context);
        }
        PackageResult result = buildPackage(bill, context, need);
        return innerProcess.consider(result.bill(), context)
                .withSignals(OutcomeSignals.diagnostics(Map.of(
                        "packageDealDepth", result.depth(),
                        "sidePaymentLoad", result.sidePaymentLoad(),
                        "omnibusComplexity", result.complexity(),
                        "jurisdictionalTradeRate", result.jurisdictionalTradeRate(),
                        "distributiveBargainShare", result.distributiveShare(),
                        "multidimensionalCompromiseGain", result.compromiseGain()
                )));
    }

    private PackageResult buildPackage(Bill bill, VoteContext context, double need) {
        int lineItems = Math.clamp((int) Math.round(1.0 + need * maxLineItems + bill.publicBenefitUncertainty()), 1, maxLineItems);
        double depth = Values.clamp(lineItems / (double) maxLineItems, 0.0, 1.0);
        double jurisdictionalTrades = Values.clamp(depth * jurisdictionalFlexibility * (0.70 + bill.salience()), 0.0, 1.0);
        double distributiveShare = Values.clamp(
                (0.28 + (0.52 * need)) * (0.45 + bill.concentratedHarm() + Math.max(0.0, bill.privateGain() - bill.publicBenefit())),
                0.0,
                1.0
        );
        double sidePaymentLoad = Values.clamp(depth * distributiveShare * (1.0 - (0.45 * transparency)), 0.0, 1.0);
        double complexity = Values.clamp(
                (0.11 * lineItems)
                        + (0.22 * jurisdictionalTrades)
                        + (0.20 * sidePaymentLoad)
                        + (0.18 * bill.publicBenefitUncertainty()),
                0.0,
                1.0
        );
        double coalitionGain = Values.clamp(
                (0.12 * depth)
                        + (0.14 * jurisdictionalTrades)
                        + (0.16 * sidePaymentEfficiency * distributiveShare)
                        - (0.08 * complexity),
                0.0,
                0.42
        );
        double harmReduction = Values.clamp(
                sidePaymentEfficiency * ((0.22 * distributiveShare) + (0.24 * bill.concentratedHarm()))
                        + (0.10 * transparency),
                0.0,
                0.78
        );
        double textComplexityCost = Values.clamp(
                complexity * (0.06 + (0.08 * (1.0 - transparency))) + (sidePaymentLoad * 0.05),
                0.0,
                0.22
        );
        double positionTarget = (0.55 * context.currentPolicyPosition()) + (0.45 * chamberCenter(context));
        double positionMovement = Values.clamp(0.12 * depth * need, 0.0, 0.32) * (positionTarget - bill.ideologyPosition());
        Bill revised = bill.withAmendment(
                Values.clamp(bill.ideologyPosition() + positionMovement, -1.0, 1.0),
                Values.clamp(bill.publicSupport() + coalitionGain, 0.0, 1.0),
                Values.clamp(bill.publicBenefit() + (0.06 * jurisdictionalTrades) - textComplexityCost, 0.0, 1.0)
        );
        double revisedHarm = Values.clamp(revised.concentratedHarm() * (1.0 - harmReduction), 0.0, 1.0);
        double affectedSupport = Values.clamp(
                revised.affectedGroupSupport()
                        + (0.62 * (revised.concentratedHarm() - revisedHarm))
                        + (0.12 * coalitionGain),
                0.0,
                1.0
        );
        int outsideSponsors = Math.max(1, (int) Math.round(1 + (jurisdictionalTrades * 3.0)));
        revised = revised
                .withCompensation(revised.publicBenefit(), affectedSupport, revisedHarm)
                .withCosponsorship(
                        revised.cosponsorCount() + lineItems,
                        revised.outsideBlocCosponsorCount() + outsideSponsors,
                        revised.affectedGroupSponsor() || affectedSupport >= 0.54
                )
                .withPublicBenefitUncertainty(Values.clamp(
                        revised.publicBenefitUncertainty() * (1.0 - (0.20 * transparency)) + (0.16 * complexity),
                        0.0,
                        1.0
                ))
                .withAttentionSpend(0.42 * lineItems + 1.40 * complexity);
        return new PackageResult(
                revised,
                depth,
                sidePaymentLoad,
                complexity,
                jurisdictionalTrades,
                distributiveShare,
                coalitionGain
        );
    }

    private static double bargainingNeed(Bill bill, VoteContext context) {
        return Values.clamp(
                (0.20 * Math.max(0.0, 0.62 - bill.publicSupport()) / 0.62)
                        + (0.22 * AffectedGroupScoring.minorityHarm(bill))
                        + (0.18 * bill.publicBenefitUncertainty())
                        + (0.16 * Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0)
                        + (0.14 * Math.max(0.0, bill.publicBenefit() - bill.publicSupport()))
                        + (0.10 * bill.salience()),
                0.0,
                1.0
        );
    }

    private static double chamberCenter(VoteContext context) {
        if (context.partyPositions().isEmpty()) {
            return context.currentPolicyPosition();
        }
        double sum = 0.0;
        for (double value : context.partyPositions().values()) {
            sum += value;
        }
        return sum / context.partyPositions().size();
    }

    private record PackageResult(
            Bill bill,
            double depth,
            double sidePaymentLoad,
            double complexity,
            double jurisdictionalTradeRate,
            double distributiveShare,
            double compromiseGain
    ) {
    }
}
