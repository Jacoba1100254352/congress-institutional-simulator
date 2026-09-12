package congresssim.institution.agenda;


import congresssim.behavior.VoteContext;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.Map;


public final class FloorRuleSchedulingProcess implements LegislativeProcess
{
	private static final double DEFAULT_SPECIAL_RULE_THRESHOLD = 0.55;
	private static final double DEFAULT_SUSPENSION_THRESHOLD = 0.50;

	private final String name;
	private final LegislativeProcess innerProcess;
	private final double openRuleNorm;
	private final double leadershipClosurePressure;
	private final double queueDelayBase;
	private final double dischargeMandateThreshold;
	private final double fallbackBlockThreshold;
	private final double minimumCalendarPriority;
	private final double specialRuleThreshold;
	private final double suspensionThreshold;
	
	public FloorRuleSchedulingProcess(
			String name,
			LegislativeProcess innerProcess,
			double openRuleNorm,
			double leadershipClosurePressure,
			double queueDelayBase,
			double dischargeMandateThreshold,
			double fallbackBlockThreshold
	) {
		this(
				name,
				innerProcess,
				openRuleNorm,
				leadershipClosurePressure,
				queueDelayBase,
				dischargeMandateThreshold,
				fallbackBlockThreshold,
				0.0,
				DEFAULT_SPECIAL_RULE_THRESHOLD,
				DEFAULT_SUSPENSION_THRESHOLD
		);
	}

	public FloorRuleSchedulingProcess(
			String name,
			LegislativeProcess innerProcess,
			double openRuleNorm,
			double leadershipClosurePressure,
			double queueDelayBase,
			double dischargeMandateThreshold,
			double fallbackBlockThreshold,
			double minimumCalendarPriority
	) {
		this(
				name,
				innerProcess,
				openRuleNorm,
				leadershipClosurePressure,
				queueDelayBase,
				dischargeMandateThreshold,
				fallbackBlockThreshold,
				minimumCalendarPriority,
				DEFAULT_SPECIAL_RULE_THRESHOLD,
				DEFAULT_SUSPENSION_THRESHOLD
		);
	}

	public FloorRuleSchedulingProcess(
			String name,
			LegislativeProcess innerProcess,
			double openRuleNorm,
			double leadershipClosurePressure,
			double queueDelayBase,
			double dischargeMandateThreshold,
			double fallbackBlockThreshold,
			double minimumCalendarPriority,
			double specialRuleThreshold,
			double suspensionThreshold
	) {
		Values.requireRange("openRuleNorm", openRuleNorm, 0.0, 1.0);
		Values.requireRange("leadershipClosurePressure", leadershipClosurePressure, 0.0, 1.0);
		Values.requireRange("queueDelayBase", queueDelayBase, 0.0, 1.0);
		Values.requireRange("dischargeMandateThreshold", dischargeMandateThreshold, 0.0, 1.0);
		Values.requireRange("fallbackBlockThreshold", fallbackBlockThreshold, 0.0, 1.0);
		Values.requireRange("minimumCalendarPriority", minimumCalendarPriority, 0.0, 1.0);
		Values.requireRange("specialRuleThreshold", specialRuleThreshold, 0.0, 1.0);
		Values.requireRange("suspensionThreshold", suspensionThreshold, 0.0, 1.0);
		this.name = name;
		this.innerProcess = innerProcess;
		this.openRuleNorm = openRuleNorm;
		this.leadershipClosurePressure = leadershipClosurePressure;
		this.queueDelayBase = queueDelayBase;
		this.dischargeMandateThreshold = dischargeMandateThreshold;
		this.fallbackBlockThreshold = fallbackBlockThreshold;
		this.minimumCalendarPriority = minimumCalendarPriority;
		this.specialRuleThreshold = specialRuleThreshold;
		this.suspensionThreshold = suspensionThreshold;
	}
	
