package congresssim.simulation.catalog;

import congresssim.simulation.*;

import congresssim.institution.accountability.EligibilityDiagnosticsProcess;
import congresssim.institution.accountability.EligibilityRule;
import congresssim.institution.accountability.LawRegistryProcess;
import congresssim.institution.accountability.ProposalBondProcess;
import congresssim.institution.accountability.ProposalCreditProcess;
import congresssim.institution.accountability.QuadraticAttentionBudgetProcess;
import congresssim.institution.accountability.SunsetTrialProcess;
import congresssim.institution.agenda.AdaptiveTrackProcess;
import congresssim.institution.agenda.AgendaLotteryProcess;
import congresssim.institution.agenda.ChallengeEscalationProcess;
import congresssim.institution.agenda.ChallengeTokenAllocation;
import congresssim.institution.agenda.ChallengeVoucherProcess;
import congresssim.institution.agenda.ProposalAccessProcess;
import congresssim.institution.agenda.ProposalAccessRules;
import congresssim.institution.bargaining.AlternativeSelectionRule;
import congresssim.institution.bargaining.AmendmentMediationProcess;
import congresssim.institution.bargaining.CoalitionCosponsorshipProcess;
import congresssim.institution.bargaining.CompetingAlternativesProcess;
import congresssim.institution.bargaining.MultiRoundAmendmentProcess;
import congresssim.institution.bargaining.MultidimensionalPackageBargainingProcess;
import congresssim.institution.bargaining.OmnibusBargainingProcess;
import congresssim.institution.bargaining.PackageBargainingProcess;
import congresssim.institution.chamber.BicameralConflictMode;
import congresssim.institution.chamber.BicameralOriginRule;
import congresssim.institution.chamber.BicameralProcess;
import congresssim.institution.chamber.BicameralRoutingProcess;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.ChamberArchitectureSignalProcess;
import congresssim.institution.chamber.ConferenceCommitteeProcess;
import congresssim.institution.chamber.ConstitutionalCourtArchitectureProcess;
import congresssim.institution.chamber.DistrictPopulationProcess;
import congresssim.institution.chamber.PresidentialVetoProcess;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.committee.CommitteeGatekeepingProcess;
import congresssim.institution.committee.CommitteeInformationProcess;
import congresssim.institution.committee.CommitteePowerConfig;
import congresssim.institution.committee.CommitteePowerProcess;
import congresssim.institution.committee.CommitteeRoleMode;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.DistributionalHarmProcess;
import congresssim.institution.distribution.HarmWeightedThresholdProcess;
import congresssim.institution.lobbying.BudgetedLobbyingProcess;
import congresssim.institution.lobbying.InfluenceSystemProcess;
import congresssim.institution.lobbying.LobbyAuditProcess;
import congresssim.institution.lobbying.LobbyTransparencyProcess;
import congresssim.institution.publicinput.CitizenInitiativeProcess;
import congresssim.institution.publicinput.CitizenPanelMode;
import congresssim.institution.publicinput.CitizenPanelReviewProcess;
import congresssim.institution.publicinput.ConstituentPublicWillProcess;
import congresssim.institution.publicinput.PublicObjectionWindowProcess;
import congresssim.institution.review.ExAnteReviewMode;
import congresssim.institution.review.ExAnteReviewProcess;
import congresssim.institution.review.IndependentInstitutionBundle;
import congresssim.institution.review.JudicialReviewProcess;
import congresssim.institution.strategy.DemocraticDeteriorationProcess;
import congresssim.institution.strategy.InstitutionalNormErosionProcess;
import congresssim.institution.strategy.LongHorizonStrategyProcess;
import congresssim.institution.strategy.ProposerStrategyProcess;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.institution.voting.DefaultPassUnlessVetoedRule;
import congresssim.institution.voting.VotingRule;

import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Legislator;
import congresssim.model.SimulationWorld;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

import static congresssim.simulation.catalog.BroadSystemScenarioBuilders.*;
import static congresssim.simulation.catalog.ChamberCommitteeScenarioBuilders.*;
import static congresssim.simulation.catalog.DefaultPassScenarioBuilders.*;
import static congresssim.simulation.catalog.SharedScenarioBuilders.*;

