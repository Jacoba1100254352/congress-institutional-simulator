package congresssim;

import congresssim.institution.chamber.Chamber;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.experiment.CampaignResult;
import congresssim.experiment.CampaignRunner;
import congresssim.experiment.CampaignRow;
import congresssim.simulation.CommitteeComposition;
import congresssim.simulation.CommitteeFactory;
import congresssim.simulation.CommitteeQuotaRule;
import congresssim.simulation.CommitteeSelectionConfig;
import congresssim.simulation.CommitteeSelectionResult;
import congresssim.simulation.ChairAllocationRule;
import congresssim.simulation.ChamberArchitectureMetrics;
import congresssim.simulation.ChamberFactory;
import congresssim.simulation.ChamberSpec;
import congresssim.simulation.PartySystemProfile;
import congresssim.simulation.RepresentationUnit;
import congresssim.simulation.Scenario;
import congresssim.simulation.catalog.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldGenerator;
import congresssim.simulation.WorldSpec;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.model.LobbyCaptureStrategy;
import congresssim.model.LobbyGroup;
import congresssim.model.RepresentationProfile;
import congresssim.model.SimulationWorld;
import congresssim.model.Vote;
import congresssim.calibration.CalibrationTarget;
import congresssim.calibration.CalibrationBenchmark;
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
        expandedCommitteeCompositionsSelectInstitutionallyDistinctMembers();
        configuredCommitteeSelectionPreservesCitizenAdvisoryWeights();
        chamberRepresentationMetricsDistinguishEqualAndTerritorialApportionment();
        generatedLegislatorsCarryRepresentationMetadata();
        chamberSelectionAnnotatesRepresentationMetadata();
        thresholdAndMagnitudeSweepsChangePartyRepresentation();
        chamberFactoryBuildsIncongruentChambers();
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

    private static void expandedCommitteeCompositionsSelectInstitutionallyDistinctMembers() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "A", -0.9, 0.2, 0.9, 0.3, 0.2, 0.4),
                new Legislator("L-2", "A", -0.5, 0.4, 0.8, 0.3, 0.3, 0.4),
                new Legislator("L-3", "A", -0.2, 0.7, 0.7, 0.5, 0.4, 0.6),
                new Legislator("L-4", "B", 0.0, 1.0, 0.2, 1.0, 0.0, 1.0),
                new Legislator("L-5", "B", 0.4, 0.7, 0.3, 0.7, 0.2, 0.8),
                new Legislator("L-6", "C", 0.8, 0.5, 0.4, 0.6, 0.1, 0.7)
        );

        List<Legislator> balanced = CommitteeFactory.select(legislators, CommitteeComposition.FORCED_PARTY_BALANCE, 3);
        Set<String> balancedParties = balanced.stream()
                .map(Legislator::party)
                .collect(java.util.stream.Collectors.toSet());
        assertTrue(balancedParties.size() >= 3, "Forced-balance committees should include available major/minor party blocs.");

        List<Legislator> opposition = CommitteeFactory.select(legislators, CommitteeComposition.OPPOSITION_CHAIRED, 3);
        assertTrue(!opposition.getFirst().party().equals("A"), "Opposition-chaired committees should put a non-majority member first as chair proxy.");

        List<Legislator> lotteryA = CommitteeFactory.select(legislators, CommitteeComposition.RANDOM_LOTTERY, 3);
        List<Legislator> lotteryB = CommitteeFactory.select(legislators, CommitteeComposition.RANDOM_LOTTERY, 3);
        assertTrue(lotteryA.equals(lotteryB), "Random-lottery committees should be deterministic for reproducible campaigns.");
    }

    private static void configuredCommitteeSelectionPreservesCitizenAdvisoryWeights() {
        List<Legislator> legislators = List.of(
                new Legislator("L-1", "A", -0.9, 0.2, 0.9, 0.3, 0.2, 0.4),
                new Legislator("L-2", "A", -0.5, 0.4, 0.8, 0.3, 0.3, 0.4),
                new Legislator("L-3", "A", -0.2, 0.7, 0.7, 0.5, 0.4, 0.6),
                new Legislator("L-4", "B", 0.0, 1.0, 0.2, 1.0, 0.0, 1.0),
                new Legislator("L-5", "B", 0.4, 0.7, 0.3, 0.7, 0.2, 0.8),
                new Legislator("L-6", "C", 0.8, 0.5, 0.4, 0.6, 0.1, 0.7)
        );
        CommitteeSelectionConfig config = new CommitteeSelectionConfig(
                "budget",
                44L,
                CommitteeQuotaRule.FORCED_BALANCE,
                0.42,
                0.34,
                0.12,
                2,
                ChairAllocationRule.EXPERT,
                0.50,
                0.40,
                true,
                4
        );
        CommitteeSelectionResult result = CommitteeFactory.select(legislators, config);

        assertTrue(result.members().size() == 4, "Configured committee selection should preserve target size.");
        assertTrue(result.topicReferralAuthority(), "Configured committees should preserve topic referral authority.");
        assertTrue(result.citizenAdvisoryWeight() == 0.40, "Mixed citizen committees should preserve citizen advisory weight.");
        assertTrue(result.legislatorVotingWeight() == 0.60, "Mixed citizen committees should retain complementary legislator vote weight.");
        assertTrue(result.quorumPartyBalance() == 0.50, "Configured committee selection should preserve quorum-balance rules.");
    }

    private static void chamberRepresentationMetricsDistinguishEqualAndTerritorialApportionment() {
        ChamberSpec lower = ChamberSpec.lowerHouse(24);
        ChamberSpec territorial = ChamberSpec.territorialUpperHouse(24, 0.85);
        List<RepresentationUnit> lowerUnits = ChamberFactory.representationUnits(lower);
        List<RepresentationUnit> territorialUnits = ChamberFactory.representationUnits(territorial);

        assertTrue(
                Math.abs(ChamberArchitectureMetrics.malapportionmentIndex(lowerUnits)) <= 0.000001,
                "Equal-population units should have no apportionment distortion."
        );
        assertTrue(
                ChamberArchitectureMetrics.malapportionmentIndex(territorialUnits) > 0.20,
                "Territorial upper chambers should expose malapportionment distortion."
        );
        assertTrue(
                ChamberArchitectureMetrics.perCitizenVotingPowerVariance(territorialUnits) > 0.0,
                "Territorial weighting should create per-citizen voting-power variance."
        );
        assertTrue(
                ChamberArchitectureMetrics.democraticResponsiveness(lowerUnits)
                        > ChamberArchitectureMetrics.democraticResponsiveness(territorialUnits),
                "Equal-population elected chambers should score as more democratically responsive than malapportioned chambers."
        );
        assertTrue(
                ChamberArchitectureMetrics.regionalTransferBias(territorialUnits) > 0.0,
                "Malapportioned territorial chambers should expose regional transfer bias."
        );
    }

    private static void generatedLegislatorsCarryRepresentationMetadata() {
        WorldSpec spec = new WorldSpec(
                33,
                5,
                4,
                0.62,
                0.58,
                0.35,
                0.60,
                0.55,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                1.0
        );
        SimulationWorld world = new WorldGenerator().generate(spec, 8844L);

        for (Legislator legislator : world.legislators()) {
            RepresentationProfile profile = legislator.representationProfile();
            assertTrue(profile.populationRepresented() > 0.0, "Generated legislators should carry population metadata.");
            assertTrue(profile.districtMagnitude() == 1, "Generated baseline legislators should carry district magnitude.");
            assertTrue(!profile.regionLabel().isBlank(), "Generated legislators should carry a region label.");
            assertTrue(!profile.selectionMode().isBlank(), "Generated legislators should carry selection-mode metadata.");
            assertTrue(profile.lowerHouseTermLength() > 0, "Generated legislators should carry lower-house term metadata.");
            assertTrue(profile.upperHouseTermLength() > 0, "Generated legislators should carry upper-house term metadata.");
            assertTrue(profile.renewalCycleLength() > 0, "Generated legislators should carry renewal-cycle metadata.");
            assertTrue(profile.nextRenewalRound() > 0, "Generated legislators should carry next-renewal metadata.");
        }
    }

    private static void chamberSelectionAnnotatesRepresentationMetadata() {
        WorldSpec spec = new WorldSpec(
                45,
                5,
                5,
                0.58,
                0.56,
                0.30,
                0.62,
                0.58,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                1.0
        );
        SimulationWorld world = new WorldGenerator().generate(spec, 9821L);
        ChamberSpec appointedSpec = ChamberSpec.appointedUpperHouse(15, 0.40);
        List<Legislator> appointedUpper = ChamberFactory.select(world.legislators(), appointedSpec, 9L);
        long appointedMembers = appointedUpper.stream()
                .filter(legislator -> legislator.representationProfile().appointed())
                .count();

        assertTrue(appointedUpper.size() == 15, "Chamber selection should preserve requested size.");
        assertTrue(appointedMembers > 0, "Mixed appointed chambers should annotate appointed members.");
        assertTrue(
                appointedUpper.stream().allMatch(legislator ->
                        legislator.representationProfile().chamberEligibility().equals(appointedSpec.name())),
                "Chamber-selected legislators should carry chamber-specific eligibility metadata."
        );
        assertTrue(
                ChamberArchitectureMetrics.appointedSeatShare(ChamberFactory.representationUnits(appointedSpec)) >= 0.35,
                "Partial-appointed chamber specs should expose appointed-seat share."
        );
        Map<Integer, Long> renewalCohorts = appointedUpper.stream()
                .collect(java.util.stream.Collectors.groupingBy(
                        legislator -> legislator.representationProfile().renewalCohort(),
                        java.util.stream.Collectors.counting()
                ));
        assertTrue(renewalCohorts.size() >= 2, "Staggered chambers should assign multiple renewal cohorts.");
        assertTrue(
                renewalCohorts.keySet().stream().allMatch(cohort -> cohort >= 0 && cohort < appointedSpec.renewalCohortCount()),
                "Renewal cohorts should stay within the chamber spec's configured range."
        );
        assertTrue(
                appointedUpper.stream().allMatch(legislator ->
                        legislator.representationProfile().nextRenewalRound()
                                <= legislator.representationProfile().renewalCycleLength()),
                "Next-renewal rounds should stay inside the configured renewal cycle."
        );
        assertTrue(
                appointedUpper.stream()
                        .map(legislator -> legislator.representationProfile().nextRenewalRound())
                        .distinct()
                        .count() >= 2,
                "Staggered chambers should expose multiple next-renewal rounds."
        );
    }

    private static void thresholdAndMagnitudeSweepsChangePartyRepresentation() {
        WorldSpec spec = new WorldSpec(
                121,
                5,
                7,
                0.58,
                0.56,
                0.30,
                0.62,
                0.58,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                1.0
        );
        SimulationWorld world = new WorldGenerator().generate(spec, 7722L);
        List<Legislator> lowMagnitude = ChamberFactory.select(
                world.legislators(),
                ChamberSpec.proportionalHouse(60, 2, 0.00),
                1L
        );
        List<Legislator> highMagnitude = ChamberFactory.select(
                world.legislators(),
                ChamberSpec.proportionalHouse(60, 12, 0.00),
                1L
        );
        List<Legislator> legalThreshold = ChamberFactory.select(
                world.legislators(),
                ChamberSpec.proportionalHouse(60, 12, 0.12),
                1L
        );

        assertTrue(
                ChamberArchitectureMetrics.effectivePartyCount(highMagnitude)
                        >= ChamberArchitectureMetrics.effectivePartyCount(lowMagnitude),
                "Larger district magnitude should not reduce effective party count in proportional allocation."
        );
        assertTrue(
                ChamberArchitectureMetrics.effectivePartyCount(legalThreshold)
                        <= ChamberArchitectureMetrics.effectivePartyCount(highMagnitude),
                "Higher legal thresholds should not increase effective party count."
        );
        assertTrue(
                ChamberArchitectureMetrics.seatVoteDistortion(world.legislators(), legalThreshold)
                        >= ChamberArchitectureMetrics.seatVoteDistortion(world.legislators(), highMagnitude),
                "Thresholds should not reduce seat-vote distortion in this controlled sweep."
        );
    }

    private static void chamberFactoryBuildsIncongruentChambers() {
        WorldSpec spec = new WorldSpec(
                101,
                6,
                5,
                0.62,
                0.58,
                0.35,
                0.60,
                0.55,
                PartySystemProfile.TWO_MAJOR_WITH_MINOR_PARTIES,
                1.0
        );
        SimulationWorld world = new WorldGenerator().generate(spec, 551L);
        List<Legislator> lower = ChamberFactory.select(world.legislators(), ChamberSpec.lowerHouse(101), 1L);
        List<Legislator> upper = ChamberFactory.select(
                world.legislators(),
                ChamberSpec.proportionalHouse(35, 7, 0.04),
                2L
        );

        assertTrue(lower.size() == 101, "Lower-house chamber spec should select the requested lower-house size.");
        assertTrue(upper.size() == 35, "Upper-house chamber spec should select the requested upper-house size.");
        assertTrue(
                ChamberArchitectureMetrics.chamberIncongruenceIndex(lower, upper) >= 0.0,
                "Chamber incongruence index should be computable for generated chambers."
        );
        assertTrue(
                upper.stream().map(Legislator::party).distinct().count() >= 2,
                "Proportional upper chambers should preserve multiparty representation in this generated profile."
        );
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
        List<CalibrationBenchmark> benchmarks = CalibrationTargetCatalog.benchmarkRanges();
        Set<String> keys = new HashSet<>();

        assertTrue(targets.size() >= 6, "Calibration catalog should cover the major external validation targets.");
        for (CalibrationTarget target : targets) {
            assertTrue(keys.add(target.key()), "Calibration target keys should be unique.");
            assertTrue(!target.empiricalDataset().isBlank(), "Calibration targets should name an empirical dataset.");
            assertTrue(!target.simulatorMetric().isBlank(), "Calibration targets should name simulator metrics.");
            assertTrue(!target.validationUse().isBlank(), "Calibration targets should explain how they will be used.");
        }

        keys.clear();
        assertTrue(benchmarks.size() >= 6, "Executable calibration should include empirical benchmark ranges.");
        assertTrue(
                Files.exists(CalibrationTargetCatalog.benchmarkFile()),
                "Calibration benchmark ranges should be backed by a tracked empirical benchmark extract."
        );
        for (CalibrationBenchmark benchmark : benchmarks) {
            assertTrue(keys.add(benchmark.key()), "Calibration benchmark keys should be unique.");
            assertTrue(!benchmark.empiricalDataset().isBlank(), "Calibration benchmarks should name a dataset.");
            assertTrue(!benchmark.scenarioKey().isBlank(), "Calibration benchmarks should name a scenario.");
            assertTrue(!benchmark.simulatorMetric().isBlank(), "Calibration benchmarks should name a simulator metric.");
            assertTrue(benchmark.minimum() <= benchmark.maximum(), "Calibration benchmark ranges should be ordered.");
        }
    }

}
