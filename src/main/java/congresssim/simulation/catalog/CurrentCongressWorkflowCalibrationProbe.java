package congresssim.simulation.catalog;


import congresssim.simulation.Scenario;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;

import java.util.List;
import java.util.Locale;


/**
 * Emits a compact deterministic parameter grid for the publication-facing
 * current-Congress workflow calibration report.
 */
public final class CurrentCongressWorkflowCalibrationProbe
{
	private CurrentCongressWorkflowCalibrationProbe() {
	}

	public static void main(String[] args) {
		if (args.length != 3) {
			throw new IllegalArgumentException(
					"Usage: CurrentCongressWorkflowCalibrationProbe <runs> <comma-separated-seeds> <comma-separated-thresholds>"
			);
		}
		int runs = Integer.parseInt(args[0]);
		if (runs <= 0) {
			throw new IllegalArgumentException("runs must be positive");
		}
		long[] seeds = parseLongs(args[1]);
		double[] thresholds = parseDoubles(args[2]);
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
		double defaultThreshold = ChamberCommitteeScenarioBuilders.currentCongressCalendarPriority();

		System.out.println(
				"threshold,seed,runs,bills,defaultThreshold,committeeAdvanceRate,floorConsiderationRate,enactmentRate,calendarCapacityDenialRate"
		);
		for (double threshold : thresholds) {
			for (long seed : seeds) {
				Scenario scenario = ChamberCommitteeScenarioBuilders.stylizedCurrentCongressWorkflow(threshold);
				ScenarioReport report = simulator.compare(List.of(scenario), world, runs, seed).getFirst();
				System.out.printf(
						Locale.ROOT,
						"%.3f,%d,%d,%d,%.3f,%.6f,%.6f,%.6f,%.6f%n",
						threshold,
						seed,
						runs,
						report.totalBills(),
						defaultThreshold,
						report.supplementalMetric("committeeAdvanceRate"),
						report.floorConsiderationRate(),
						report.productivity(),
						report.supplementalMetric("calendarCapacityDenialRate")
				);
			}
		}
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
