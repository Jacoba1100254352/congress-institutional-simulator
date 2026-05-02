package congresssim.calibration;

import congresssim.simulation.Scenario;
import congresssim.simulation.catalog.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;
import congresssim.reporting.ReportProvenance;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public final class CalibrationRunner {
    private static final List<String> CALIBRATION_SCENARIOS = List.of(
            "simple-majority",
            "bicameral-majority",
            "presidential-veto",
            "current-system",
            "default-pass-budgeted-lobbying"
    );

    private CalibrationRunner() {
    }

    public static CalibrationRunResult run(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        Files.createDirectories(outputDir);
        WorldSpec worldSpec = new WorldSpec(
                legislators,
                bills,
                2,
                0.76,
                0.74,
                0.48,
                0.62,
                0.46
        );
        List<Scenario> scenarios = ScenarioCatalog.scenariosForKeys(CALIBRATION_SCENARIOS);
        List<ScenarioReport> reports = new Simulator().compare(scenarios, worldSpec, runs, seed);
        Map<String, ScenarioReport> reportByScenario = new LinkedHashMap<>();
        for (int index = 0; index < CALIBRATION_SCENARIOS.size(); index++) {
            reportByScenario.put(CALIBRATION_SCENARIOS.get(index), reports.get(index));
        }

        List<CalibrationRow> rows = new ArrayList<>();
        for (CalibrationBenchmark benchmark : CalibrationTargetCatalog.benchmarkRanges()) {
            ScenarioReport report = reportByScenario.get(benchmark.scenarioKey());
            if (report == null) {
                continue;
            }
            double observed = metricValue(report, benchmark.simulatorMetric(), runs);
            rows.add(new CalibrationRow(
                    benchmark,
                    observed,
                    observed >= benchmark.minimum() && observed <= benchmark.maximum()
            ));
        }

        CalibrationRunResult result = new CalibrationRunResult(
                rows,
                outputDir.resolve("calibration-baseline.csv"),
                outputDir.resolve("calibration-baseline.md"),
                outputDir.resolve("calibration-baseline-manifest.json")
        );
        Files.writeString(result.csvPath(), csv(result));
        Files.writeString(result.markdownPath(), markdown(result, runs, legislators, bills, seed));
        ReportProvenance.write(
                result.manifestPath(),
                "Calibration Baseline",
                runs,
                legislators,
                bills,
                seed,
                1,
                CALIBRATION_SCENARIOS.size(),
                List.of(result.csvPath(), result.markdownPath())
        );
        return result;
    }

    private static double metricValue(ScenarioReport report, String metric, int runs) {
        return switch (metric) {
            case "productivity" -> report.productivity();
            case "floor" -> report.floorConsiderationRate();
            case "averageEnactedSupport" -> report.averageEnactedSupport();
            case "vetoesPerRun" -> (double) report.vetoes() / runs;
            case "proposerAccessGini" -> report.proposerAccessGini();
            case "lobbySpendPerBill" -> report.lobbySpendPerBill();
            case "welfarePerSubmittedBill" -> report.welfarePerSubmittedBill();
            default -> throw new IllegalArgumentException("Unsupported calibration metric: " + metric);
        };
    }

    private static String csv(CalibrationRunResult result) {
        StringBuilder builder = new StringBuilder();
        builder.append("key,dataset,quantity,scenarioKey,metric,minimum,maximum,observed,passed,source,notes\n");
        for (CalibrationRow row : result.rows()) {
            CalibrationBenchmark benchmark = row.benchmark();
            builder.append(csvValue(benchmark.key())).append(',')
                    .append(csvValue(benchmark.empiricalDataset())).append(',')
                    .append(csvValue(benchmark.empiricalQuantity())).append(',')
                    .append(csvValue(benchmark.scenarioKey())).append(',')
                    .append(csvValue(benchmark.simulatorMetric())).append(',')
                    .append(format(benchmark.minimum())).append(',')
                    .append(format(benchmark.maximum())).append(',')
                    .append(format(row.observed())).append(',')
                    .append(row.passed()).append(',')
                    .append(csvValue(benchmark.source())).append(',')
                    .append(csvValue(benchmark.notes())).append('\n');
        }
        return builder.toString();
    }

    private static String markdown(
            CalibrationRunResult result,
            int runs,
            int legislators,
            int bills,
            long seed
    ) {
        long passed = result.rows().stream().filter(CalibrationRow::passed).count();
        StringBuilder builder = new StringBuilder();
        builder.append("# Calibration Baseline\n\n");
        builder.append("Executable empirical-screening run for the conventional simulator baseline. This is not a claim that the model is fully fitted to Congress; it is a reproducible pass/fail check against explicit benchmark ranges derived from named empirical datasets.\n\n");
        builder.append("## Run Configuration\n\n");
        builder.append("- runs: ").append(runs).append('\n');
        builder.append("- legislators: ").append(legislators).append('\n');
        builder.append("- bills per run: ").append(bills).append('\n');
        builder.append("- seed: ").append(seed).append('\n');
        builder.append("- scenarios: ").append(String.join(", ", CALIBRATION_SCENARIOS)).append("\n\n");
        builder.append("## Summary\n\n");
        builder.append("- passed checks: ").append(passed).append(" / ").append(result.rows().size()).append("\n\n");
        builder.append("| Check | Scenario | Metric | Range | Observed | Pass |\n");
        builder.append("| --- | --- | --- | ---: | ---: | --- |\n");
        for (CalibrationRow row : result.rows()) {
            CalibrationBenchmark benchmark = row.benchmark();
            builder.append("| ")
                    .append(benchmark.key()).append(" | ")
                    .append(benchmark.scenarioKey()).append(" | ")
                    .append(benchmark.simulatorMetric()).append(" | ")
                    .append(format(benchmark.minimum())).append("--").append(format(benchmark.maximum())).append(" | ")
                    .append(format(row.observed())).append(" | ")
                    .append(row.passed() ? "yes" : "no").append(" |\n");
        }
        builder.append("\n## Sources\n\n");
        for (CalibrationRow row : result.rows()) {
            CalibrationBenchmark benchmark = row.benchmark();
            builder.append("- ").append(benchmark.key()).append(": ")
                    .append(benchmark.source()).append(". ")
                    .append(benchmark.notes()).append('\n');
        }
        return builder.toString();
    }

    private static String csvValue(String value) {
        if (value.contains(",") || value.contains("\"") || value.contains("\n")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }

    private static String format(double value) {
        return String.format(Locale.ROOT, "%.3f", value);
    }

    public record CalibrationRunResult(
            List<CalibrationRow> rows,
            Path csvPath,
            Path markdownPath,
            Path manifestPath
    ) {
        public CalibrationRunResult {
            rows = List.copyOf(rows);
        }
    }

    public record CalibrationRow(
            CalibrationBenchmark benchmark,
            double observed,
            boolean passed
    ) {
    }
}
