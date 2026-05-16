package congresssim;


public final class SimulatorTests
{
	private SimulatorTests() {
	}
	
	static void main(String[] args) {
		InstitutionProcessTests.run();
		WorldGenerationTests.run();
		ScenarioCatalogTests.run();
		CampaignRunnerTests.run();
		SimulatorInvariantTests.run();
		System.out.println("All simulator tests passed.");
	}
}
