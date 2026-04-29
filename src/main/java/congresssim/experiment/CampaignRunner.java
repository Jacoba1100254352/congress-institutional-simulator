package congresssim.experiment;

import congresssim.simulation.Scenario;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public final class CampaignRunner {
    private static final List<String> CORE_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-access",
            "default-pass-committee",
            "default-pass-guarded",
            "default-pass-informed-guarded",
            "bicameral-majority",
            "presidential-veto"
    );

    private CampaignRunner() {
    }

    public static CampaignResult runV0(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        Files.createDirectories(outputDir);

        List<ExperimentCase> cases = v0Cases(legislators, bills);
        List<Scenario> scenarios = ScenarioCatalog.scenariosForKeys(CORE_SCENARIOS);
        Simulator simulator = new Simulator();
        List<CampaignRow> rows = new ArrayList<>();

        for (int caseIndex = 0; caseIndex < cases.size(); caseIndex++) {
            ExperimentCase experimentCase = cases.get(caseIndex);
            List<ScenarioReport> reports = simulator.compare(
                    scenarios,
                    experimentCase.worldSpec(),
                    runs,
                    seed + (10_000L * caseIndex)
            );
            for (int scenarioIndex = 0; scenarioIndex < reports.size(); scenarioIndex++) {
                rows.add(new CampaignRow(
                        experimentCase.key(),
                        experimentCase.name(),
                        experimentCase.description(),
                        CORE_SCENARIOS.get(scenarioIndex),
                        reports.get(scenarioIndex)
                ));
            }
        }

        CampaignResult result = new CampaignResult(
                "Simulation Campaign v0",
                rows,
                outputDir.resolve("simulation-campaign-v0.csv"),
                outputDir.resolve("simulation-campaign-v0.md")
        );
        Files.writeString(result.csvPath(), csv(result));
        Files.writeString(result.markdownPath(), markdown(result, runs, legislators, bills, seed));
        return result;
    }

    private static List<ExperimentCase> v0Cases(int legislators, int bills) {
        return List.of(
                experiment("baseline", "Baseline", "Moderately polarized three-party legislature.",
                        legislators, bills, 3, 0.72, 0.68, 0.48, 0.64, 0.52),
                experiment("low-polarization", "Low Polarization", "Legislators are less ideologically clustered.",
                        legislators, bills, 3, 0.25, 0.55, 0.48, 0.64, 0.62),
                experiment("high-polarization", "High Polarization", "Legislators are tightly clustered into ideological camps.",
                        legislators, bills, 3, 0.92, 0.80, 0.48, 0.58, 0.34),
                experiment("low-party-loyalty", "Low Party Loyalty", "Party pressure is weak and legislators act more independently.",
                        legislators, bills, 3, 0.72, 0.25, 0.48, 0.64, 0.52),
                experiment("high-party-loyalty", "High Party Loyalty", "Party pressure is strong.",
                        legislators, bills, 3, 0.72, 0.90, 0.48, 0.64, 0.52),
                experiment("low-compromise", "Low Compromise Culture", "Members are less inclined toward moderate, incremental bills.",
                        legislators, bills, 3, 0.72, 0.68, 0.48, 0.64, 0.18),
                experiment("high-compromise", "High Compromise Culture", "Members are more inclined toward moderate, incremental bills.",
                        legislators, bills, 3, 0.72, 0.55, 0.38, 0.70, 0.86),
                experiment("low-lobbying", "Low Lobbying Pressure", "Lobby pressure is weak.",
                        legislators, bills, 3, 0.72, 0.68, 0.12, 0.64, 0.52),
                experiment("high-lobbying", "High Lobbying Pressure", "Lobby pressure is strong.",
                        legislators, bills, 3, 0.72, 0.68, 0.88, 0.54, 0.44),
                experiment("weak-constituency", "Weak Constituency Pressure", "Members are less responsive to public support.",
                        legislators, bills, 3, 0.72, 0.68, 0.48, 0.20, 0.52),
                experiment("two-party", "Two-Party System", "Generated legislators sort into two broad parties.",
                        legislators, bills, 2, 0.72, 0.72, 0.48, 0.64, 0.52),
                experiment("multi-party", "Multi-Party System", "Generated legislators sort into five parties.",
                        legislators, bills, 5, 0.72, 0.58, 0.48, 0.64, 0.58)
        );
    }

    private static ExperimentCase experiment(
            String key,
            String name,
            String description,
            int legislators,
            int bills,
            int parties,
            double polarization,
            double partyLoyalty,
            double lobbying,
            double constituency,
            double compromise
    ) {
        return new ExperimentCase(
                key,
                name,
                description,
                new WorldSpec(
                        legislators,
                        bills,
                        parties,
                        polarization,
                        partyLoyalty,
                        lobbying,
                        constituency,
                        compromise
                )
        );
    }

    private static String csv(CampaignResult result) {
        StringBuilder builder = new StringBuilder();
        builder.append("caseKey,caseName,caseDescription,scenarioKey,scenario,totalBills,enactedBills,productivity,floor,avgSupport,welfare,cooperation,compromise,gridlock,accessDenied,committeeRejected,lowSupport,popularFail,policyShift,proposerGain,vetoes,overriddenVetoes\n");
        for (CampaignRow row : result.rows()) {
            ScenarioReport report = row.report();
            builder.append(csvValue(row.caseKey())).append(',')
                    .append(csvValue(row.caseName())).append(',')
                    .append(csvValue(row.caseDescription())).append(',')
                    .append(csvValue(row.scenarioKey())).append(',')
                    .append(csvValue(report.scenarioName())).append(',')
                    .append(report.totalBills()).append(',')
                    .append(report.enactedBills()).append(',')
                    .append(format(report.productivity())).append(',')
                    .append(format(report.floorConsiderationRate())).append(',')
                    .append(format(report.averageEnactedSupport())).append(',')
                    .append(format(report.averagePublicBenefit())).append(',')
                    .append(format(report.cooperationScore())).append(',')
                    .append(format(report.compromiseScore())).append(',')
                    .append(format(report.gridlockRate())).append(',')
                    .append(format(report.accessDenialRate())).append(',')
                    .append(format(report.committeeRejectionRate())).append(',')
                    .append(format(report.controversialPassageRate())).append(',')
                    .append(format(report.popularBillFailureRate())).append(',')
                    .append(format(report.averagePolicyShift())).append(',')
                    .append(format(report.averageProposerGain())).append(',')
                    .append(report.vetoes()).append(',')
                    .append(report.overriddenVetoes()).append('\n');
        }
        return builder.toString();
    }

    private static String markdown(
            CampaignResult result,
            int runs,
            int legislators,
            int bills,
            long seed
    ) {
        Map<String, ScenarioAggregate> aggregateByScenario = aggregateByScenario(result.rows());
        StringBuilder builder = new StringBuilder();
        builder.append("# Simulation Campaign v0\n\n");
        builder.append("Deterministic batch campaign for comparing institutional regimes across assumption sweeps.\n\n");
        builder.append("## Run Configuration\n\n");
        builder.append("- runs per case: ").append(runs).append('\n');
        builder.append("- legislators: ").append(legislators).append('\n');
        builder.append("- bills per run: ").append(bills).append('\n');
        builder.append("- base seed: ").append(seed).append('\n');
        builder.append("- scenarios per case: ").append(CORE_SCENARIOS.size()).append('\n');
        builder.append("- experiment cases: ").append(caseCount(result.rows())).append("\n\n");

        builder.append("## Headline Findings\n\n");
        appendHeadlineFindings(builder, result.rows(), aggregateByScenario);

        builder.append("## Scenario Averages Across Cases\n\n");
        builder.append("| Scenario | Productivity | Welfare | Low-support | Policy shift | Proposer gain | Floor |\n");
        builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |\n");
        aggregateByScenario.values()
                .stream()
                .sorted(Comparator.comparing(ScenarioAggregate::scenarioKey))
                .forEach(summary -> builder.append("| ")
                        .append(summary.scenarioName()).append(" | ")
                        .append(format(summary.productivity())).append(" | ")
                        .append(format(summary.welfare())).append(" | ")
                        .append(format(summary.lowSupport())).append(" | ")
                        .append(format(summary.policyShift())).append(" | ")
                        .append(format(summary.proposerGain())).append(" | ")
                        .append(format(summary.floor())).append(" |\n"));
        builder.append('\n');

        builder.append("## Default-Pass Guardrail Deltas\n\n");
        builder.append("Delta values compare `default-pass-informed-guarded` against open `default-pass` in the same case. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity losses are the tradeoff.\n\n");
        builder.append("| Case | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |\n");
        builder.append("| --- | ---: | ---: | ---: | ---: | ---: |\n");
        for (String caseKey : caseKeys(result.rows())) {
            CampaignRow open = find(result.rows(), caseKey, "default-pass");
            CampaignRow guarded = find(result.rows(), caseKey, "default-pass-informed-guarded");
            if (open != null && guarded != null) {
                builder.append("| ")
                        .append(open.caseName()).append(" | ")
                        .append(format(guarded.report().productivity() - open.report().productivity())).append(" | ")
                        .append(format(guarded.report().averagePublicBenefit() - open.report().averagePublicBenefit())).append(" | ")
                        .append(format(guarded.report().controversialPassageRate() - open.report().controversialPassageRate())).append(" | ")
                        .append(format(guarded.report().averagePolicyShift() - open.report().averagePolicyShift())).append(" | ")
                        .append(format(guarded.report().averageProposerGain() - open.report().averageProposerGain())).append(" |\n");
            }
        }
        builder.append('\n');

        builder.append("## Case Highlights\n\n");
        builder.append("| Case | Best welfare | Most productive | Lowest low-support passage |\n");
        builder.append("| --- | --- | --- | --- |\n");
        for (String caseKey : caseKeys(result.rows())) {
            List<CampaignRow> caseRows = rowsForCase(result.rows(), caseKey);
            CampaignRow bestWelfare = max(caseRows, Comparator.comparingDouble(row -> row.report().averagePublicBenefit()));
            CampaignRow mostProductive = max(caseRows, Comparator.comparingDouble(row -> row.report().productivity()));
            CampaignRow lowestLowSupport = min(caseRows, Comparator.comparingDouble(row -> row.report().controversialPassageRate()));
            builder.append("| ")
                    .append(caseRows.get(0).caseName()).append(" | ")
                    .append(bestWelfare.report().scenarioName()).append(" (").append(format(bestWelfare.report().averagePublicBenefit())).append(") | ")
                    .append(mostProductive.report().scenarioName()).append(" (").append(format(mostProductive.report().productivity())).append(") | ")
                    .append(lowestLowSupport.report().scenarioName()).append(" (").append(format(lowestLowSupport.report().controversialPassageRate())).append(") |\n");
        }
        builder.append('\n');

        builder.append("## Interpretation\n\n");
        builder.append("- Open default-pass is consistently the throughput leader, but it also carries high low-support passage, high policy movement, and high proposer gain.\n");
        builder.append("- Guarded default-pass variants trade productivity for lower volatility and lower proposer advantage.\n");
        builder.append("- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.\n");
        builder.append("- The next model extension should target proposal flooding and proposal costs, because this campaign makes proposal access and agenda screening central to the default-pass tradeoff.\n\n");
        builder.append("## Reproduction\n\n");
        builder.append("```sh\nmake campaign\n```\n");
        return builder.toString();
    }

    private static void appendHeadlineFindings(
            StringBuilder builder,
            List<CampaignRow> rows,
            Map<String, ScenarioAggregate> aggregateByScenario
    ) {
        ScenarioAggregate openDefault = aggregateByScenario.get("default-pass");
        ScenarioAggregate informedGuarded = aggregateByScenario.get("default-pass-informed-guarded");
        ScenarioAggregate simpleMajority = aggregateByScenario.get("simple-majority");
        ScenarioAggregate bestWelfare = aggregateByScenario.values()
                .stream()
                .max(Comparator.comparingDouble(ScenarioAggregate::welfare))
                .orElseThrow();
        double lowSupportReduction = openDefault.lowSupport() - informedGuarded.lowSupport();
        double policyShiftReduction = openDefault.policyShift() - informedGuarded.policyShift();
        double productivityChange = informedGuarded.productivity() - openDefault.productivity();

        builder.append("- Open default-pass averaged ")
                .append(format(openDefault.productivity()))
                .append(" productivity, versus ")
                .append(format(simpleMajority.productivity()))
                .append(" for simple majority.\n");
        builder.append("- Open default-pass also averaged ")
                .append(format(openDefault.lowSupport()))
                .append(" low-support passage and ")
                .append(format(openDefault.policyShift()))
                .append(" policy shift.\n");
        builder.append("- Informed guarded default-pass reduced low-support passage by ")
                .append(format(lowSupportReduction))
                .append(" and reduced policy shift by ")
                .append(format(policyShiftReduction))
                .append(", while changing productivity by ")
                .append(format(productivityChange))
                .append(".\n");
        builder.append("- Best average welfare in this campaign came from ")
                .append(bestWelfare.scenarioName())
                .append(" at ")
                .append(format(bestWelfare.welfare()))
                .append(".\n\n");
    }

    private static Map<String, ScenarioAggregate> aggregateByScenario(List<CampaignRow> rows) {
        Map<String, ScenarioAggregate> byScenario = new LinkedHashMap<>();
        for (CampaignRow row : rows) {
            byScenario.computeIfAbsent(
                    row.scenarioKey(),
                    key -> new ScenarioAggregate(key, row.report().scenarioName())
            ).add(row.report());
        }
        return byScenario;
    }

    private static int caseCount(List<CampaignRow> rows) {
        return caseKeys(rows).size();
    }

    private static List<String> caseKeys(List<CampaignRow> rows) {
        List<String> keys = new ArrayList<>();
        for (CampaignRow row : rows) {
            if (!keys.contains(row.caseKey())) {
                keys.add(row.caseKey());
            }
        }
        return keys;
    }

    private static CampaignRow find(List<CampaignRow> rows, String caseKey, String scenarioKey) {
        for (CampaignRow row : rows) {
            if (row.caseKey().equals(caseKey) && row.scenarioKey().equals(scenarioKey)) {
                return row;
            }
        }
        return null;
    }

    private static List<CampaignRow> rowsForCase(List<CampaignRow> rows, String caseKey) {
        List<CampaignRow> caseRows = new ArrayList<>();
        for (CampaignRow row : rows) {
            if (row.caseKey().equals(caseKey)) {
                caseRows.add(row);
            }
        }
        return caseRows;
    }

    private static CampaignRow max(List<CampaignRow> rows, Comparator<CampaignRow> comparator) {
        return rows.stream().max(comparator).orElseThrow();
    }

    private static CampaignRow min(List<CampaignRow> rows, Comparator<CampaignRow> comparator) {
        return rows.stream().min(comparator).orElseThrow();
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

    private record ExperimentCase(String key, String name, String description, WorldSpec worldSpec) {
    }

    private static final class ScenarioAggregate {
        private final String scenarioKey;
        private final String scenarioName;
        private int count;
        private double productivity;
        private double welfare;
        private double lowSupport;
        private double policyShift;
        private double proposerGain;
        private double floor;

        private ScenarioAggregate(String scenarioKey, String scenarioName) {
            this.scenarioKey = scenarioKey;
            this.scenarioName = scenarioName;
        }

        private void add(ScenarioReport report) {
            count++;
            productivity += report.productivity();
            welfare += report.averagePublicBenefit();
            lowSupport += report.controversialPassageRate();
            policyShift += report.averagePolicyShift();
            proposerGain += report.averageProposerGain();
            floor += report.floorConsiderationRate();
        }

        private String scenarioKey() {
            return scenarioKey;
        }

        private String scenarioName() {
            return scenarioName;
        }

        private double productivity() {
            return productivity / count;
        }

        private double welfare() {
            return welfare / count;
        }

        private double lowSupport() {
            return lowSupport / count;
        }

        private double policyShift() {
            return policyShift / count;
        }

        private double proposerGain() {
            return proposerGain / count;
        }

        private double floor() {
            return floor / count;
        }
    }
}
