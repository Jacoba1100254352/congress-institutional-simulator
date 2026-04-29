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
        double floorConsiderationRate,
        double accessDenialRate,
        double committeeRejectionRate,
        int vetoes,
        int overriddenVetoes
) {
}