/**
 * Chamber architecture, committee-power, eligibility, ex ante review, and conventional benchmark builders.
 */
final class ChamberCommitteeScenarioBuilders {
    private ChamberCommitteeScenarioBuilders() {
    }

    static Scenario majorityWithCommitteePower(
            String name,
            CommitteeComposition composition,
            double dischargeThreshold,
            double reportingDeadlinePressure,
            double amendmentStrength,
            double minorityHearingThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(world.legislators(), composition, 19);
                Chamber committee = new Chamber(
                        "Committee power",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber floor = new Chamber(
                        "Floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = new UnicameralProcess(name(), floor);
                process = new CommitteePowerProcess(
                        name(),
                        committee,
                        process,
                        dischargeThreshold,
                        reportingDeadlinePressure,
                        amendmentStrength,
                        minorityHearingThreshold
                );
                return new CommitteeInformationProcess(name(), committeeMembers, 0.70, 0.40, process);
            }
        };
    }

    static Scenario majorityWithCommitteeRole(
            String name,
            CommitteeRoleMode roleMode,
            CommitteeComposition composition,
            double gatekeepingThreshold,
            double chairNegativeAgendaPower,
            double informationAccuracy,
            double queueCapacity,
            double reviewCost,
            double captureSusceptibility
    ) {
        CommitteePowerConfig config = new CommitteePowerConfig(
                roleMode,
                gatekeepingThreshold,
                chairNegativeAgendaPower,
                informationAccuracy,
                queueCapacity,
                reviewCost,
                captureSusceptibility,
                Math.clamp(informationAccuracy - (0.30 * captureSusceptibility), 0.0, 1.0),
                Math.clamp(gatekeepingThreshold + 0.08, 0.0, 1.0),
                Math.clamp(0.42 + (0.40 * informationAccuracy), 0.0, 1.0),
                0.46,
                roleMode == CommitteeRoleMode.PUBLIC_ACCOUNTS ? 0.58 : 0.42,
                roleMode == CommitteeRoleMode.VETO_PLAYER,
                roleMode != CommitteeRoleMode.FAST_TRACK_CERTIFIER
        );
        return majorityWithConfiguredCommittee(
                name,
                CommitteeSelectionConfig.standard("general", 19),
                config,
                composition
        );
    }

    static Scenario majorityWithConfiguredCommittee(
            String name,
            CommitteeSelectionConfig selectionConfig,
            CommitteePowerConfig powerConfig
    ) {
        return majorityWithConfiguredCommittee(
                name,
                selectionConfig,
                powerConfig,
                CommitteeComposition.MIXED_PARLIAMENTARIAN_CITIZEN
        );
    }

    static Scenario majorityWithConfiguredCommittee(
            String name,
            CommitteeSelectionConfig selectionConfig,
            CommitteePowerConfig powerConfig,
            CommitteeComposition fallbackComposition
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                CommitteeSelectionResult selection = selectionConfig == null
                        ? new CommitteeSelectionResult(
                        CommitteeFactory.select(world.legislators(), fallbackComposition, 19),
                        null,
                        1.0,
                        0.0,
                        0.34,
                        true
                )
                        : CommitteeFactory.select(world.legislators(), selectionConfig);
                Chamber committee = new Chamber(
                        "Configured committee",
                        selection.members(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber floor = new Chamber(
                        "Floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = new UnicameralProcess(name(), floor);
                process = new CommitteePowerProcess(
                        name(),
                        committee,
                        process,
                        0.36,
                        powerConfig
                );
                return new CommitteeInformationProcess(
                        name(),
                        selection.members(),
                        Math.clamp(powerConfig.informationAccuracy() + (0.12 * selection.citizenAdvisoryWeight()), 0.0, 1.0),
                        Math.clamp(powerConfig.captureSusceptibility(), 0.0, 1.0),
                        process
                );
            }
        };
    }

    static Scenario majorityWithCommitteeComposition(String name, CommitteeComposition composition) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(world.legislators(), composition, 19);
                Chamber committee = new Chamber(
                        "Committee",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber floor = new Chamber(
                        "Floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                LegislativeProcess process = new UnicameralProcess(name(), floor);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                return new CommitteeInformationProcess(name(), committeeMembers, 0.72, 0.44, process);
            }
        };
    }

