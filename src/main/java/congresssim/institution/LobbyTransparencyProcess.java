package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class LobbyTransparencyProcess implements LegislativeProcess {
    private final String name;
    private final double disclosureStrength;
    private final double backlashWeight;
    private final LegislativeProcess innerProcess;

    public LobbyTransparencyProcess(
            String name,
            double disclosureStrength,
            double backlashWeight,
            LegislativeProcess innerProcess
    ) {
        Values.requireRange("disclosureStrength", disclosureStrength, 0.0, 1.0);
        Values.requireRange("backlashWeight", backlashWeight, 0.0, 1.0);
        this.name = name;
        this.disclosureStrength = disclosureStrength;
        this.backlashWeight = backlashWeight;
        this.innerProcess = innerProcess;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double revisedLobbyPressure = bill.lobbyPressure() * (1.0 - disclosureStrength);
        double revisedPublicSupport = revisedPublicSupport(bill);
        return innerProcess.consider(bill.withLobbySignal(revisedLobbyPressure, revisedPublicSupport), context);
    }

    private double revisedPublicSupport(Bill bill) {
        double support = bill.publicSupport();
        if (bill.antiLobbyingReform()) {
            double suppressedSupport = Math.max(0.0, bill.publicBenefit() - bill.publicSupport());
            support += backlashWeight * disclosureStrength * Math.max(0.0, -bill.lobbyPressure()) * (0.20 + suppressedSupport);
        } else {
            double captureRisk = LobbyCaptureScoring.captureRisk(bill);
            support -= backlashWeight * disclosureStrength * captureRisk * Math.max(0.0, bill.lobbyPressure());
        }
        return Values.clamp(support, 0.0, 1.0);
    }
}
