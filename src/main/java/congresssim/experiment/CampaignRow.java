package congresssim.experiment;

import congresssim.simulation.ScenarioReport;

public record CampaignRow(
        String caseKey,
        String caseName,
        String caseDescription,
        double caseWeight,
        String scenarioKey,
        ScenarioReport report
) {
}