    static Scenario chamberUnicameral(String name, ChamberSpec chamberSpec, VotingRule rule) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> members = ChamberFactory.select(world.legislators(), chamberSpec, 15_151L);
                Chamber chamber = new Chamber(chamberSpec.name(), members, strategy, rule);
                OutcomeSignals architectureSignals = chamberArchitectureSignals(
                        world.legislators(),
                        chamberSpec,
                        chamberSpec,
                        members,
                        members
                );
                return new ChamberArchitectureSignalProcess(new UnicameralProcess(name(), chamber), architectureSignals);
            }
        };
    }

    static Scenario eligibilityFilteredMajority(
            String name,
            EligibilityRule eligibilityRule,
            boolean appointmentPool
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> candidatePool = appointmentPool
                        ? ChamberFactory.select(world.legislators(), ChamberSpec.appointedUpperHouse(101, 0.62), 72_121L)
                        : world.legislators();
                List<Legislator> eligible = eligibleMembers(candidatePool, eligibilityRule, Math.min(31, candidatePool.size()));
                Chamber chamber = new Chamber("Eligibility-filtered chamber", eligible, strategy, AffirmativeThresholdRule.simpleMajority());
                LegislativeProcess process = new UnicameralProcess(name(), chamber);
                return new EligibilityDiagnosticsProcess(name(), world.legislators(), eligible, eligibilityRule, process);
            }
        };
    }

    static Scenario exAnteReviewMajority(
            String name,
            ExAnteReviewMode mode,
            IndependentInstitutionBundle bundle,
            double highRiskThreshold,
            double overrideThreshold
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber chamber = new Chamber("Congress", world.legislators(), strategy, AffirmativeThresholdRule.simpleMajority());
                return new ExAnteReviewProcess(
                        name(),
                        mode,
                        bundle,
                        highRiskThreshold,
                        overrideThreshold,
                        new UnicameralProcess(name(), chamber)
                );
            }
        };
    }

    static List<Legislator> eligibleMembers(
            List<Legislator> candidatePool,
            EligibilityRule eligibilityRule,
            int minimumSize
    ) {
        List<Legislator> eligible = candidatePool.stream()
                .filter(eligibilityRule::eligible)
                .toList();
        if (eligible.size() >= minimumSize) {
            return eligible;
        }
        List<Legislator> expanded = new ArrayList<>(eligible);
        candidatePool.stream()
                .sorted(Comparator.comparingDouble(EligibilityRule::expertiseProxy).reversed())
                .filter(legislator -> expanded.stream().noneMatch(existing -> existing.id().equals(legislator.id())))
                .forEach(legislator -> {
                    if (expanded.size() < minimumSize) {
                        expanded.add(legislator);
                    }
                });
        return expanded;
    }

    static Scenario chamberArchitecture(
            String name,
            ChamberSpec lowerSpec,
            ChamberSpec upperSpec,
            VotingRule upperRule,
            boolean useConference
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> lowerMembers = ChamberFactory.select(world.legislators(), lowerSpec, 10_101L);
                List<Legislator> upperMembers = ChamberFactory.select(world.legislators(), upperSpec, 20_202L);
                Chamber lower = new Chamber(
                        lowerSpec.name(),
                        lowerMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber upper = new Chamber(upperSpec.name(), upperMembers, strategy, upperRule);
                OutcomeSignals architectureSignals = chamberArchitectureSignals(
                        world.legislators(),
                        lowerSpec,
                        upperSpec,
                        lowerMembers,
                        upperMembers
                );
                LegislativeProcess process;
                if (useConference) {
                    process = new ConferenceCommitteeProcess(
                            name(),
                            lower,
                            upper,
                            0.46,
                            (chamberMedian(lowerMembers) + chamberMedian(upperMembers)) / 2.0,
                            0.34,
                            0.28
                    );
                } else {
                    process = new BicameralProcess(name(), lower, upper);
                }
                return new ChamberArchitectureSignalProcess(process, architectureSignals);
            }
        };
    }

    static Scenario chamberRouting(
            String name,
            ChamberSpec lowerSpec,
            ChamberSpec upperSpec,
            VotingRule upperRule,
            BicameralOriginRule originRule,
            BicameralConflictMode conflictMode
    ) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> lowerMembers = ChamberFactory.select(world.legislators(), lowerSpec, 30_303L);
                List<Legislator> upperMembers = ChamberFactory.select(world.legislators(), upperSpec, 40_404L);
                Chamber lower = new Chamber(
                        lowerSpec.name(),
                        lowerMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber upper = new Chamber(upperSpec.name(), upperMembers, strategy, upperRule);
                LegislativeProcess process = new BicameralRoutingProcess(
                        name(),
                        lower,
                        upper,
                        strategy,
                        originRule,
                        conflictMode,
                        AffirmativeThresholdRule.simpleMajority(),
                        0.46,
                        (chamberMedian(lowerMembers) + chamberMedian(upperMembers)) / 2.0,
                        0.32,
                        0.22,
                        0.58,
                        3
                );
                return new ChamberArchitectureSignalProcess(
                        process,
                        chamberArchitectureSignals(world.legislators(), lowerSpec, upperSpec, lowerMembers, upperMembers)
                );
            }
        };
    }

    static OutcomeSignals chamberArchitectureSignals(
            List<Legislator> electorate,
            ChamberSpec lowerSpec,
            ChamberSpec upperSpec,
            List<Legislator> lowerMembers,
            List<Legislator> upperMembers
    ) {
        List<RepresentationUnit> lowerUnits = ChamberFactory.representationUnits(lowerSpec);
        List<RepresentationUnit> upperUnits = ChamberFactory.representationUnits(upperSpec);
        double populationSeatDistortion = average(
                ChamberArchitectureMetrics.populationSeatDistortion(lowerUnits),
                ChamberArchitectureMetrics.populationSeatDistortion(upperUnits)
        );
        double democraticResponsiveness = average(
                ChamberArchitectureMetrics.democraticResponsiveness(lowerUnits),
                ChamberArchitectureMetrics.democraticResponsiveness(upperUnits)
        );
        double seatVoteDistortion = average(
                ChamberArchitectureMetrics.seatVoteDistortion(electorate, lowerMembers),
                ChamberArchitectureMetrics.seatVoteDistortion(electorate, upperMembers)
        );
        double constituencyServiceConcentration = average(
                ChamberArchitectureMetrics.constituencyServiceConcentration(lowerUnits),
                ChamberArchitectureMetrics.constituencyServiceConcentration(upperUnits)
        );
        double regionalTransferBias = average(
                ChamberArchitectureMetrics.regionalTransferBias(lowerUnits),
                ChamberArchitectureMetrics.regionalTransferBias(upperUnits)
        );
        double malapportionmentIndex = average(
                ChamberArchitectureMetrics.malapportionmentIndex(lowerUnits),
                ChamberArchitectureMetrics.malapportionmentIndex(upperUnits)
        );
        return OutcomeSignals.chamberArchitecture(
                populationSeatDistortion,
                democraticResponsiveness,
                seatVoteDistortion,
                constituencyServiceConcentration,
                regionalTransferBias
        ).plus(OutcomeSignals.diagnostic("malapportionmentIndex", malapportionmentIndex));
    }

    static double average(double left, double right) {
        return (left + right) / 2.0;
    }

    static Scenario presidentialVeto() {
        return new Scenario() {
            @Override
            public String name() {
                return "Bicameral majority + presidential veto";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                VotingRule chamberRule = AffirmativeThresholdRule.simpleMajority();
                Chamber house = new Chamber("House", world.legislators(), strategy, chamberRule);
                Chamber senate = new Chamber("Senate", senateSubset(world.legislators()), strategy, chamberRule);
                LegislativeProcess bicameral = new BicameralProcess(name(), house, senate);
                Legislator president = presidentFromWorld(world);
                return new PresidentialVetoProcess(
                        bicameral,
                        president,
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
            }
        };
    }

    static Scenario currentSystem() {
        return new Scenario() {
            @Override
            public String name() {
                return "Stylized U.S.-like conventional benchmark";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber house = new Chamber(
                        "House",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber senate = new Chamber(
                        "Senate",
                        senateSubset(world.legislators()),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                LegislativeProcess bicameral = new BicameralProcess(name(), house, senate);
                LegislativeProcess finalPassage = new PresidentialVetoProcess(
                        bicameral,
                        presidentFromWorld(world),
                        strategy,
                        0.68,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.currentSystemAgenda(0.58),
                        finalPassage
                );
            }
        };
    }

    static Scenario stylizedCurrentCongressWorkflow() {
        return new Scenario() {
            @Override
            public String name() {
                return "Stylized current-Congress workflow";
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                List<Legislator> committeeMembers = CommitteeFactory.select(
                        world.legislators(),
                        CommitteeComposition.MAJORITY_CONTROLLED,
                        19
                );
                Chamber committee = new Chamber(
                        "Committee queue",
                        committeeMembers,
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber house = new Chamber(
                        "House floor",
                        world.legislators(),
                        strategy,
                        AffirmativeThresholdRule.simpleMajority()
                );
                Chamber senate = new Chamber(
                        "Senate cloture/final passage",
                        senateSubset(world.legislators()),
                        strategy,
                        AffirmativeThresholdRule.supermajority(0.60)
                );
                LegislativeProcess process = new ConferenceCommitteeProcess(
                        name(),
                        house,
                        senate,
                        0.50,
                        chamberMedian(world.legislators()),
                        0.30,
                        0.34
                );
                process = new PresidentialVetoProcess(
                        process,
                        presidentFromWorld(world),
                        strategy,
                        0.66,
                        AffirmativeThresholdRule.supermajority(2.0 / 3.0)
                );
                process = new JudicialReviewProcess(name(), process, 0.44, 0.68, 0.44);
                process = new CommitteeGatekeepingProcess(name(), committee, process);
                process = new CommitteeInformationProcess(name(), committeeMembers, 0.74, 0.50, process);
                return new ProposalAccessProcess(
                        name(),
                        ProposalAccessRules.leadershipAgenda(
                                world.legislators(),
                                0.58,
                                0.46,
                                0.34,
                                0.20,
                                0.20,
                                0.16
                        ),
                        process
                );
            }
        };
    }

    static double chamberMedian(List<Legislator> legislators) {
        if (legislators.isEmpty()) {
            return 0.0;
        }
        List<Double> positions = legislators.stream()
                .map(Legislator::ideology)
                .sorted()
                .toList();
        int middle = positions.size() / 2;
        if (positions.size() % 2 == 1) {
            return positions.get(middle);
        }
        return (positions.get(middle - 1) + positions.get(middle)) / 2.0;
    }

    static List<Legislator> senateSubset(List<Legislator> legislators) {
        List<Legislator> senate = new ArrayList<>();
        int stride = Math.max(2, legislators.size() / Math.max(1, legislators.size() / 3));
        for (int i = 0; i < legislators.size(); i += stride) {
            senate.add(legislators.get(i));
        }
        if (senate.isEmpty()) {
            senate.add(legislators.getFirst());
        }
        return senate;
    }

    static Legislator presidentFromWorld(SimulationWorld world) {
        double averageIdeology = world.legislators()
                .stream()
                .mapToDouble(Legislator::ideology)
                .average()
                .orElse(0.0);
        return new Legislator(
                "EXEC-1",
                "Executive",
                averageIdeology * 0.7,
                0.42,
                0.72,
                0.58,
                0.46,
                0.62
        );
    }
}
