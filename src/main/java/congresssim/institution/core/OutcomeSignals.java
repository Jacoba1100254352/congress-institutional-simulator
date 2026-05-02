package congresssim.institution.core;

import java.util.HashMap;
import java.util.Map;

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
        int strategicDecoys,
        double routingDelayCost,
        int shuttleAgreements,
        int shuttleRounds,
        int suspensiveOverrides,
        int bicameralDeadlocks,
        int committeePowerReviews,
        int committeeDischarges,
        int committeeHearings,
        double committeeQueueDelay,
        double committeeAmendmentValue,
        int chamberArchitectureReviews,
        double populationSeatDistortion,
        double democraticResponsiveness,
        double seatVoteDistortion,
        double constituencyServiceConcentration,
        double regionalTransferBias,
        Map<String, Double> supplementalMetrics
) {
    public OutcomeSignals {
        supplementalMetrics = Map.copyOf(supplementalMetrics);
    }

    public static OutcomeSignals none() {
        return zero();
    }

    public OutcomeSignals plus(OutcomeSignals other) {
        Map<String, Double> mergedSupplemental = new HashMap<>(supplementalMetrics);
        for (Map.Entry<String, Double> entry : other.supplementalMetrics.entrySet()) {
            mergedSupplemental.merge(entry.getKey(), entry.getValue(), Double::sum);
        }
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
                strategicDecoys + other.strategicDecoys,
                routingDelayCost + other.routingDelayCost,
                shuttleAgreements + other.shuttleAgreements,
                shuttleRounds + other.shuttleRounds,
                suspensiveOverrides + other.suspensiveOverrides,
                bicameralDeadlocks + other.bicameralDeadlocks,
                committeePowerReviews + other.committeePowerReviews,
                committeeDischarges + other.committeeDischarges,
                committeeHearings + other.committeeHearings,
                committeeQueueDelay + other.committeeQueueDelay,
                committeeAmendmentValue + other.committeeAmendmentValue,
                chamberArchitectureReviews + other.chamberArchitectureReviews,
                populationSeatDistortion + other.populationSeatDistortion,
                democraticResponsiveness + other.democraticResponsiveness,
                seatVoteDistortion + other.seatVoteDistortion,
                constituencyServiceConcentration + other.constituencyServiceConcentration,
                regionalTransferBias + other.regionalTransferBias,
                mergedSupplemental
        );
    }

    public static OutcomeSignals lawReview(
            boolean reversed,
            boolean renewed,
            double activeLawWelfare,
            double lowSupportActiveLawShare,
            double correctionDelay
    ) {
        OutcomeSignals signal = zero();
        return signal.withLawReview(reversed, renewed, activeLawWelfare, lowSupportActiveLawShare, correctionDelay);
    }

    public static OutcomeSignals alternatives(
            int alternativesConsidered,
            boolean statusQuoWon,
            double selectedAlternativeMedianDistance,
            double proposerAgendaAdvantage
    ) {
        OutcomeSignals signal = zero();
        return signal.withAlternatives(
                alternativesConsidered,
                statusQuoWon,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage
        );
    }

    public static OutcomeSignals citizenReview(boolean certified, double legitimacy) {
        OutcomeSignals signal = zero();
        return signal.withCitizenReview(certified, legitimacy);
    }

    public static OutcomeSignals objectionWindow(boolean reversal) {
        OutcomeSignals signal = zero();
        return signal.withObjectionWindow(reversal);
    }

    public static OutcomeSignals route(String lane) {
        OutcomeSignals signal = zero();
        return signal.withRoute(lane);
    }

    public static OutcomeSignals challengeDiagnostics(boolean tokenExhausted, boolean falseNegativePass) {
        OutcomeSignals signal = zero();
        return signal.withChallengeDiagnostics(tokenExhausted, falseNegativePass);
    }

    public static OutcomeSignals publicWill(double publicSignalMovement, double districtAlignment) {
        OutcomeSignals signal = zero();
        return signal.withPublicWill(publicSignalMovement, districtAlignment);
    }

    public static OutcomeSignals cosponsorship(
            boolean admitted,
            boolean affectedGroupSponsor,
            int cosponsorCount
    ) {
        OutcomeSignals signal = zero();
        return signal.withCosponsorship(admitted, affectedGroupSponsor, cosponsorCount);
    }

    public static OutcomeSignals proposalBond(double forfeiture) {
        OutcomeSignals signal = zero();
        return signal.withProposalBond(forfeiture);
    }

    public static OutcomeSignals strategicAlternatives(int decoys) {
        OutcomeSignals signal = zero();
        return signal.withStrategicAlternatives(decoys);
    }

    public static OutcomeSignals bicameralRouting(
            double routingDelayCost,
            int shuttleRounds,
            boolean shuttleAgreement,
            boolean suspensiveOverride,
            boolean deadlock
    ) {
        OutcomeSignals signal = zero();
        return signal.withBicameralRouting(
                routingDelayCost,
                shuttleRounds,
                shuttleAgreement,
                suspensiveOverride,
                deadlock
        );
    }

    public static OutcomeSignals committeePower(
            boolean discharged,
            boolean hearing,
            double queueDelay,
            double amendmentValue
    ) {
        OutcomeSignals signal = zero();
        return signal.withCommitteePower(discharged, hearing, queueDelay, amendmentValue);
    }

    public static OutcomeSignals chamberArchitecture(
            double populationSeatDistortion,
            double democraticResponsiveness,
            double seatVoteDistortion,
            double constituencyServiceConcentration,
            double regionalTransferBias
    ) {
        OutcomeSignals signal = zero();
        return signal.withChamberArchitecture(
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias
        );
    }

    public static OutcomeSignals diagnostic(String key, double value) {
        return diagnostics(Map.of(key, value));
    }

    public static OutcomeSignals diagnostics(Map<String, Double> metrics) {
        OutcomeSignals signal = zero();
        return signal.withSupplementalMetrics(metrics);
    }

    private OutcomeSignals withLawReview(
            boolean reversed,
            boolean renewed,
            double activeLawWelfare,
            double lowSupportActiveLawShare,
            double correctionDelay
    ) {
        return copy(
                1,
                reversed ? 1 : 0,
                renewed ? 1 : 0,
                reversed ? 1 : 0,
                reversed ? correctionDelay : 0.0,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withAlternatives(
            int alternativesConsidered,
            boolean statusQuoWon,
            double selectedAlternativeMedianDistance,
            double proposerAgendaAdvantage
    ) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                1,
                alternativesConsidered,
                statusQuoWon ? 1 : 0,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withCitizenReview(boolean certified, double legitimacy) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                1,
                certified ? 1 : 0,
                legitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withObjectionWindow(boolean reversal) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                1,
                reversal ? 1 : 0,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withRoute(String lane) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                "fast".equals(lane) ? 1 : 0,
                "middle".equals(lane) ? 1 : 0,
                "high".equals(lane) ? 1 : 0,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withChallengeDiagnostics(boolean tokenExhausted, boolean falseNegativePass) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                tokenExhausted ? 1 : 0,
                falseNegativePass ? 1 : 0,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withPublicWill(double publicSignalMovement, double districtAlignment) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                1,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withCosponsorship(
            boolean admitted,
            boolean affectedGroupSponsor,
            int cosponsorCount
    ) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                1,
                admitted ? 1 : 0,
                affectedGroupSponsor ? 1 : 0,
                cosponsorCount,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withProposalBond(double forfeiture) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                1,
                forfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withStrategicAlternatives(int decoys) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                1,
                decoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withBicameralRouting(
            double routingDelayCost,
            int shuttleRounds,
            boolean shuttleAgreement,
            boolean suspensiveOverride,
            boolean deadlock
    ) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreement ? 1 : 0,
                shuttleRounds,
                suspensiveOverride ? 1 : 0,
                deadlock ? 1 : 0,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withCommitteePower(
            boolean discharged,
            boolean hearing,
            double queueDelay,
            double amendmentValue
    ) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                1,
                discharged ? 1 : 0,
                hearing ? 1 : 0,
                queueDelay,
                amendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withChamberArchitecture(
            double populationSeatDistortion,
            double democraticResponsiveness,
            double seatVoteDistortion,
            double constituencyServiceConcentration,
            double regionalTransferBias
    ) {
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                1,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }

    private OutcomeSignals withSupplementalMetrics(Map<String, Double> metrics) {
        Map<String, Double> merged = new HashMap<>(supplementalMetrics);
        for (Map.Entry<String, Double> entry : metrics.entrySet()) {
            if (entry.getKey() == null || entry.getKey().isBlank()) {
                throw new IllegalArgumentException("supplemental metric key must not be blank.");
            }
            double value = entry.getValue() == null ? 0.0 : entry.getValue();
            if (!Double.isFinite(value)) {
                throw new IllegalArgumentException("supplemental metric value must be finite.");
            }
            merged.merge(entry.getKey(), value, Double::sum);
        }
        return copy(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                merged
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
                0, 0,
                0.0, 0, 0, 0, 0,
                0, 0, 0, 0.0, 0.0,
                0, 0.0, 0.0, 0.0, 0.0, 0.0,
                Map.of()
        );
    }

    private OutcomeSignals copy(
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
            int strategicDecoys,
            double routingDelayCost,
            int shuttleAgreements,
            int shuttleRounds,
            int suspensiveOverrides,
            int bicameralDeadlocks,
            int committeePowerReviews,
            int committeeDischarges,
            int committeeHearings,
            double committeeQueueDelay,
            double committeeAmendmentValue,
            int chamberArchitectureReviews,
            double populationSeatDistortion,
            double democraticResponsiveness,
            double seatVoteDistortion,
            double constituencyServiceConcentration,
            double regionalTransferBias,
            Map<String, Double> supplementalMetrics
    ) {
        return new OutcomeSignals(
                lawReviews,
                lawReversals,
                lawRenewals,
                lawCorrections,
                correctionDelay,
                activeLawWelfare,
                lowSupportActiveLawShare,
                alternativeRounds,
                alternativesConsidered,
                statusQuoWins,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                citizenReviews,
                citizenCertifications,
                citizenLegitimacy,
                objectionWindows,
                repealWindowReversals,
                fastLaneRoutes,
                middleLaneRoutes,
                highRiskRoutes,
                challengeTokenExhaustions,
                falseNegativePasses,
                publicWillReviews,
                publicSignalMovement,
                districtAlignment,
                cosponsorshipReviews,
                crossBlocAdmissions,
                affectedGroupSponsors,
                totalCosponsors,
                proposalBondReviews,
                proposalBondForfeiture,
                strategicAlternativeRounds,
                strategicDecoys,
                routingDelayCost,
                shuttleAgreements,
                shuttleRounds,
                suspensiveOverrides,
                bicameralDeadlocks,
                committeePowerReviews,
                committeeDischarges,
                committeeHearings,
                committeeQueueDelay,
                committeeAmendmentValue,
                chamberArchitectureReviews,
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias,
                supplementalMetrics
        );
    }
}