	private static double mandateScore(Bill bill) {
		return Values.clamp(
				(0.46 * bill.publicSupport())
						+ (0.22 * bill.salience())
						+ (0.16 * bill.affectedGroupSupport())
						+ (0.10 * bill.publicBenefit())
						+ (0.06 * Math.clamp(bill.cosponsorCount() / 10.0, 0.0, 1.0))
						- (0.16 * LobbyCaptureScoring.captureRisk(bill)),
				0.0,
				1.0
		);
	}
	
	private static double schedulingRisk(Bill bill, VoteContext context) {
		return Values.clamp(
				(0.26 * (1.0 - bill.publicSupport()))
						+ (0.20 * AffectedGroupScoring.minorityHarm(bill))
						+ (0.18 * bill.publicBenefitUncertainty())
						+ (0.14 * LobbyCaptureScoring.captureRisk(bill))
						+ (0.12 * Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0)
						+ (0.10 * bill.salience()),
				0.0,
				1.0
		);
	}

	private static double ideologicalDistance(Bill bill, VoteContext context) {
		return Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0;
	}

	private static double specialRuleScore(
			Bill bill,
			VoteContext context,
			double closureScore,
			double risk
	) {
		return Values.clamp(
				(0.42 * closureScore)
						+ (0.23 * risk)
						+ (0.20 * bill.salience())
						+ (0.15 * ideologicalDistance(bill, context)),
				0.0,
				1.0
		);
	}

	private static double suspensionScore(
			Bill bill,
			VoteContext context,
			double mandate,
			double risk,
			double capture
	) {
		return Values.clamp(
				(0.42 * mandate)
						+ (0.24 * (1.0 - risk))
						+ (0.18 * (1.0 - capture))
						+ (0.10 * (1.0 - ideologicalDistance(bill, context)))
						+ (0.06 * (1.0 - bill.publicBenefitUncertainty())),
				0.0,
				1.0
		);
	}
	
	@Override
	public String name() {
		return name;
	}
	
