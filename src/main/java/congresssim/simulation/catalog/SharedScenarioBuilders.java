package congresssim.simulation.catalog;


import congresssim.behavior.VotingStrategies;
import congresssim.behavior.VotingStrategy;
import congresssim.institution.agenda.ChallengeTokenAllocation;
import congresssim.institution.agenda.ChallengeVoucherProcess;
import congresssim.institution.agenda.ProposalAccessProcess;
import congresssim.institution.agenda.ProposalAccessRules;
import congresssim.institution.chamber.BicameralProcess;
import congresssim.institution.chamber.Chamber;
import congresssim.institution.chamber.UnicameralProcess;
import congresssim.institution.committee.CommitteeGatekeepingProcess;
import congresssim.institution.committee.CommitteeInformationProcess;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.voting.AffirmativeThresholdRule;
import congresssim.institution.voting.DefaultPassUnlessVetoedRule;
import congresssim.institution.voting.VotingRule;
import congresssim.model.Legislator;
import congresssim.model.SimulationWorld;
import congresssim.simulation.CommitteeComposition;
import congresssim.simulation.CommitteeFactory;
import congresssim.simulation.Scenario;

import java.util.List;

import static congresssim.simulation.catalog.ChamberCommitteeScenarioBuilders.senateSubset;


/**
 * Common floor, voting, and reusable process constructors.
 */
final class SharedScenarioBuilders
{
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
		return new Scenario()
		{
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
		return new Scenario()
		{
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
