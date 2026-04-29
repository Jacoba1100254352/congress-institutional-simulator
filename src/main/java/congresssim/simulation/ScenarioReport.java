package congresssim.simulation;

public record ScenarioReport(
        String scenarioName,
        int totalBills,
        int enactedBills,
        double productivity,
        double averageEnactedSupport,
        double cooperationScore,
        double compromiseScore,
        double gridlockRate,
        double controversialPassageRate,
        double popularBillFailureRate,
        double averagePolicyShift,
        double averageProposerGain,
        int vetoes,
        int overriddenVetoes
) {
}
