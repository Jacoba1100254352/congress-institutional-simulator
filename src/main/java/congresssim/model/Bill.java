package congresssim.model;

import congresssim.util.Values;

public record Bill(
        String id,
        String title,
        String proposerId,
        double proposerIdeology,
        double ideologyPosition,
        double publicSupport,
        double publicBenefit,
        double lobbyPressure,
        double salience
) {
    public Bill {
        Values.requireRange("proposerIdeology", proposerIdeology, -1.0, 1.0);
        Values.requireRange("ideologyPosition", ideologyPosition, -1.0, 1.0);
        Values.requireRange("publicSupport", publicSupport, 0.0, 1.0);
        Values.requireRange("publicBenefit", publicBenefit, 0.0, 1.0);
        Values.requireRange("lobbyPressure", lobbyPressure, -1.0, 1.0);
        Values.requireRange("salience", salience, 0.0, 1.0);
    }

    public Bill withPublicSignal(double revisedPublicSupport, double revisedSalience) {
        return new Bill(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                revisedPublicSupport,
                publicBenefit,
                lobbyPressure,
                revisedSalience
        );
    }
}
