package congresssim.simulation.catalog;


import congresssim.simulation.Scenario;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;


/**
 * Emits the locked House agenda-control route-calibration grid.
 */
public final class HouseAgendaControlCalibrationProbe
{
	private record Candidate(
			double calendarPriority,
			double specialRuleThreshold,
			double suspensionThreshold
	) {
	}

	private HouseAgendaControlCalibrationProbe() {
	}

	public static void main(String[] args) {
		if (args.length != 5) {
			throw new IllegalArgumentException(
					"Usage: HouseAgendaControlCalibrationProbe <runs> <comma-separated-seeds> "
							+ "<comma-separated-calendar-thresholds> <comma-separated-special-thresholds> "
							+ "<comma-separated-suspension-thresholds>"
			);
		}
		int runs = Integer.parseInt(args[0]);
		if (runs <= 0) {
			throw new IllegalArgumentException("runs must be positive");
		}
		long[] seeds = parseLongs(args[1]);
		double[] calendarThresholds = parseDoubles(args[2]);
		double[] specialThresholds = parseDoubles(args[3]);
		double[] suspensionThresholds = parseDoubles(args[4]);
		List<Candidate> candidates = candidates(
				calendarThresholds,
				specialThresholds,
				suspensionThresholds
		);
		List<Scenario> scenarios = candidates.stream()
				.map(candidate -> ChamberCommitteeScenarioBuilders.stylizedCurrentCongressWorkflow(
						candidate.calendarPriority(),
						candidate.specialRuleThreshold(),
						candidate.suspensionThreshold()
				))
				.toList();
		WorldSpec world = new WorldSpec(
				101,
				60,
				2,
				0.76,
				0.74,
				0.48,
				0.62,
				0.46
		);
		Simulator simulator = new Simulator();

		System.out.println(
				"calendarPriorityThreshold,specialRuleThreshold,suspensionThreshold,seed,runs,bills,"
						+ "committeeAdvanceRate,floorConsiderationRate,advanceToFloorRate,enactmentRate,"
						+ "specialRuleOnlyRouteRate,suspensionOnlyRouteRate,"
						+ "mixedSpecialRuleAndSuspensionRouteRate,otherFloorRouteRate,floorRouteAssignmentRate,"
						+ "specialRuleOnlyRouteShare,suspensionOnlyRouteShare,"
						+ "mixedSpecialRuleAndSuspensionRouteShare,otherFloorRouteShare,"
						+ "restrictiveSpecialRuleRouteRate,restrictiveSpecialRuleShare,"
						+ "closedRuleRate,openRuleRate,calendarCapacityDenialRate"
		);
		for (long seed : seeds) {
			List<ScenarioReport> reports = simulator.compare(scenarios, world, runs, seed);
			for (int index = 0; index < candidates.size(); index++) {
				writeRow(candidates.get(index), seed, runs, reports.get(index));
			}
		}
	}

	private static void writeRow(Candidate candidate, long seed, int runs, ScenarioReport report) {
		double committeeAdvance = report.supplementalMetric("committeeAdvanceRate");
		double floor = report.floorConsiderationRate();
		double special = report.supplementalMetric("specialRuleOnlyRouteRate");
		double suspension = report.supplementalMetric("suspensionOnlyRouteRate");
		double mixed = report.supplementalMetric("mixedSpecialRuleAndSuspensionRouteRate");
		double other = report.supplementalMetric("otherFloorRouteRate");
		double assigned = report.supplementalMetric("floorRouteAssignmentRate");
		double routeTotal = special + suspension + mixed + other;
		if (Math.abs(routeTotal - floor) > 1e-12 || Math.abs(assigned - floor) > 1e-12) {
			throw new IllegalStateException(
					"Modeled floor routes must be exclusive and exhaustive: floor=" + floor
							+ ", routeTotal=" + routeTotal + ", assigned=" + assigned
			);
		}
		double specialDenominator = special + mixed;
		double restrictiveRate = report.supplementalMetric("restrictiveSpecialRuleRouteRate");
		double advanceToFloor = committeeAdvance == 0.0 ? 0.0 : floor / committeeAdvance;
		double specialShare = floor == 0.0 ? 0.0 : special / floor;
		double suspensionShare = floor == 0.0 ? 0.0 : suspension / floor;
		double mixedShare = floor == 0.0 ? 0.0 : mixed / floor;
		double otherShare = floor == 0.0 ? 0.0 : other / floor;
		double restrictiveShare = specialDenominator == 0.0 ? 0.0 : restrictiveRate / specialDenominator;

		System.out.printf(
				Locale.ROOT,
				"%.3f,%.3f,%.3f,%d,%d,%d,"
						+ "%.15f,%.15f,%.15f,%.15f,"
						+ "%.15f,%.15f,%.15f,%.15f,%.15f,"
						+ "%.15f,%.15f,%.15f,%.15f,"
						+ "%.15f,%.15f,%.15f,%.15f,%.15f%n",
				candidate.calendarPriority(),
				candidate.specialRuleThreshold(),
				candidate.suspensionThreshold(),
				seed,
				runs,
				report.totalBills(),
				committeeAdvance,
				floor,
				advanceToFloor,
				report.productivity(),
				special,
				suspension,
				mixed,
				other,
				assigned,
				specialShare,
				suspensionShare,
				mixedShare,
				otherShare,
				restrictiveRate,
				restrictiveShare,
				report.supplementalMetric("closedRuleRate"),
				report.supplementalMetric("openRuleRate"),
				report.supplementalMetric("calendarCapacityDenialRate")
		);
	}

	private static List<Candidate> candidates(
			double[] calendarThresholds,
			double[] specialThresholds,
			double[] suspensionThresholds
	) {
		List<Candidate> candidates = new ArrayList<>();
		for (double calendarThreshold : calendarThresholds) {
			for (double specialThreshold : specialThresholds) {
				for (double suspensionThreshold : suspensionThresholds) {
					candidates.add(new Candidate(
							calendarThreshold,
							specialThreshold,
							suspensionThreshold
					));
				}
			}
		}
		return List.copyOf(candidates);
	}

	private static long[] parseLongs(String text) {
		String[] values = text.split(",");
		long[] parsed = new long[values.length];
		for (int index = 0; index < values.length; index++) {
			parsed[index] = Long.parseLong(values[index].trim());
		}
		return parsed;
	}

	private static double[] parseDoubles(String text) {
		String[] values = text.split(",");
		double[] parsed = new double[values.length];
		for (int index = 0; index < values.length; index++) {
			parsed[index] = Double.parseDouble(values[index].trim());
		}
		return parsed;
	}
}
