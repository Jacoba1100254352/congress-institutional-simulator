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
 * Common floor, voting, and reusable process constructors.
 */
final class SharedScenarioBuilders {
    private SharedScenarioBuilders() {
    }

    static LegislativeProcess defaultPassFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                new DefaultPassUnlessVetoedRule(2.0 / 3.0)
        );
        return new UnicameralProcess(name, chamber);
    }

    static LegislativeProcess simpleMajorityFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        return new UnicameralProcess(name, chamber);
    }

    static LegislativeProcess supermajorityFloorProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy,
            double threshold
    ) {
        Chamber chamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.supermajority(threshold)
        );
        return new UnicameralProcess(name, chamber);
    }

    static LegislativeProcess challengeMiddleLane(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        Chamber activeVoteChamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        return new ChallengeVoucherProcess(
                name,
                world.legislators(),
                strategy,
                ChallengeTokenAllocation.PARTY,
                10,
                0.82,
                new UnicameralProcess(name, activeVoteChamber)
        );
    }

    static LegislativeProcess informedGuardrailProcess(
            String name,
            SimulationWorld world,
            VotingStrategy strategy
    ) {
        List<Legislator> committeeMembers = CommitteeFactory.select(
                world.legislators(),
                CommitteeComposition.REPRESENTATIVE,
                17
        );
        Chamber floorChamber = new Chamber(
                "Congress",
                world.legislators(),
                strategy,
                new DefaultPassUnlessVetoedRule(2.0 / 3.0)
        );
        Chamber committee = new Chamber(
                "Committee",
                committeeMembers,
                strategy,
                AffirmativeThresholdRule.simpleMajority()
        );
        LegislativeProcess process = new UnicameralProcess(name, floorChamber);
        process = new CommitteeGatekeepingProcess(name, committee, process);
        process = new CommitteeInformationProcess(name, committeeMembers, 0.85, 0.45, process);
        return new ProposalAccessProcess(
                name,
                ProposalAccessRules.viabilityScreen(0.35, 0.85),
                process
        );
    }

    static Scenario unicameral(String name, VotingRule rule) {
        return unicameral(name, rule, VotingStrategies.standard());
    }

    static Scenario unicameral(String name, VotingRule rule, VotingStrategy strategy) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                Chamber chamber = new Chamber("Congress", world.legislators(), strategy, rule);
                return new UnicameralProcess(name, chamber);
            }
        };
    }

    static Scenario bicameral(String name, VotingRule rule) {
        return new Scenario() {
            @Override
            public String name() {
                return name;
            }

            @Override
            public LegislativeProcess buildProcess(SimulationWorld world) {
                VotingStrategy strategy = VotingStrategies.standard();
                Chamber house = new Chamber("House", world.legislators(), strategy, rule);
                Chamber senate = new Chamber("Senate", senateSubset(world.legislators()), strategy, rule);
                return new BicameralProcess(name, house, senate);
            }
        };
    }
}
