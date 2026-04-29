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
    private final Map<String, Double> trustByProposer = new HashMap<>();
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
        double trust = trustByProposer.getOrDefault(bill.proposerId(), 0.55);
        double risk = proposalRisk(bill, context);
        if (trust < 0.30 && risk >= withdrawalThreshold && bill.publicBenefit() < 0.62) {
            trustByProposer.put(bill.proposerId(), Values.clamp(trust + 0.03, 0.0, 1.0));
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "strategic proposer withdrawal");
        }

        Bill revisedBill = adaptBill(bill, context, trust, risk);
        BillOutcome outcome = innerProcess.consider(revisedBill, context);
        updateTrust(revisedBill, outcome);
        return outcome;
    }

    private Bill adaptBill(Bill bill, VoteContext context, double trust, double risk) {
        double moderationRate = Values.clamp(adaptationStrength * risk * (1.10 - trust), 0.0, 0.70);
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

    private void updateTrust(Bill bill, BillOutcome outcome) {
        double current = trustByProposer.getOrDefault(bill.proposerId(), 0.55);
        double quality = (0.42 * bill.publicBenefit())
                + (0.28 * bill.publicSupport())
                + (0.18 * (1.0 - LobbyCaptureScoring.captureRisk(bill)))
                + (0.12 * bill.affectedGroupSupport());
        double enactedBonus = outcome.enacted() ? 0.08 : -0.05;
        double lowSupportPenalty = outcome.enacted() && bill.publicSupport() < 0.45 ? 0.12 : 0.0;
        double updated = current + (0.18 * (quality - 0.50)) + enactedBonus - lowSupportPenalty;
        trustByProposer.put(bill.proposerId(), Values.clamp(updated, 0.0, 1.0));
    }
}
