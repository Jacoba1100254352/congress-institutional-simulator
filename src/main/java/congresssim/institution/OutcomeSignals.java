package congresssim.institution;

public record OutcomeSignals(
        int lawReviews,
        int lawReversals,
        int lawRenewals,
        int lawCorrections,
        double correctionDelay,
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
        int repealWindowReversals,
        int fastLaneRoutes,
        int middleLaneRoutes,
        int highRiskRoutes,
        int challengeTokenExhaustions,
        int falseNegativePasses,
        int publicWillReviews,
        double publicSignalMovement,
        double districtAlignment,
        int cosponsorshipReviews,
        int crossBlocAdmissions,
        int affectedGroupSponsors,
        int totalCosponsors,
        int proposalBondReviews,
        double proposalBondForfeiture,
        int strategicAlternativeRounds,
        int strategicDecoys
) {
    public static OutcomeSignals none() {
        return zero();
    }

    public OutcomeSignals plus(OutcomeSignals other) {
        return new OutcomeSignals(
                lawReviews + other.lawReviews,
                lawReversals + other.lawReversals,
                lawRenewals + other.lawRenewals,
                lawCorrections + other.lawCorrections,
                correctionDelay + other.correctionDelay,
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
                repealWindowReversals + other.repealWindowReversals,
                fastLaneRoutes + other.fastLaneRoutes,
                middleLaneRoutes + other.middleLaneRoutes,
                highRiskRoutes + other.highRiskRoutes,
                challengeTokenExhaustions + other.challengeTokenExhaustions,
                falseNegativePasses + other.falseNegativePasses,
                publicWillReviews + other.publicWillReviews,
                publicSignalMovement + other.publicSignalMovement,
                districtAlignment + other.districtAlignment,
                cosponsorshipReviews + other.cosponsorshipReviews,
                crossBlocAdmissions + other.crossBlocAdmissions,
                affectedGroupSponsors + other.affectedGroupSponsors,
                totalCosponsors + other.totalCosponsors,
                proposalBondReviews + other.proposalBondReviews,
                proposalBondForfeiture + other.proposalBondForfeiture,
                strategicAlternativeRounds + other.strategicAlternativeRounds,
                strategicDecoys + other.strategicDecoys
        );
    }

    public static OutcomeSignals lawReview(
            boolean reversed,
            boolean renewed,
            double activeLawWelfare,
            double lowSupportActiveLawShare,
            double correctionDelay
    ) {
        return zero(
                reversed ? 1 : 0,
                renewed ? 1 : 0,
                reversed ? 1 : 0,
                reversed ? correctionDelay : 0.0,
                activeLawWelfare,
                lowSupportActiveLawShare
        );
    }

    public static OutcomeSignals alternatives(
            int alternativesConsidered,
            boolean statusQuoWon,
            double selectedAlternativeMedianDistance,
            double proposerAgendaAdvantage
    ) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                1,
                alternativesConsidered,
                statusQuoWon ? 1 : 0,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals citizenReview(boolean certified, double legitimacy) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                1,
                certified ? 1 : 0,
                legitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals objectionWindow(boolean reversal) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                1,
                reversal ? 1 : 0,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals route(String lane) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                "fast".equals(lane) ? 1 : 0,
                "middle".equals(lane) ? 1 : 0,
                "high".equals(lane) ? 1 : 0,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals challengeDiagnostics(boolean tokenExhausted, boolean falseNegativePass) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                tokenExhausted ? 1 : 0,
                falseNegativePass ? 1 : 0,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals publicWill(double publicSignalMovement, double districtAlignment) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                1,
                publicSignalMovement,
                districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals cosponsorship(
            boolean admitted,
            boolean affectedGroupSponsor,
            int cosponsorCount
    ) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                1,
                admitted ? 1 : 0,
                affectedGroupSponsor ? 1 : 0,
                cosponsorCount,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals proposalBond(double forfeiture) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                1,
                forfeiture,
                base.strategicAlternativeRounds,
                base.strategicDecoys
        );
    }

    public static OutcomeSignals strategicAlternatives(int decoys) {
        OutcomeSignals base = zero();
        return new OutcomeSignals(
                base.lawReviews,
                base.lawReversals,
                base.lawRenewals,
                base.lawCorrections,
                base.correctionDelay,
                base.activeLawWelfare,
                base.lowSupportActiveLawShare,
                base.alternativeRounds,
                base.alternativesConsidered,
                base.statusQuoWins,
                base.selectedAlternativeMedianDistance,
                base.proposerAgendaAdvantage,
                base.citizenReviews,
                base.citizenCertifications,
                base.citizenLegitimacy,
                base.objectionWindows,
                base.repealWindowReversals,
                base.fastLaneRoutes,
                base.middleLaneRoutes,
                base.highRiskRoutes,
                base.challengeTokenExhaustions,
                base.falseNegativePasses,
                base.publicWillReviews,
                base.publicSignalMovement,
                base.districtAlignment,
                base.cosponsorshipReviews,
                base.crossBlocAdmissions,
                base.affectedGroupSponsors,
                base.totalCosponsors,
                base.proposalBondReviews,
                base.proposalBondForfeiture,
                1,
                decoys
        );
    }

    private static OutcomeSignals zero() {
        return new OutcomeSignals(
                0, 0, 0, 0, 0.0, 0.0, 0.0,
                0, 0, 0, 0.0, 0.0,
                0, 0, 0.0,
                0, 0,
                0, 0, 0, 0, 0,
                0, 0.0, 0.0,
                0, 0, 0, 0,
                0, 0.0,
                0, 0
        );
    }

    private static OutcomeSignals zero(
            int lawReversals,
            int lawRenewals,
            int lawCorrections,
            double correctionDelay,
            double activeLawWelfare,
            double lowSupportActiveLawShare
    ) {
        return new OutcomeSignals(
                1, lawReversals, lawRenewals, lawCorrections, correctionDelay, activeLawWelfare, lowSupportActiveLawShare,
                0, 0, 0, 0.0, 0.0,
                0, 0, 0.0,
                0, 0,
                0, 0, 0, 0, 0,
                0, 0.0, 0.0,
                0, 0, 0, 0,
                0, 0.0,
                0, 0
        );
    }
}
