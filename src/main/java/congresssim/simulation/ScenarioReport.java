package congresssim.simulation;

import java.util.List;
import java.util.Map;

public record ScenarioReport(
        String scenarioName,
        int totalBills,
        int enactedBills,
        double productivity,
        double averageEnactedSupport,
        double averagePublicBenefit,
        double cooperationScore,
        double compromiseScore,
        double gridlockRate,
        double controversialPassageRate,
        double popularBillFailureRate,
        double averagePolicyShift,
        double averageProposerGain,
        double lobbyCaptureIndex,
        double publicAlignmentScore,
        double antiLobbyingSuccessRate,
        double privateGainRatio,
        double lobbySpendPerBill,
        double defensiveLobbyingShare,
        double captureReturnOnSpend,
        double publicPreferenceDistortion,
        double weakPublicMandatePassageRate,
        double amendmentRate,
        double averageAmendmentMovement,
        double minorityHarmIndex,
        double concentratedHarmPassageRate,
        double compensationRate,
        double legitimacyScore,
        double activeLawWelfare,
        double reversalRate,
        double timeToCorrectBadLaw,
        double statusQuoVolatility,
        double lowSupportActiveLawShare,
        double selectedAlternativeMedianDistance,
        double proposerAgendaAdvantage,
        double alternativeDiversity,
        double statusQuoWinRate,
        double publicBenefitPerLobbyDollar,
        double directLobbySpendShare,
        double agendaLobbySpendShare,
        double informationLobbySpendShare,
        double publicCampaignSpendShare,
        double litigationThreatSpendShare,
        double citizenReviewRate,
        double citizenCertificationRate,
        double citizenLegitimacy,
        double attentionSpendPerBill,
        double objectionWindowRate,
        double repealWindowReversalRate,
        double fastLaneRate,
        double middleLaneRate,
        double highRiskLaneRate,
        double challengeExhaustionRate,
        double falseNegativePassRate,
        double publicWillReviewRate,
        double publicSignalMovement,
        double districtAlignment,
        double crossBlocAdmissionRate,
        double affectedGroupSponsorshipRate,
        double averageCosponsors,
        double proposalBondForfeiture,
        double strategicDecoyRate,
        double proposerAccessGini,
        double welfarePerSubmittedBill,
        double administrativeCostIndex,
        double floorConsiderationRate,
        double accessDenialRate,
        double committeeRejectionRate,
        double challengeRate,
        int vetoes,
        int overriddenVetoes,
        double interChamberConflictRate,
        double secondChamberKillRate,
        double conferenceRate,
        double conferenceSuccessRate,
        double routingDelayCost,
        double shuttleRoundsToAgreement,
        double suspensiveOverrideRate,
        double bicameralDeadlockRate,
        double dischargePetitionRate,
        double committeeOverrideRate,
        double committeeHearingRate,
        double committeeQueueDelay,
        double committeeAmendmentValueAdded,
        double populationSeatDistortion,
        double democraticResponsiveness,
        double seatVoteDistortion,
        double constituencyServiceConcentration,
        double regionalTransferBias,
        Map<String, Double> supplementalMetrics
) {
    private static final double POLICY_DISTANCE_MAX = 2.0;
    public static final List<String> SUPPLEMENTAL_METRIC_KEYS = List.of(
            "malapportionmentIndex",
            "smallConstituencyVetoRate",
            "populationSupportedButBlockedRate",
            "firstMoverWinRate",
            "amendmentSurvivalRate",
            "mediatorAddedTextShare",
            "upperHouseAmendmentRetentionRate",
            "suspensiveDelayUseRate",
            "committeeAgendaConcentration",
            "committeeCaptureIndex",
            "committeeExpertiseScore",
            "minorityCommitteeAccessRate",
            "committeeFalsePositiveRate",
            "committeeFalseNegativeRate",
            "reportedBillSponsorDiversity",
            "oppositionAmendmentSuccessRate",
            "hearingDiversity",
            "auditFollowThroughRate",
            "scandalDetectionRate",
            "appointmentCaptureRisk",
            "eligibilityExclusionRate",
            "expertiseRepresentationGap",
            "constituencyAccountability",
            "selectorCaptureIndex",
            "legislatorExperienceStock",
            "electoralResponsiveness",
            "turnoverOutsideInfluenceShift",
            "candidatePoolDiversity",
            "contestedSeatRate",
            "vacancyRate",
            "renewalStaggeringIndex",
            "nearTermRenewalShare",
            "recusalRate",
            "conflictDisclosureRate",
            "revolvingDoorTransitionRate",
            "sponsorIndustryAlignment",
            "exAnteReviewRate",
            "reviewDelay",
            "exPostInvalidationRate",
            "draftingErrorRate",
            "referralPartisanSkew",
            "forecastError",
            "publicationCompliance",
            "informationRequestFulfillment",
            "institutionOverrideFrequency",
            "oppositionTrustProxy",
            "independenceInsulationScore",
            "quietCaptureRisk"
    );

    public ScenarioReport {
        supplementalMetrics = Map.copyOf(supplementalMetrics);
    }

    public double supplementalMetric(String key) {
        return supplementalMetrics.getOrDefault(key, 0.0);
    }

    public double representativeQualityScore() {
        return MetricDefinition.average(
                averagePublicBenefit,
                averageEnactedSupport,
                compromiseScore,
                publicAlignmentScore,
                legitimacyScore
        );
    }

    public double riskControlScore() {
        return MetricDefinition.average(
                MetricDefinition.lowerIsBetter(controversialPassageRate),
                MetricDefinition.lowerIsBetter(weakPublicMandatePassageRate),
                MetricDefinition.lowerIsBetter(minorityHarmIndex),
                MetricDefinition.lowerIsBetter(lobbyCaptureIndex),
                MetricDefinition.lowerIsBetter(publicPreferenceDistortion),
                MetricDefinition.lowerIsBetter(concentratedHarmPassageRate),
                MetricDefinition.lowerIsBetter(averageProposerGain, POLICY_DISTANCE_MAX),
                MetricDefinition.lowerIsBetter(averagePolicyShift, POLICY_DISTANCE_MAX)
        );
    }

    public double administrativeFeasibilityScore() {
        return MetricDefinition.lowerIsBetter(administrativeCostIndex);
    }

    public double directionalScore() {
        return MetricDefinition.average(
                productivity,
                representativeQualityScore(),
                riskControlScore(),
                administrativeFeasibilityScore()
        );
    }
}
