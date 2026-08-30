package congresssim.calibration;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;


public final class CalibrationTargetCatalog
{
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
						"current-congress-committee-advance-rate",
						"GovInfo 117th-Congress H.R. and S. bill census",
						"share of introduced bills ordered reported reported or discharged",
						"current-congress-workflow",
						"committeeAdvanceRate",
						0.079,
						0.120,
						"GovInfo BILLSTATUS 117th-Congress H.R. and S. census",
						"Range centered on the deterministic calibration split with a 0.020 abstraction tolerance; held-out rows were not used to select the threshold."
				),
				new CalibrationBenchmark(
						"current-congress-floor-consideration-rate",
						"GovInfo 117th-Congress H.R. and S. bill census",
						"share of introduced bills receiving substantive floor consideration",
						"current-congress-workflow",
						"floor",
						0.05,
						0.081,
						"GovInfo BILLSTATUS 117th-Congress H.R. and S. census",
						"Range centered on the deterministic calibration split with a 0.015 abstraction tolerance; held-out rows were not used to select the threshold."
				),
				new CalibrationBenchmark(
						"current-congress-enactment-rate",
						"GovInfo 117th-Congress H.R. and S. bill census",
						"share of introduced bills enacted",
						"current-congress-workflow",
						"productivity",
						0.012,
						0.033,
						"GovInfo BILLSTATUS 117th-Congress H.R. and S. census",
						"Range centered on the deterministic calibration split with a 0.010 abstraction tolerance; held-out rows were not used to select the threshold."
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
				),
				new CalibrationBenchmark(
						"district-public-will-alignment",
						"Cumulative CES Common Content district aggregates",
						"district support and turnout signals should be visible in public-will scenarios",
						"district-population-majority",
						"districtAlignment",
						0.20,
						0.80,
						"CES district-level survey aggregates",
						"Abstract public-will alignment screen using district proxy data, not bill-specific support validation."
				),
				new CalibrationBenchmark(
						"district-turnout-skew-proxy",
						"Cumulative CES Common Content district aggregates",
						"turnout skew should stay finite in district public-will scenarios",
						"district-population-majority",
						"turnoutSkewIndex",
						0.00,
						0.40,
						"CES district-level survey aggregates",
						"Coarse turnout-skew screen using district proxy data, not a voter-file validation."
				),
				new CalibrationBenchmark(
						"campaign-finance-observable-band",
						"OpenFEC campaign-finance extracts",
						"campaign-finance pressure should be visible in influence-system scenarios",
						"influence-system-majority",
						"campaignFinanceCaptureIndex",
						0.00,
						1.00,
						"OpenFEC Schedule A and Schedule E bounded extracts",
						"Unit-scale observability band for campaign-finance influence metrics, not causal capture calibration."
				),
				new CalibrationBenchmark(
						"judicial-review-constraint",
						"Supreme Court Database merits cases",
						"constitutional invalidation should stay within a broad merits-case plausibility band",
						"constitutional-court-architecture-majority",
						"constitutionalInvalidationRate",
						0.00,
						0.20,
						"Supreme Court Database case-centered release",
						"Broad upper-bound screen for merits-case invalidation, not emergency-order validation."
				),
				new CalibrationBenchmark(
						"implementation-delay-proxy",
						"Federal Register final-rule effective-date sample",
						"implementation-delay proxy should remain finite and nonnegative",
						"law-registry-majority",
						"implementationDelay",
						0.00,
						100.00,
						"Federal Register final-rule publication and effective-date extract",
						"Abstract delay screen linked to final-to-effective-date rows, not full administrative implementation validation."
				),
				new CalibrationBenchmark(
						"implementation-capacity-proxy",
						"Federal Register final-rule effective-date sample",
						"implementation-capacity proxy should remain on the unit scale",
						"law-registry-majority",
						"implementationCapacity",
						0.00,
						1.00,
						"Federal Register final-rule publication and effective-date extract",
						"Abstract capacity screen derived from effective-date speed, not enforcement validation."
				),
				new CalibrationBenchmark(
						"law-revision-correction-proxy",
						"Congress.gov public-law text flags",
						"post-enactment correction or revision should be represented in law-registry scenarios",
						"law-registry-majority",
						"reversalRate",
						0.00,
						0.80,
						"Congress.gov public-law title and summary flags",
						"Broad correction-rate proxy for amendment, repeal, reauthorization, and sunset language, not statutory-lineage validation."
				),
				new CalibrationBenchmark(
						"bicameral-veto-burden",
						"QoG and V-Dem comparative institutional profiles",
						"bicameral conflict should be visible in bicameral scenarios",
						"bicameral-majority",
						"interChamberConflictRate",
						0.05,
						0.60,
						"QoG DES POLCON and OWID V-Dem selected profiles",
						"Coarse bicameral-burden screen, not cross-national productivity validation."
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
						"The simulator has abstract domains; this is a mapping target for later empirical work."
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
