package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public final class CoalitionCosponsorshipProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final int minimumCosponsors;
    private final int minimumOutsideBlocs;
    private final double minimumIdeologicalDistance;
    private final double cosponsorThreshold;
    private final boolean requireAffectedGroupSponsor;
    private final boolean applyAgendaCreditDiscount;

    public CoalitionCosponsorshipProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            int minimumCosponsors,
            int minimumOutsideBlocs,
            double minimumIdeologicalDistance,
            double cosponsorThreshold,
            boolean requireAffectedGroupSponsor,
            boolean applyAgendaCreditDiscount
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.minimumCosponsors = minimumCosponsors;
        this.minimumOutsideBlocs = minimumOutsideBlocs;
        this.minimumIdeologicalDistance = minimumIdeologicalDistance;
        this.cosponsorThreshold = cosponsorThreshold;
        this.requireAffectedGroupSponsor = requireAffectedGroupSponsor;
        this.applyAgendaCreditDiscount = applyAgendaCreditDiscount;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Sponsorship sponsorship = evaluate(bill, context);
        boolean admitted = sponsorship.cosponsorCount() >= minimumCosponsors
                && sponsorship.outsideBlocCount() >= minimumOutsideBlocs
                && (!requireAffectedGroupSponsor || sponsorship.affectedGroupSponsor());
        Bill signaledBill = bill.withCosponsorship(
                sponsorship.cosponsorCount(),
                sponsorship.outsideBlocCount(),
                sponsorship.affectedGroupSponsor()
        );
        if (applyAgendaCreditDiscount && admitted) {
            double breadthBonus = Math.min(0.12, sponsorship.outsideBlocCount() * 0.03);
            signaledBill = signaledBill.withPublicWillSignal(
                    Values.clamp(signaledBill.publicSupport() + breadthBonus, 0.0, 1.0),
                    Values.clamp(signaledBill.affectedGroupSupport() + (sponsorship.affectedGroupSponsor() ? 0.08 : 0.0), 0.0, 1.0),
                    signaledBill.salience(),
                    Math.max(0.0, signaledBill.publicBenefitUncertainty() - breadthBonus)
            );
        }
        OutcomeSignals signals = OutcomeSignals.cosponsorship(
                admitted,
                sponsorship.affectedGroupSponsor(),
                sponsorship.cosponsorCount()
        );
        if (!admitted) {
            return BillOutcome.accessDenied(
                    signaledBill,
                    context.currentPolicyPosition(),
                    "coalition cosponsorship denied"
            ).withSignals(signals);
        }
        return innerProcess.consider(signaledBill, context).withSignals(signals);
    }

    private Sponsorship evaluate(Bill bill, VoteContext context) {
        Legislator proposer = proposerFor(bill);
        if (proposer == null) {
            return new Sponsorship(0, 0, false);
        }
        int cosponsors = 0;
        boolean affectedGroupSponsor = false;
        Set<String> outsideBlocs = new LinkedHashSet<>();
        for (Legislator legislator : legislators) {
            if (legislator.id().equals(proposer.id()) || !isOutsideBloc(proposer, legislator)) {
                continue;
            }
            double score = cosponsorScore(legislator, bill, context);
            if (score < cosponsorThreshold) {
                continue;
            }
            cosponsors++;
            outsideBlocs.add(legislator.party());
            if (legislator.affectedGroupSensitivity() >= 0.62 && bill.affectedGroupSupport() >= 0.42) {
                affectedGroupSponsor = true;
            }
        }
        return new Sponsorship(cosponsors, outsideBlocs.size(), affectedGroupSponsor);
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
        double districtFit = 1.0 - (Math.abs(bill.ideologyPosition() - legislator.districtPreference()) / 2.0);
        double ideologicalFit = 1.0 - (Math.abs(bill.ideologyPosition() - legislator.ideology()) / 2.0);
        double publicPull = legislator.constituencySensitivity() * bill.publicSupport();
        double welfarePull = legislator.reputationSensitivity() * bill.publicBenefit();
        double affectedPull = legislator.affectedGroupSensitivity() * bill.affectedGroupSupport();
        double moderationBonus = legislator.compromisePreference() * (1.0 - Math.abs(bill.ideologyPosition()));
        double shiftPenalty = Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
        double lobbyRisk = Math.max(0.0, bill.lobbyPressure()) * (1.0 - bill.publicSupport());
        return (0.20 * districtFit)
                + (0.18 * ideologicalFit)
                + (0.18 * publicPull)
                + (0.16 * welfarePull)
                + (0.12 * affectedPull)
                + (0.12 * moderationBonus)
                - (0.16 * shiftPenalty)
                - (0.14 * legislator.reputationSensitivity() * lobbyRisk);
    }

    private record Sponsorship(int cosponsorCount, int outsideBlocCount, boolean affectedGroupSponsor) {
    }
}
