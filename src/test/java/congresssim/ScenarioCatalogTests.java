package congresssim;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.experiment.CampaignResult;
import congresssim.experiment.CampaignRunner;
import congresssim.experiment.CampaignRow;
import congresssim.institution.AdaptiveTrackProcess;
import congresssim.institution.AffirmativeThresholdRule;
import congresssim.institution.AgendaDisposition;
import congresssim.institution.AgendaLotteryProcess;
import congresssim.institution.AlternativeSelectionRule;
import congresssim.institution.AmendmentMediationProcess;
import congresssim.institution.BillOutcome;
import congresssim.institution.BudgetedLobbyingProcess;
import congresssim.institution.Chamber;
import congresssim.institution.ChallengeEscalationProcess;
import congresssim.institution.ChallengeTokenAllocation;
import congresssim.institution.ChallengeVoucherProcess;
import congresssim.institution.CitizenPanelMode;
import congresssim.institution.CitizenPanelReviewProcess;
import congresssim.institution.CoalitionCosponsorshipProcess;
import congresssim.institution.CommitteeGatekeepingProcess;
import congresssim.institution.CommitteeInformationProcess;
import congresssim.institution.CompetingAlternativesProcess;
import congresssim.institution.ConstituentPublicWillProcess;
import congresssim.institution.DefaultPassUnlessVetoedRule;
import congresssim.institution.DistributionalHarmProcess;
import congresssim.institution.LawRegistryProcess;
import congresssim.institution.LegislativeProcess;
import congresssim.institution.LobbyAuditProcess;
import congresssim.institution.LobbyTransparencyProcess;
import congresssim.institution.MultiRoundAmendmentProcess;
import congresssim.institution.ProposalAccessRules;
import congresssim.institution.ProposalBondProcess;
import congresssim.institution.ProposalCreditProcess;
import congresssim.institution.PublicObjectionWindowProcess;
import congresssim.institution.QuadraticAttentionBudgetProcess;
import congresssim.institution.SunsetTrialProcess;
import congresssim.simulation.CommitteeComposition;
import congresssim.simulation.CommitteeFactory;
import congresssim.simulation.PartySystemProfile;
import congresssim.simulation.Scenario;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldGenerator;
import congresssim.simulation.WorldSpec;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.LobbyCaptureStrategy;
import congresssim.model.LobbyGroup;
import congresssim.model.SimulationWorld;
import congresssim.model.Vote;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Map;
import java.util.List;
import java.util.Random;
import java.util.Set;

import static congresssim.TestSupport.*;
final class ScenarioCatalogTests {
    private ScenarioCatalogTests() {
    }

    static void run() {
        scenarioKeysSelectExpectedScenarios();
        scenarioCatalogHasUniqueKeysAndRunnableNames();
    }


    private static void scenarioKeysSelectExpectedScenarios() {
        assertTrue(
                ScenarioCatalog.scenariosForKeys(List.of("default-pass", "default-pass-guarded")).size() == 2,
                "Scenario keys should select a focused scenario subset."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-challenge"),
                "Scenario catalog should expose CLI-facing keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-escalation-q12-s082"),
                "Scenario catalog should expose tokenless escalation sweep keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-cross-bloc"),
                "Scenario catalog should expose cross-bloc cosponsorship keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-adaptive-track"),
                "Scenario catalog should expose adaptive-track keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-sunset-trial"),
                "Scenario catalog should expose sunset-trial keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-earned-credits"),
                "Scenario catalog should expose earned proposal-credit keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-anti-capture-bundle"),
                "Scenario catalog should expose anti-capture scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-budgeted-lobbying"),
                "Scenario catalog should expose budgeted-lobbying scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-mediation"),
                "Scenario catalog should expose mediation scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-budgeted-lobbying-mediation"),
                "Scenario catalog should expose budgeted lobbying plus mediation scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-alternatives-pairwise"),
                "Scenario catalog should expose competing-alternatives scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-lobby-channel-bundle"),
                "Scenario catalog should expose lobbying-channel scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-citizen-certificate"),
                "Scenario catalog should expose citizen-panel scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-weighted-agenda-lottery"),
                "Scenario catalog should expose agenda-lottery scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-quadratic-attention"),
                "Scenario catalog should expose quadratic attention scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-public-objection"),
                "Scenario catalog should expose public-objection scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-constituent-public-will"),
                "Scenario catalog should expose constituent-public-will scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-proposal-bonds"),
                "Scenario catalog should expose proposal-bond scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-multiround-mediation"),
                "Scenario catalog should expose multi-round mediation scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-alternatives-strategic"),
                "Scenario catalog should expose strategic-alternative scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-adaptive-proposers"),
                "Scenario catalog should expose adaptive proposer scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-strategic-lobbying"),
                "Scenario catalog should expose strategic lobbying scenario keys."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("current-system"),
                "Scenario catalog should expose the current-system benchmark key."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("committee-regular-order"),
                "Scenario catalog should expose non-default committee-first designs."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("parliamentary-coalition-confidence"),
                "Scenario catalog should expose non-default coalition-confidence designs."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("simple-majority-alternatives-strategic"),
                "Scenario catalog should expose non-default strategic policy tournaments."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("risk-routed-majority"),
                "Scenario catalog should expose non-default adaptive routing designs."
        );
        assertTrue(
                ScenarioCatalog.scenarioKeys().contains("default-pass-challenge-minority-bonus"),
                "Scenario catalog should expose challenge allocation variant keys."
        );
    }


    private static void scenarioCatalogHasUniqueKeysAndRunnableNames() {
        List<String> keys = ScenarioCatalog.scenarioKeys();
        assertTrue(keys.size() == new HashSet<>(keys).size(), "Scenario keys should be unique.");
        assertTrue(
                ScenarioCatalog.defaultScenarios().size() == ScenarioCatalog.defaultScenarioKeys().size(),
                "Default scenario list should match the default key list."
        );
        assertTrue(
                ScenarioCatalog.defaultScenarioKeys().size() < keys.size(),
                "Default scenario list should be a representative breadth-first set, not the full historical catalog."
        );
        long defaultPassCount = ScenarioCatalog.defaultScenarioKeys().stream()
                .filter(key -> key.startsWith("default-pass"))
                .count();
        assertTrue(
                defaultPassCount <= 3,
                "Default scenario list should keep default-pass as a small side family."
        );

        Set<String> scenarioNames = new HashSet<>();
        for (Scenario scenario : ScenarioCatalog.defaultScenarios()) {
            assertTrue(scenario.name() != null && !scenario.name().isBlank(), "Every scenario should expose a nonblank name.");
            assertTrue(scenarioNames.add(scenario.name()), "Scenario display names should be unique for reports.");
        }

        assertThrows(
                () -> ScenarioCatalog.scenariosForKeys(List.of("missing-scenario-key")),
                "Unknown scenario keys should fail fast instead of silently changing campaign composition."
        );
    }

}
