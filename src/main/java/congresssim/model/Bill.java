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
        double salience,
        double privateGain,
        boolean antiLobbyingReform,
        String issueDomain,
        double lobbySpend,
        double defensiveLobbySpend,
        double originalIdeologyPosition,
        double amendmentMovement
) {
    public Bill {
        Values.requireRange("proposerIdeology", proposerIdeology, -1.0, 1.0);
        Values.requireRange("ideologyPosition", ideologyPosition, -1.0, 1.0);
        Values.requireRange("publicSupport", publicSupport, 0.0, 1.0);
        Values.requireRange("publicBenefit", publicBenefit, 0.0, 1.0);
        Values.requireRange("lobbyPressure", lobbyPressure, -1.0, 1.0);
        Values.requireRange("salience", salience, 0.0, 1.0);
        Values.requireRange("privateGain", privateGain, 0.0, 1.0);
        Values.requireRange("lobbySpend", lobbySpend, 0.0, 100.0);
        Values.requireRange("defensiveLobbySpend", defensiveLobbySpend, 0.0, 100.0);
        Values.requireRange("originalIdeologyPosition", originalIdeologyPosition, -1.0, 1.0);
        Values.requireRange("amendmentMovement", amendmentMovement, 0.0, 10.0);
    }

    public Bill(
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
        this(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                Math.max(0.0, lobbyPressure),
                false,
                "general",
                0.0,
                0.0,
                ideologyPosition,
                0.0
        );
    }

    public Bill(
            String id,
            String title,
            String proposerId,
            double proposerIdeology,
            double ideologyPosition,
            double publicSupport,
            double publicBenefit,
            double lobbyPressure,
            double salience,
            double privateGain,
            boolean antiLobbyingReform
    ) {
        this(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                antiLobbyingReform,
                antiLobbyingReform ? "democracy" : "general",
                0.0,
                0.0,
                ideologyPosition,
                0.0
        );
    }

    public Bill(
            String id,
            String title,
            String proposerId,
            double proposerIdeology,
            double ideologyPosition,
            double publicSupport,
            double publicBenefit,
            double lobbyPressure,
            double salience,
            double privateGain,
            boolean antiLobbyingReform,
            String issueDomain,
            double lobbySpend,
            double defensiveLobbySpend
    ) {
        this(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                publicSupport,
                publicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                antiLobbyingReform,
                issueDomain,
                lobbySpend,
                defensiveLobbySpend,
                ideologyPosition,
                0.0
        );
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
                revisedSalience,
                privateGain,
                antiLobbyingReform,
                issueDomain,
                lobbySpend,
                defensiveLobbySpend,
                originalIdeologyPosition,
                amendmentMovement
        );
    }

    public Bill withLobbySignal(double revisedLobbyPressure, double revisedPublicSupport) {
        return new Bill(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                revisedPublicSupport,
                publicBenefit,
                revisedLobbyPressure,
                salience,
                privateGain,
                antiLobbyingReform,
                issueDomain,
                lobbySpend,
                defensiveLobbySpend,
                originalIdeologyPosition,
                amendmentMovement
        );
    }

    public Bill withLobbyActivity(
            double revisedLobbyPressure,
            double revisedPublicSupport,
            double revisedPrivateGain,
            double addedLobbySpend,
            double addedDefensiveLobbySpend
    ) {
        return new Bill(
                id,
                title,
                proposerId,
                proposerIdeology,
                ideologyPosition,
                revisedPublicSupport,
                publicBenefit,
                revisedLobbyPressure,
                salience,
                revisedPrivateGain,
                antiLobbyingReform,
                issueDomain,
                lobbySpend + addedLobbySpend,
                defensiveLobbySpend + addedDefensiveLobbySpend,
                originalIdeologyPosition,
                amendmentMovement
        );
    }

    public Bill withAmendment(
            double revisedIdeologyPosition,
            double revisedPublicSupport,
            double revisedPublicBenefit
    ) {
        return new Bill(
                id,
                title,
                proposerId,
                proposerIdeology,
                revisedIdeologyPosition,
                revisedPublicSupport,
                revisedPublicBenefit,
                lobbyPressure,
                salience,
                privateGain,
                antiLobbyingReform,
                issueDomain,
                lobbySpend,
                defensiveLobbySpend,
                originalIdeologyPosition,
                amendmentMovement + Math.abs(revisedIdeologyPosition - ideologyPosition)
        );
    }
}
