package congresssim.institution.review;


import congresssim.behavior.VoteContext;
import congresssim.institution.agenda.AdaptiveTrackProcess;
import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.distribution.AffectedGroupScoring;
import congresssim.institution.lobbying.LobbyCaptureScoring;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.Map;


/**
 * Applies a bounded administrative-capacity constraint to a defended review path.
 * External filings and case review draw from the same recoverable capacity pool;
 * cases below the configured coverage threshold use the overflow path.
 */
public final class AdministrativeReviewCapacityProcess implements LegislativeProcess
{
	private static final double EPSILON = 0.000001;

	private final String name;
	private final LegislativeProcess defendedProcess;
	private final LegislativeProcess overflowProcess;
	private final double capacityUnits;
	private final double recoveryUnitsPerCycle;
	private final double minimumDefendedCoverage;

	private double availableCapacity;
	private double backlogUnits;
	private double pendingExternalDemand;
	private double cumulativeDemandUnits;
	private double cumulativeQueuePressure;
	private int consideredCases;
	private int defendedCases;
	private int overflowFallbackCases;
	private int overloadEvents;
	private int recoveryEvents;
	private boolean everOverloaded;

	public AdministrativeReviewCapacityProcess(
			String name,
			LegislativeProcess defendedProcess,
			LegislativeProcess overflowProcess,
			double capacityUnits,
			double recoveryUnitsPerCycle,
			double minimumDefendedCoverage
	) {
		if (!Double.isFinite(capacityUnits) || capacityUnits <= 0.0) {
			throw new IllegalArgumentException("capacityUnits must be finite and positive.");
		}
		if (!Double.isFinite(recoveryUnitsPerCycle) || recoveryUnitsPerCycle <= 0.0) {
			throw new IllegalArgumentException("recoveryUnitsPerCycle must be finite and positive.");
		}
		Values.requireRange("minimumDefendedCoverage", minimumDefendedCoverage, 0.0, 1.0);
		this.name = name;
		this.defendedProcess = defendedProcess;
		this.overflowProcess = overflowProcess;
		this.capacityUnits = capacityUnits;
		this.recoveryUnitsPerCycle = recoveryUnitsPerCycle;
		this.minimumDefendedCoverage = minimumDefendedCoverage;
		this.availableCapacity = capacityUnits;
	}

	@Override
	public String name() {
		return name;
	}

	/** Adds proposal, filing, or review demand before the next legislative case. */
	public void submitExternalDemand(double units) {
		if (!Double.isFinite(units) || units < 0.0) {
			throw new IllegalArgumentException("external demand must be finite and nonnegative.");
		}
		pendingExternalDemand += units;
	}

	/** Advances one no-case recovery cycle and returns the resulting capacity state. */
	public CapacitySnapshot advanceRecoveryCycle() {
		if (pendingExternalDemand > EPSILON) {
			backlogUnits += pendingExternalDemand;
			cumulativeDemandUnits += pendingExternalDemand;
			pendingExternalDemand = 0.0;
		}
		boolean hadBacklog = backlogUnits > EPSILON;
		recoverAndServeBacklog();
		if (hadBacklog && backlogUnits <= EPSILON) {
			recoveryEvents++;
		}
		cumulativeQueuePressure += backlogUnits;
		return snapshot();
	}

