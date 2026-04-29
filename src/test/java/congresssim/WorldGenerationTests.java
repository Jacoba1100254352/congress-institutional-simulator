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
import congresssim.calibration.CalibrationTarget;
import congresssim.calibration.CalibrationTargetCatalog;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Map;
import java.util.List;
import java.util.Random;
import java.util.Set;

import static congresssim.TestSupport.*;
final class WorldGenerationTests {
    private WorldGenerationTests() {
    }

    static void run() {
        committeeCompositionPresetsSelectDifferentMembers();
        partySystemProfilesRepresentMajorAndMinorParties();
        partySystemProfilesKeepIdeologicalOrdering();
        modelValidationRejectsInvalidInputs();
        worldGenerationIsDeterministicAndBounded();
        calibrationTargetCatalogDocumentsExternalValidationWork();
    }


    private static void committeeCompositionPresetsSelectDifferentMembers() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "A", -0.9, 0.1, 0.5, 0.2, 0.1, 0.2),
                new Legislator("L-2", "A", -0.4, 0.2, 0.5, 0.2, 0.2, 0.2),
                new Legislator("L-3", "B", 0.0, 1.0, 0.5, 1.0, 0.0, 1.0),
                new Legislator("L-4", "B", 0.4, 0.4, 0.5, 0.4, 0.8, 0.4),
                new Legislator("L-5", "B", 0.9, 0.3, 0.5, 0.3, 1.0, 0.3)
        );

        List<Legislator> expert = CommitteeFactory.select(legislators, CommitteeComposition.EXPERT, 2);
        List<Legislator> captured = CommitteeFactory.select(legislators, CommitteeComposition.CAPTURED, 2);

        assertTrue(expert.stream().anyMatch(legislator -> legislator.id().equals("L-3")), "Expert committee should select public-interest members.");
        assertTrue(captured.stream().anyMatch(legislator -> legislator.id().equals("L-5")), "Captured committee should select lobby-sensitive members.");
    }


    private static void partySystemProfilesRepresentMajorAndMinorParties() {
        WorldSpec twoMajorWithMinors = new WorldSpec(
                101,
                4,
                5,
                0.70,
                0.65,
                0.45,
                0.60,
                0.50,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                0.40
        );
        SimulationWorld world = new WorldGenerator().generate(twoMajorWithMinors, 88L);
        Map<String, Long> counts = world.legislators()
                .stream()
                .collect(java.util.stream.Collectors.groupingBy(Legislator::party, java.util.stream.Collectors.counting()));
        long majorSeats = counts.getOrDefault("Major-Left", 0L) + counts.getOrDefault("Major-Right", 0L);

        assertTrue(counts.size() == 5, "Two-major-with-minors profile should represent all configured parties.");
        assertTrue(majorSeats > 65, "Two largest parties should hold most seats while minor parties remain present.");

        WorldSpec fragmented = new WorldSpec(
                101,
                4,
                7,
                0.60,
                0.55,
                0.45,
                0.60,
                0.60,
                PartySystemProfile.FRAGMENTED_MULTIPARTY,
                0.20
        );
        SimulationWorld fragmentedWorld = new WorldGenerator().generate(fragmented, 99L);
        long representedParties = fragmentedWorld.legislators()
                .stream()
                .map(Legislator::party)
                .distinct()
                .count();
        assertTrue(representedParties == 7, "Fragmented multiparty profile should keep each party represented.");
    }


    private static void partySystemProfilesKeepIdeologicalOrdering() {
        WorldSpec twoMajorWithMinors = new WorldSpec(
                101,
                4,
                5,
                0.70,
                0.65,
                0.45,
                0.60,
                0.50,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                0.40
        );
        SimulationWorld world = new WorldGenerator().generate(twoMajorWithMinors, 2026L);
        Map<String, Double> partyPositions = world.partyPositions();

        assertTrue(
                partyPositions.get("Major-Left") < partyPositions.get("Center-Minor"),
                "Major-left parties should be ideologically left of the center minor party."
        );
        assertTrue(
                partyPositions.get("Center-Minor") < partyPositions.get("Major-Right"),
                "Center minor parties should be ideologically left of the major-right party."
        );

        WorldSpec dominant = new WorldSpec(
                101,
                4,
                4,
                0.66,
                0.70,
                0.48,
                0.62,
                0.48,
                PartySystemProfile.DOMINANT_PARTY,
                0.15
        );
        SimulationWorld dominantWorld = new WorldGenerator().generate(dominant, 2027L);
        long dominantSeats = dominantWorld.legislators()
                .stream()
                .filter(legislator -> legislator.party().equals("Dominant-Center"))
                .count();
        assertTrue(dominantSeats > 45, "Dominant-party profile should create a large center party.");
        assertTrue(
                Math.abs(dominantWorld.partyPositions().get("Dominant-Center")) < 0.45,
                "Dominant-party profile should keep the dominant party near the ideological center."
        );
    }


    private static void modelValidationRejectsInvalidInputs() {
        assertThrows(
                () -> new WorldSpec(0, 4, 2, 0.50, 0.50, 0.50, 0.50, 0.50),
                "WorldSpec should reject nonpositive legislature sizes."
        );
        assertThrows(
                () -> new WorldSpec(10, 4, 2, 1.50, 0.50, 0.50, 0.50, 0.50),
                "WorldSpec should reject out-of-range polarization."
        );
        assertThrows(
                () -> new Bill("B-invalid", "Invalid Bill", "L-1", 0.0, 1.2, 0.5, 0.5, 0.0, 0.5),
                "Bill should reject out-of-range ideology positions."
        );
        assertThrows(
                () -> new LobbyGroup(
                        "G-invalid",
                        "energy",
                        Map.of("energy", 1.2),
                        0.0,
                        1.0,
                        0.5,
                        1.0,
                        0.5,
                        0.5,
                        LobbyCaptureStrategy.BALANCED,
                        0.5
                ),
                "LobbyGroup should reject out-of-range issue preferences."
        );
    }


    private static void worldGenerationIsDeterministicAndBounded() {
        WorldSpec spec = new WorldSpec(
                61,
                20,
                5,
                0.72,
                0.66,
                0.48,
                0.64,
                0.55,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                0.40
        );
        WorldGenerator generator = new WorldGenerator();
        SimulationWorld first = generator.generate(spec, 4242L);
        SimulationWorld second = generator.generate(spec, 4242L);

        assertTrue(first.equals(second), "World generation should be deterministic for a fixed seed.");
        assertTrue(first.legislators().size() == spec.legislatorCount(), "World should contain the requested number of legislators.");
        assertTrue(first.bills().size() == spec.billCount(), "World should contain the requested number of bills.");
        assertTrue(first.lobbyGroups().size() >= spec.partyCount(), "World should include explicit lobby actors.");
        assertRatio((first.initialPolicy().position() + 1.0) / 2.0, "Initial policy should be inside [-1, 1].");

        Set<String> legislatorIds = new HashSet<>();
        for (Legislator legislator : first.legislators()) {
            assertTrue(legislatorIds.add(legislator.id()), "Generated legislator IDs should be unique.");
            assertRatio((legislator.ideology() + 1.0) / 2.0, "Legislator ideology should be inside [-1, 1].");
            assertRatio(legislator.compromisePreference(), "Compromise preference should be a ratio.");
            assertRatio(legislator.partyLoyalty(), "Party loyalty should be a ratio.");
            assertRatio(legislator.constituencySensitivity(), "Constituency sensitivity should be a ratio.");
            assertRatio(legislator.lobbySensitivity(), "Lobby sensitivity should be a ratio.");
            assertRatio(legislator.districtIntensity(), "District intensity should be a ratio.");
        }

        Set<String> billIds = new HashSet<>();
        for (Bill bill : first.bills()) {
            assertTrue(billIds.add(bill.id()), "Generated bill IDs should be unique.");
            assertTrue(legislatorIds.contains(bill.proposerId()), "Each generated bill should have a real proposer.");
            assertRatio((bill.ideologyPosition() + 1.0) / 2.0, "Bill ideology should be inside [-1, 1].");
            assertRatio(bill.publicSupport(), "Bill public support should be a ratio.");
            assertRatio(bill.publicBenefit(), "Bill public benefit should be a ratio.");
            assertRatio((bill.lobbyPressure() + 1.0) / 2.0, "Bill lobby pressure should be inside [-1, 1].");
            assertRatio(bill.salience(), "Bill salience should be a ratio.");
            assertRatio(bill.privateGain(), "Bill private gain should be a ratio.");
            assertRatio(bill.affectedGroupSupport(), "Affected-group support should be a ratio.");
            assertRatio(bill.concentratedHarm(), "Concentrated harm should be a ratio.");
            assertRatio(bill.compensationCost(), "Compensation cost should be a ratio.");
            assertRatio(bill.publicBenefitUncertainty(), "Public-benefit uncertainty should be a ratio.");
        }
    }

    private static void calibrationTargetCatalogDocumentsExternalValidationWork() {
        List<CalibrationTarget> targets = CalibrationTargetCatalog.standardTargets();
        Set<String> keys = new HashSet<>();

        assertTrue(targets.size() >= 6, "Calibration catalog should cover the major external validation targets.");
        for (CalibrationTarget target : targets) {
            assertTrue(keys.add(target.key()), "Calibration target keys should be unique.");
            assertTrue(!target.empiricalDataset().isBlank(), "Calibration targets should name an empirical dataset.");
            assertTrue(!target.simulatorMetric().isBlank(), "Calibration targets should name simulator metrics.");
            assertTrue(!target.validationUse().isBlank(), "Calibration targets should explain how they will be used.");
        }
    }

}
