package congresssim.simulation;

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
        double floorConsiderationRate,
        double accessDenialRate,
        double committeeRejectionRate,
        double challengeRate,
        int vetoes,
        int overriddenVetoes
) {
    private static final double POLICY_DISTANCE_MAX = 2.0;

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
                MetricDefinition.lowerIsBetter(minorityHarmIndex),
                MetricDefinition.lowerIsBetter(lobbyCaptureIndex),
                MetricDefinition.lowerIsBetter(publicPreferenceDistortion),
                MetricDefinition.lowerIsBetter(concentratedHarmPassageRate),
                MetricDefinition.lowerIsBetter(averageProposerGain, POLICY_DISTANCE_MAX),
                MetricDefinition.lowerIsBetter(averagePolicyShift, POLICY_DISTANCE_MAX)
        );
    }

    public double directionalScore() {
        return MetricDefinition.average(
                productivity,
                representativeQualityScore(),
                riskControlScore()
        );
    }
}