	@Override
	public BillOutcome consider(Bill bill, VoteContext context) {
		consideredCases++;
		boolean hadBacklog = backlogUnits > EPSILON;
		recoverAndServeBacklog();
		boolean backlogCleared = hadBacklog && backlogUnits <= EPSILON;
		if (backlogCleared) {
			recoveryEvents++;
		}

		double externalDemand = pendingExternalDemand;
		pendingExternalDemand = 0.0;
		double backlogBeforeExternalDemand = backlogUnits;
		backlogUnits += externalDemand;
		cumulativeDemandUnits += externalDemand;
		double totalBacklogServed = serveBacklog();
		double existingBacklogServed = Math.min(totalBacklogServed, backlogBeforeExternalDemand);
		double externalDemandServed = Math.max(0.0, totalBacklogServed - existingBacklogServed);

		double caseDemand = reviewDemand(bill, context);
		cumulativeDemandUnits += caseDemand;
		double coveredDemand = Math.min(availableCapacity, caseDemand);
		availableCapacity -= coveredDemand;
		double uncoveredDemand = Math.max(0.0, caseDemand - coveredDemand);
		backlogUnits += uncoveredDemand;
		double reviewCoverage = caseDemand <= EPSILON ? 1.0 : coveredDemand / caseDemand;
		boolean overflowFallback = reviewCoverage + EPSILON < minimumDefendedCoverage;
		boolean overloaded = backlogUnits > EPSILON || overflowFallback;
		if (overloaded) {
			overloadEvents++;
			everOverloaded = true;
		}
		if (overflowFallback) {
			overflowFallbackCases++;
		} else {
			defendedCases++;
		}
		cumulativeQueuePressure += backlogUnits;

		LegislativeProcess selected = overflowFallback ? overflowProcess : defendedProcess;
		BillOutcome outcome = selected.consider(bill, context);
		return outcome.withSignals(OutcomeSignals.diagnostics(Map.ofEntries(
				Map.entry("administrativeReviewDemand", caseDemand),
				Map.entry("administrativeExternalDemand", externalDemand),
				Map.entry("administrativeExternalDemandServed", externalDemandServed),
				Map.entry("administrativeReviewCoverage", reviewCoverage),
				Map.entry("administrativeCapacityUsed", coveredDemand + externalDemandServed),
				Map.entry("administrativeCapacityRemainingShare", availableCapacity / capacityUnits),
				Map.entry("administrativeQueueOverflow", backlogUnits),
				Map.entry("administrativeCapacitySaturated", overloaded ? 1.0 : 0.0),
				Map.entry("administrativeOverflowFallback", overflowFallback ? 1.0 : 0.0),
				Map.entry("administrativeRecoveryEvent", backlogCleared ? 1.0 : 0.0),
				Map.entry("administrativeCumulativeQueuePressure", cumulativeQueuePressure)
		)));
	}

	public CapacitySnapshot snapshot() {
		return new CapacitySnapshot(
				capacityUnits,
				availableCapacity,
				backlogUnits + pendingExternalDemand,
				cumulativeDemandUnits + pendingExternalDemand,
				cumulativeQueuePressure,
				consideredCases,
				defendedCases,
				overflowFallbackCases,
				overloadEvents,
				recoveryEvents,
				everOverloaded,
				backlogUnits + pendingExternalDemand <= EPSILON
						&& availableCapacity / capacityUnits >= minimumDefendedCoverage
		);
	}

	private void recoverAndServeBacklog() {
		availableCapacity = Math.min(capacityUnits, availableCapacity + recoveryUnitsPerCycle);
		serveBacklog();
	}

	private double serveBacklog() {
		double served = Math.min(availableCapacity, backlogUnits);
		availableCapacity -= served;
		backlogUnits -= served;
		if (backlogUnits < EPSILON) {
			backlogUnits = 0.0;
		}
		return served;
	}

	private static double reviewDemand(Bill bill, VoteContext context) {
		double routingRisk = AdaptiveTrackProcess.riskScore(bill, context);
		double harmRisk = AffectedGroupScoring.minorityHarm(bill);
		double captureRisk = LobbyCaptureScoring.captureRisk(bill);
		double signalConflict = Math.abs(bill.publicSupport() - bill.publicBenefit());
		return Math.max(0.25,
				0.48
						+ (1.10 * routingRisk)
						+ (0.52 * harmRisk)
						+ (0.42 * captureRisk)
						+ (0.38 * bill.publicBenefitUncertainty())
						+ (0.30 * signalConflict)
						+ (0.12 * bill.publicSignalMovement())
		);
	}

	public record CapacitySnapshot(
			double capacityUnits,
			double availableCapacity,
			double backlogUnits,
			double cumulativeDemandUnits,
			double cumulativeQueuePressure,
			int consideredCases,
			int defendedCases,
			int overflowFallbackCases,
			int overloadEvents,
			int recoveryEvents,
			boolean everOverloaded,
			boolean fullReviewReady
	) {
		public double remainingCapacityShare() {
			return availableCapacity / capacityUnits;
		}
	}
}
