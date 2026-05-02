package congresssim.institution.agenda;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;

import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public final class CrossBlocCosponsorshipAccessRule implements ProposalAccessRule {
    private final List<Legislator> legislators;
    private final int minimumCosponsors;
    private final int minimumOutsideBlocs;
    private final double minimumIdeologicalDistance;
    private final double cosponsorThreshold;

    public CrossBlocCosponsorshipAccessRule(
            List<Legislator> legislators,
            int minimumCosponsors,
            int minimumOutsideBlocs,
            double minimumIdeologicalDistance,
            double cosponsorThreshold
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        if (minimumCosponsors < 1) {
            throw new IllegalArgumentException("minimumCosponsors must be positive.");
        }
        if (minimumOutsideBlocs < 1) {
            throw new IllegalArgumentException("minimumOutsideBlocs must be positive.");
        }
        if (minimumIdeologicalDistance < 0.0) {
            throw new IllegalArgumentException("minimumIdeologicalDistance must not be negative.");
        }
        if (cosponsorThreshold < 0.0) {
            throw new IllegalArgumentException("cosponsorThreshold must not be negative.");
        }
        this.legislators = List.copyOf(legislators);
        this.minimumCosponsors = minimumCosponsors;
        this.minimumOutsideBlocs = minimumOutsideBlocs;
        this.minimumIdeologicalDistance = minimumIdeologicalDistance;
        this.cosponsorThreshold = cosponsorThreshold;
    }

    @Override
    public String name() {
        return "cross-bloc cosponsorship";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        Legislator proposer = proposerFor(bill);
        if (proposer == null) {
            return AccessDecision.denied("cross-bloc cosponsorship denied: proposer not found");
        }

        int cosponsors = 0;
        Set<String> outsideBlocs = new LinkedHashSet<>();
        for (Legislator legislator : legislators) {
            if (legislator.id().equals(proposer.id())) {
                continue;
            }
            if (!isOutsideBloc(proposer, legislator)) {
                continue;
            }
            if (cosponsorScore(legislator, bill, context) >= cosponsorThreshold) {
                cosponsors++;
                outsideBlocs.add(legislator.party());
            }
        }

        if (cosponsors < minimumCosponsors || outsideBlocs.size() < minimumOutsideBlocs) {
            return AccessDecision.denied(
                    "cross-bloc cosponsorship denied: "
                            + cosponsors
                            + " cosponsors from "
                            + outsideBlocs.size()
                            + " outside blocs"
            );
        }
        return AccessDecision.granted(
                "cross-bloc cosponsorship granted: "
                        + cosponsors
                        + " cosponsors from "
                        + outsideBlocs.size()
                        + " outside blocs"
        );
    }

    private Legislator proposerFor(Bill bill) {
        for (Legislator legislator : legislators) {
            if (legislator.id().equals(bill.proposerId())) {
                return legislator;
            }
        }
        return null;
    }

    private boolean isOutsideBloc(Legislator proposer, Legislator legislator) {
        return !legislator.party().equals(proposer.party())
                && Math.abs(legislator.ideology() - proposer.ideology()) >= minimumIdeologicalDistance;
    }

    private static double cosponsorScore(Legislator legislator, Bill bill, VoteContext context) {
        double ideologicalFit = 1.0 - (Math.abs(bill.ideologyPosition() - legislator.ideology()) / 2.0);
        double partyFit = 1.0 - (Math.abs(bill.ideologyPosition() - context.partyPosition(legislator.party())) / 2.0);
        double publicPull = legislator.constituencySensitivity() * bill.publicSupport();
        double welfarePull = legislator.reputationSensitivity() * bill.publicBenefit();
        double moderationBonus = legislator.compromisePreference() * (1.0 - Math.abs(bill.ideologyPosition()));
        double shiftPenalty = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double lobbyRisk = Math.max(0.0, bill.lobbyPressure()) * (1.0 - bill.publicSupport());

        return (0.30 * ideologicalFit)
                + (0.16 * partyFit)
                + (0.20 * publicPull)
                + (0.18 * welfarePull)
                + (0.14 * moderationBonus)
                - (0.18 * shiftPenalty)
                - (0.16 * legislator.reputationSensitivity() * lobbyRisk);
    }
}
