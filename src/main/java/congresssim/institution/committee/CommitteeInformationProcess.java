package congresssim.institution.committee;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.List;

public final class CommitteeInformationProcess implements LegislativeProcess {
    private final String name;
    private final List<Legislator> committeeMembers;
    private final double informationStrength;
    private final double captureStrength;
    private final LegislativeProcess innerProcess;
    private final double truthSeeking;
    private final double captureSusceptibility;

    public CommitteeInformationProcess(
            String name,
            List<Legislator> committeeMembers,
            double informationStrength,
            double captureStrength,
            LegislativeProcess innerProcess
    ) {
        if (committeeMembers.isEmpty()) {
            throw new IllegalArgumentException("committeeMembers must not be empty.");
        }
        Values.requireRange("informationStrength", informationStrength, 0.0, 1.0);
        Values.requireRange("captureStrength", captureStrength, 0.0, 1.0);
        this.name = name;
        this.committeeMembers = List.copyOf(committeeMembers);
        this.informationStrength = informationStrength;
        this.captureStrength = captureStrength;
        this.innerProcess = innerProcess;
        this.truthSeeking = calculateTruthSeeking(committeeMembers);
        this.captureSusceptibility = committeeMembers.stream()
                .mapToDouble(Legislator::lobbySensitivity)
                .average()
                .orElse(0.0);
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double truthWeight = Values.clamp(informationStrength * truthSeeking, 0.0, 1.0);
        double lobbySpin = captureStrength * captureSusceptibility * bill.lobbyPressure() * (1.0 - truthWeight) * 0.40;
        double revisedSupport = Values.clamp(
                bill.publicSupport() + (truthWeight * (bill.publicBenefit() - bill.publicSupport())) + lobbySpin,
                0.0,
                1.0
        );
        double revisedSalience = Values.clamp(
                bill.salience() + (Math.abs(bill.publicBenefit() - bill.publicSupport()) * truthWeight * 0.25),
                0.0,
                1.0
        );

        return innerProcess.consider(bill.withPublicSignal(revisedSupport, revisedSalience), context);
    }

    private static double calculateTruthSeeking(List<Legislator> committeeMembers) {
        double total = 0.0;
        for (Legislator member : committeeMembers) {
            double publicOrientation = (
                    member.compromisePreference()
                            + member.reputationSensitivity()
                            + member.constituencySensitivity()
            ) / 3.0;
            total += publicOrientation * (1.0 - (member.lobbySensitivity() * 0.5));
        }
        return total / committeeMembers.size();
    }
}

