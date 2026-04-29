package congresssim.experiment;

import congresssim.simulation.ScenarioReport;

public record CampaignRow(
        String caseKey,
        String caseName,
        String caseDescription,
        String scenarioKey,
        ScenarioReport report
) {
}

