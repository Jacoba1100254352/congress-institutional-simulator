package congresssim.institution.publicinput;

import congresssim.institution.agenda.AgendaDisposition;
import congresssim.institution.chamber.ChamberVoteResult;
import congresssim.institution.chamber.PresidentialAction;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.lobbying.LobbyCaptureScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.List;

public final class CitizenInitiativeProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final double petitionThreshold;
    private final double referendumThreshold;
    private final double salienceThreshold;
    private final double misinformationRisk;

    public CitizenInitiativeProcess(
            String name,
            LegislativeProcess innerProcess,
            double petitionThreshold,
            double referendumThreshold,
            double salienceThreshold,
            double misinformationRisk
    ) {
        Values.requireRange("petitionThreshold", petitionThreshold, 0.0, 1.0);
        Values.requireRange("referendumThreshold", referendumThreshold, 0.0, 1.0);
        Values.requireRange("salienceThreshold", salienceThreshold, 0.0, 1.0);
        Values.requireRange("misinformationRisk", misinformationRisk, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.petitionThreshold = petitionThreshold;
        this.referendumThreshold = referendumThreshold;
        this.salienceThreshold = salienceThreshold;
        this.misinformationRisk = misinformationRisk;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        if (!qualifiesForInitiative(bill)) {
            return innerProcess.consider(bill, context);
        }

        double referendumSupport = referendumSupport(bill);
        int yay = (int) Math.round(referendumSupport * 1000.0);
        int nay = 1000 - yay;
        ChamberVoteResult referendum = new ChamberVoteResult(
                "Citizen referendum",
                "public majority",
                yay,
                nay,
                referendumSupport >= referendumThreshold
        );
        double statusQuoBefore = context.currentPolicyPosition();
        if (referendum.passed()) {
            return new BillOutcome(
                    bill,
                    statusQuoBefore,
                    bill.ideologyPosition(),
                    true,
                    AgendaDisposition.FLOOR_CONSIDERED,
                    List.of(),
                    List.of(referendum),
                    PresidentialAction.none(),
                    false,
                    OutcomeSignals.publicWill(
                            Math.abs(referendumSupport - bill.publicSupport()),
                            districtAlignmentProxy(bill, referendumSupport)
                    ),
                    "citizen initiative enacted by referendum"
            );
        }

        BillOutcome legislativeFallback = innerProcess.consider(bill, context);
        return legislativeFallback.withGateResult(referendum).withSignals(OutcomeSignals.publicWill(
                Math.abs(referendumSupport - bill.publicSupport()),
                districtAlignmentProxy(bill, referendumSupport)
        ));
    }

    private boolean qualifiesForInitiative(Bill bill) {
        double petitionSignal = (0.64 * bill.publicSupport())
                + (0.24 * bill.salience())
                + (bill.antiLobbyingReform() ? 0.10 : 0.0)
                - (0.16 * LobbyCaptureScoring.captureRisk(bill));
        return petitionSignal >= petitionThreshold && bill.salience() >= salienceThreshold;
    }

    private double referendumSupport(Bill bill) {
        double harmBacklash = bill.concentratedHarm() * (1.0 - bill.affectedGroupSupport()) * 0.22;
        double captureBacklash = LobbyCaptureScoring.captureRisk(bill) * 0.14;
        double misinformationBoost = Math.max(0.0, bill.privateGain() - bill.publicBenefit()) * misinformationRisk * 0.18;
        return Values.clamp(
                bill.publicSupport()
                        + (0.18 * (bill.publicBenefit() - bill.publicSupport()))
                        + misinformationBoost
                        - harmBacklash
                        - captureBacklash,
                0.0,
                1.0
        );
    }

    private static double districtAlignmentProxy(Bill bill, double referendumSupport) {
        return Values.clamp(1.0 - Math.abs(referendumSupport - bill.publicSupport()), 0.0, 1.0);
    }
}
