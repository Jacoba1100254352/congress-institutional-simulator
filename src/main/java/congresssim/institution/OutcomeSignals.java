package congresssim.institution;

public record OutcomeSignals(
        int lawReviews,
        int lawReversals,
        int lawRenewals,
        double activeLawWelfare,
        double lowSupportActiveLawShare,
        int alternativeRounds,
        int alternativesConsidered,
        int statusQuoWins,
        double selectedAlternativeMedianDistance,
        double proposerAgendaAdvantage,
        int citizenReviews,
        int citizenCertifications,
        double citizenLegitimacy,
        int objectionWindows,
        int repealWindowReversals
) {
    public static OutcomeSignals none() {
        return new OutcomeSignals(0, 0, 0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0, 0, 0.0, 0, 0);
    }

    public OutcomeSignals plus(OutcomeSignals other) {
        return new OutcomeSignals(
                lawReviews + other.lawReviews,
                lawReversals + other.lawReversals,
                lawRenewals + other.lawRenewals,
                activeLawWelfare + other.activeLawWelfare,
                lowSupportActiveLawShare + other.lowSupportActiveLawShare,
                alternativeRounds + other.alternativeRounds,
                alternativesConsidered + other.alternativesConsidered,
                statusQuoWins + other.statusQuoWins,
                selectedAlternativeMedianDistance + other.selectedAlternativeMedianDistance,
                proposerAgendaAdvantage + other.proposerAgendaAdvantage,
                citizenReviews + other.citizenReviews,
                citizenCertifications + other.citizenCertifications,
                citizenLegitimacy + other.citizenLegitimacy,
                objectionWindows + other.objectionWindows,
                repealWindowReversals + other.repealWindowReversals
        );
    }

    public static OutcomeSignals lawReview(
            boolean reversed,
            boolean renewed,
            double activeLawWelfare,
            double lowSupportActiveLawShare
    ) {
        return new OutcomeSignals(
                1,
                reversed ? 1 : 0,
                renewed ? 1 : 0,
                activeLawWelfare,
                lowSupportActiveLawShare,
                0,
                0,
                0,
                0.0,
                0.0,
                0,
                0,
                0.0,
                0,
                0
        );
    }

    public static OutcomeSignals alternatives(
            int alternativesConsidered,
            boolean statusQuoWon,
            double selectedAlternativeMedianDistance,
            double proposerAgendaAdvantage
    ) {
        return new OutcomeSignals(
                0,
                0,
                0,
                0.0,
                0.0,
                1,
                alternativesConsidered,
                statusQuoWon ? 1 : 0,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                0,
                0,
                0.0,
                0,
                0
        );
    }

    public static OutcomeSignals citizenReview(boolean certified, double legitimacy) {
        return new OutcomeSignals(
                0,
                0,
                0,
                0.0,
                0.0,
                0,
                0,
                0,
                0.0,
                0.0,
                1,
                certified ? 1 : 0,
                legitimacy,
                0,
                0
        );
    }

    public static OutcomeSignals objectionWindow(boolean reversal) {
        return new OutcomeSignals(
                0,
                0,
                0,
                0.0,
                0.0,
                0,
                0,
                0,
                0.0,
                0.0,
                0,
                0,
                0.0,
                1,
                reversal ? 1 : 0
        );
    }
}
