package congresssim.institution.agenda;


import congresssim.behavior.VoteContext;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;


public final class OpenFloorCalendarProcess implements LegislativeProcess
{
	private final String name;
	private final LegislativeProcess ordinaryFloorProcess;
	private final LegislativeProcess reviewProcess;
	private final double minimumPublicMandate;
	private final double reviewRiskThreshold;
	private final double captureBlockThreshold;
	private final double baseDelayCost;
	private final double amendmentOpenness;
	
	public OpenFloorCalendarProcess(
			String name,
			LegislativeProcess ordinaryFloorProcess,
			LegislativeProcess reviewProcess,
			double minimumPublicMandate,
			double reviewRiskThreshold,
			double captureBlockThreshold,
			double baseDelayCost,
			double amendmentOpenness
	) {
		Values.requireRange("minimumPublicMandate", minimumPublicMandate, 0.0, 1.0);
		Values.requireRange("reviewRiskThreshold", reviewRiskThreshold, 0.0, 1.0);
		Values.requireRange("captureBlockThreshold", captureBlockThreshold, 0.0, 1.0);
		Values.requireRange("baseDelayCost", baseDelayCost, 0.0, 1.0);
		Values.requireRange("amendmentOpenness", amendmentOpenness, 0.0, 1.0);
		this.name = name;
		this.ordinaryFloorProcess = ordinaryFloorProcess;
		this.reviewProcess = reviewProcess;
		this.minimumPublicMandate = minimumPublicMandate;
		this.reviewRiskThreshold = reviewRiskThreshold;
		this.captureBlockThreshold = captureBlockThreshold;
		this.baseDelayCost = baseDelayCost;
		this.amendmentOpenness = amendmentOpenness;
	}
	
	@Override
	public String name() {
		return name;
	}
	
	@Override
	public BillOutcome consider(Bill bill, VoteContext context) {
		double mandate = publicMandate(bill);
		double risk = routingRisk(bill, context);
		double capture = LobbyCaptureScoring.captureRisk(bill);
		boolean blockedAsAbusive = mandate < minimumPublicMandate && capture > captureBlockThreshold;
		double delayCost = baseDelayCost * (0.55 + risk) * (risk >= reviewRiskThreshold ? 1.65 : 1.0);
		OutcomeSignals signals = OutcomeSignals.diagnostics(Map.of(
				"openCalendarRate", blockedAsAbusive ? 0.0 : 1.0,
				"calendarDelayCost", delayCost,
				"amendmentOpenness", blockedAsAbusive ? 0.0 : amendmentOpenness
		));
		
		if (blockedAsAbusive) {
			return BillOutcome.accessDenied(
					bill,
					context.currentPolicyPosition(),
					"open calendar abuse screen"
			).withSignals(signals);
		}
		
		Bill scheduledBill = bill.withAttentionSpend(delayCost);
		LegislativeProcess next = risk >= reviewRiskThreshold ? reviewProcess : ordinaryFloorProcess;
		return next.consider(scheduledBill, context).withSignals(signals);
	}
	
	private double publicMandate(Bill bill) {
		return Values.clamp(
				(0.52 * bill.publicSupport())
						+ (0.20 * bill.publicBenefit())
						+ (0.14 * bill.salience())
						+ (0.10 * bill.affectedGroupSupport())
						- (0.18 * LobbyCaptureScoring.captureRisk(bill)),
				0.0,
				1.0
		);
	}
	
	private double routingRisk(Bill bill, VoteContext context) {
		return Values.clamp(
				(0.24 * (1.0 - bill.publicSupport()))
						+ (0.20 * AffectedGroupScoring.minorityHarm(bill))
						+ (0.18 * LobbyCaptureScoring.captureRisk(bill))
						+ (0.16 * bill.publicBenefitUncertainty())
						+ (0.12 * Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0)
						+ (0.10 * bill.salience()),
				0.0,
				1.0
		);
	}
}
