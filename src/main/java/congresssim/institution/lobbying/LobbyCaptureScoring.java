package congresssim.institution.lobbying;

import congresssim.model.Bill;
import congresssim.util.Values;

public final class LobbyCaptureScoring {
    private LobbyCaptureScoring() {
    }

    public static double captureRisk(Bill bill) {
        if (bill.antiLobbyingReform()) {
            return 0.0;
        }

        double positiveLobbyPressure = Math.max(0.0, bill.lobbyPressure());
        double publicWeakness = 1.0 - publicInterestScore(bill);
        return Values.clamp(
                (0.42 * positiveLobbyPressure)
                        + (0.34 * bill.privateGain())
                        + (0.24 * publicWeakness),
                0.0,
                1.0
        );
    }

    public static double publicInterestScore(Bill bill) {
        return Values.clamp(
                (0.56 * bill.publicBenefit())
                        + (0.34 * bill.publicSupport())
                        + (0.10 * (1.0 - Math.max(0.0, bill.lobbyPressure()))),
                0.0,
                1.0
        );
    }

    public static double publicAlignment(double yayShare, Bill bill) {
        return Values.clamp(1.0 - Math.abs(yayShare - bill.publicSupport()), 0.0, 1.0);
    }

    public static double privateGainRatio(Bill bill) {
        return Values.clamp(bill.privateGain() / Math.max(0.15, bill.publicBenefit()), 0.0, 5.0);
    }
}
