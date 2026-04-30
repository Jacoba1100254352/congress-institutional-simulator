package congresssim.calibration;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public final class CalibrationTargetCatalog {
    private static final Path BENCHMARK_FILE = Path.of("data", "calibration", "empirical-benchmarks.csv");

    private CalibrationTargetCatalog() {
    }

    public static List<CalibrationBenchmark> benchmarkRanges() {
        if (Files.exists(BENCHMARK_FILE)) {
            try {
                return benchmarkRangesFromCsv(BENCHMARK_FILE);
            } catch (IOException exception) {
                throw new IllegalStateException("Unable to read calibration benchmark file: " + BENCHMARK_FILE, exception);
            }
        }
        return embeddedBenchmarkRanges();
    }

    public static Path benchmarkFile() {
        return BENCHMARK_FILE;
    }

    private static List<CalibrationBenchmark> benchmarkRangesFromCsv(Path path) throws IOException {
        List<String> lines = Files.readAllLines(path).stream()
                .map(String::trim)
                .filter(line -> !line.isEmpty() && !line.startsWith("#"))
                .toList();
        if (lines.size() < 2) {
            throw new IllegalArgumentException("Calibration benchmark file must include a header and at least one row.");
        }
        return lines.stream()
                .skip(1)
                .map(CalibrationTargetCatalog::parseBenchmarkCsvRow)
                .toList();
    }

    private static CalibrationBenchmark parseBenchmarkCsvRow(String line) {
        String[] columns = line.split(",", -1);
        if (columns.length != 9) {
            throw new IllegalArgumentException("Calibration benchmark row must have 9 columns: " + line);
        }
        return new CalibrationBenchmark(
                columns[0],
                columns[1],
                columns[2],
                columns[3],
                columns[4],
                Double.parseDouble(columns[5]),
                Double.parseDouble(columns[6]),
                columns[7],
                columns[8]
        );
    }

    private static List<CalibrationBenchmark> embeddedBenchmarkRanges() {
        return List.of(
                new CalibrationBenchmark(
                        "current-system-enactment-rate",
                        "Congress.gov and govinfo bill histories",
                        "share of introduced bills that become law in recent U.S. Congresses",
                        "current-system",
                        "productivity",
                        0.01,
                        0.12,
                        "Congress.gov bill-status bulk data and govinfo BILLS/BILLSTATUS collections",
                        "Broad screening range for stylized U.S.-like conventional attrition; exact Congress-specific targets should be fitted from raw bill histories."
                ),
                new CalibrationBenchmark(
                        "current-system-floor-load",
                        "Congress.gov and govinfo bill histories",
                        "share of introduced bills receiving floor consideration or final chamber action",
                        "current-system",
                        "floor",
                        0.05,
                        0.45,
                        "Congress.gov bill-status bulk data and govinfo BILLS/BILLSTATUS collections",
                        "Used to keep the benchmark from treating every introduced bill as a floor bill."
                ),
                new CalibrationBenchmark(
                        "party-unity-support-band",
                        "Voteview roll-call votes",
                        "ordinary enacted-bill coalition support range under a polarized Congress",
                        "current-system",
                        "averageEnactedSupport",
                        0.50,
                        0.82,
                        "Voteview roll-call and party-unity data",
                        "Screens whether party loyalty and polarization generate plausible winning coalition support."
                ),
                new CalibrationBenchmark(
                        "veto-frequency-band",
                        "Congress.gov veto actions and CRS presidential veto summaries",
                        "vetoes per simulated run under bicameral presidential-veto baseline",
                        "presidential-veto",
                        "vetoesPerRun",
                        0.00,
                        8.00,
                        "Congress.gov action histories and CRS presidential veto summaries",
                        "Loose range because run length is abstract; failures here indicate a wildly implausible veto model."
                ),
                new CalibrationBenchmark(
                        "sponsor-success-concentration",
                        "Center for Effective Lawmaking",
                        "concentration in member-level legislative advancement and sponsor success",
                        "current-system",
                        "proposerAccessGini",
                        0.05,
                        0.75,
                        "Center for Effective Lawmaking member-level effectiveness scores",
                        "Screens whether proposer access is neither perfectly equal nor fully concentrated."
                ),
                new CalibrationBenchmark(
                        "lobbying-spend-observable",
                        "U.S. Senate Lobbying Disclosure Act data",
                        "organized-interest spending should be visible in explicit lobbying scenarios",
                        "default-pass-budgeted-lobbying",
                        "lobbySpendPerBill",
                        0.01,
                        1.50,
                        "U.S. Senate Lobbying Disclosure Act filings",
                        "The simulator uses abstract budget units; this validates observability and relative scale, not dollar calibration."
                ),
                new CalibrationBenchmark(
                        "topic-throughput-yield",
                        "Comparative Agendas Project",
                        "policy-topic throughput should not collapse to zero in conventional baselines",
                        "simple-majority",
                        "welfarePerSubmittedBill",
                        0.05,
                        0.45,
                        "Comparative Agendas Project topic coding",
                        "A coarse screen for generated issue-domain throughput before topic-specific calibration."
                )
        );
    }

    public static List<CalibrationTarget> standardTargets() {
        return List.of(
                new CalibrationTarget(
                        "voteview-party-unity",
                        "Voteview roll-call votes",
                        "party-unity rates and coalition-size distributions by Congress",
                        "averageEnactedSupport, party-position spread, chamber vote shares",
                        "Tune generated party loyalty and polarization so ordinary majority scenarios produce plausible coalition patterns.",
                        "This target supports representation and compromise calibration, not normative scoring."
                ),
                new CalibrationTarget(
                        "congressgov-bill-attrition",
                        "Congress.gov and govinfo bill histories",
                        "introduced, referred, reported, passed, vetoed, and enacted bill counts",
                        "floorConsiderationRate, accessDenialRate, committeeRejectionRate, productivity, vetoes",
                        "Check whether ordinary procedural baselines produce plausible attrition before testing counterfactual institutions.",
                        "Topic-specific attrition should be checked separately once issue domains are calibrated."
                ),
                new CalibrationTarget(
                        "comparative-agendas-topic-throughput",
                        "Comparative Agendas Project",
                        "agenda attention and policy-topic throughput over time",
                        "issue-domain bill shares, enacted bill diversity, welfarePerSubmittedBill",
                        "Calibrate issue-domain generation and topic throughput so simulated campaigns are not dominated by one generated domain.",
                        "The current simulator has abstract domains; this is a mapping target for later empirical work."
                ),
                new CalibrationTarget(
                        "parlgov-party-system",
                        "ParlGov party-system data",
                        "party counts, governing-party concentration, and party-family seat shares",
                        "partySystemProfile, partySystemWeight, party seat shares, party-position spread",
                        "Ground weighted party-system sensitivity cases instead of treating two-party and multiparty assumptions equally.",
                        "This is especially relevant for v18-style weighted cases."
                ),
                new CalibrationTarget(
                        "lobbying-disclosure-spend",
                        "U.S. lobbying disclosure data",
                        "client, issue, and sector lobbying expenditure distributions",
                        "lobbySpendPerBill, defensiveLobbyingShare, channel spend shares, captureReturnOnSpend",
                        "Constrain explicit lobby-group budgets and channel reallocations before making claims about anti-capture designs.",
                        "The simulator should compare spending distributions, not infer causality from disclosure totals alone."
                ),
                new CalibrationTarget(
                        "effective-lawmaking-sponsor-success",
                        "Center for Effective Lawmaking",
                        "sponsor effectiveness and bill-advancement success by member and chamber",
                        "proposerAccessGini, welfarePerSubmittedBill, enacted bills by proposer",
                        "Check whether proposer access and success concentration look plausible in conventional baselines.",
                        "This target helps interpret earned credits and proposal bonds."
                ),
                new CalibrationTarget(
                        "v-dem-institutional-constraints",
                        "V-Dem institutional indicators",
                        "executive constraints, party institutionalization, and deliberative components",
                        "scenario case weights, veto frequency, legitimacyScore, publicAlignmentScore",
                        "Use broad cross-national indicators for sensitivity analysis rather than direct U.S.-Congress validation.",
                        "This is a coarse external-context target."
                )
        );
    }
}
