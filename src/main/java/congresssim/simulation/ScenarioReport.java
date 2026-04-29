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
        double floorConsiderationRate,
        double accessDenialRate,
        double committeeRejectionRate,
        double challengeRate,
        int vetoes,
        int overriddenVetoes
) {
}