	@Override
	public BillOutcome consider(Bill bill, VoteContext context) {
		double mandate = mandateScore(bill);
		double risk = schedulingRisk(bill, context);
		double capture = LobbyCaptureScoring.captureRisk(bill);
		double closureScore = Values.clamp(
				leadershipClosurePressure
						+ (0.20 * capture)
						+ (0.14 * risk)
						+ (0.12 * Math.max(0.0, Math.abs(bill.ideologyPosition()) - 0.35))
						- (0.22 * mandate)
						- (0.18 * openRuleNorm),
				0.0,
				1.0
		);
		boolean dischargeBackstop = mandate >= dischargeMandateThreshold
				&& bill.salience() >= 0.52
				&& capture < 0.72;
		boolean closedRule = !dischargeBackstop && closureScore >= Math.max(0.34, openRuleNorm);
		double statusQuoFallbackPressure = Values.clamp(
				closureScore
						+ (0.22 * (1.0 - mandate))
						+ (0.12 * risk)
						- (dischargeBackstop ? 0.28 : 0.0),
				0.0,
				1.0
		);
		double delay = Values.clamp(
				queueDelayBase
						+ (0.24 * statusQuoFallbackPressure)
						+ (closedRule ? 0.12 : 0.0)
						- (dischargeBackstop ? 0.16 : 0.0),
				0.0,
				1.0
		);
		double calendarPriority = Values.clamp(
				(0.40 * mandate)
						+ (0.20 * (1.0 - risk))
						+ (0.14 * (1.0 - capture))
						+ (0.12 * bill.salience())
						+ (0.08 * bill.publicBenefit())
						+ (0.06 * Math.clamp(bill.cosponsorCount() / 10.0, 0.0, 1.0)),
				0.0,
				1.0
		);
		boolean calendarCapacityDenied = !dischargeBackstop && calendarPriority < minimumCalendarPriority;
		double specialScore = specialRuleScore(bill, context, closureScore, risk);
		double suspensionScore = suspensionScore(bill, context, mandate, risk, capture);
		Map<String, Double> diagnosticValues = new HashMap<>();
		diagnosticValues.put("floorSchedulingDelay", delay);
		diagnosticValues.put("closedRuleRate", closedRule ? 1.0 : 0.0);
		diagnosticValues.put("openRuleRate", closedRule ? 0.0 : 1.0);
		diagnosticValues.put("dischargeBackstopUse", dischargeBackstop ? 1.0 : 0.0);
		diagnosticValues.put("statusQuoFallbackPressure", statusQuoFallbackPressure);
		diagnosticValues.put(
				"leadershipSchedulingBias",
				Values.clamp(closureScore * leadershipClosurePressure, 0.0, 1.0)
		);
		diagnosticValues.put(
				"rulesCommitteeCaptureIndex",
				Values.clamp(capture * leadershipClosurePressure * (closedRule ? 1.0 : 0.55), 0.0, 1.0)
		);
		diagnosticValues.put("calendarPriorityScore", calendarPriority);
		diagnosticValues.put("calendarCapacityDenialRate", calendarCapacityDenied ? 1.0 : 0.0);
		diagnosticValues.put("specialRuleRouteScore", specialScore);
		diagnosticValues.put("suspensionRouteScore", suspensionScore);
		diagnosticValues.put("specialRuleOnlyRouteRate", 0.0);
		diagnosticValues.put("suspensionOnlyRouteRate", 0.0);
		diagnosticValues.put("mixedSpecialRuleAndSuspensionRouteRate", 0.0);
		diagnosticValues.put("otherFloorRouteRate", 0.0);
		diagnosticValues.put("restrictiveSpecialRuleRouteRate", 0.0);
		diagnosticValues.put("floorRouteAssignmentRate", 0.0);
		OutcomeSignals signals = OutcomeSignals.diagnostics(diagnosticValues);

		if (calendarCapacityDenied) {
			return BillOutcome.accessDenied(
					bill,
					context.currentPolicyPosition(),
					"floor calendar capacity gate"
			).withSignals(signals);
		}
		
		if (!dischargeBackstop && statusQuoFallbackPressure >= fallbackBlockThreshold && mandate < 0.36) {
			return BillOutcome.accessDenied(
					bill,
					context.currentPolicyPosition(),
					"floor calendar fallback to status quo"
			).withSignals(signals);
		}

		boolean specialRoute = specialScore >= specialRuleThreshold;
		boolean suspensionRoute = suspensionScore >= suspensionThreshold;
		boolean mixedRoute = specialRoute && suspensionRoute;
		boolean specialOnlyRoute = specialRoute && !suspensionRoute;
		boolean suspensionOnlyRoute = !specialRoute && suspensionRoute;
		boolean otherRoute = !specialRoute && !suspensionRoute;
		boolean restrictiveSpecialRule = specialRoute
				&& closureScore >= Math.max(0.34, openRuleNorm);
		diagnosticValues.put("specialRuleOnlyRouteRate", specialOnlyRoute ? 1.0 : 0.0);
		diagnosticValues.put("suspensionOnlyRouteRate", suspensionOnlyRoute ? 1.0 : 0.0);
		diagnosticValues.put("mixedSpecialRuleAndSuspensionRouteRate", mixedRoute ? 1.0 : 0.0);
		diagnosticValues.put("otherFloorRouteRate", otherRoute ? 1.0 : 0.0);
		diagnosticValues.put("restrictiveSpecialRuleRouteRate", restrictiveSpecialRule ? 1.0 : 0.0);
		diagnosticValues.put("floorRouteAssignmentRate", 1.0);
		signals = OutcomeSignals.diagnostics(diagnosticValues);
		
		double opennessPenalty = closedRule ? 0.0 : 0.04 * (mandate - risk);
		Bill scheduled = bill.withAttentionSpend(delay + Math.max(0.0, -opennessPenalty));
		return innerProcess.consider(scheduled, context).withSignals(signals);
	}
}
