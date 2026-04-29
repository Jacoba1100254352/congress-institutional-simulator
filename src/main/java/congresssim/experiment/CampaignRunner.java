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
    private static final List<String> FLOODING_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-cost",
            "default-pass-access",
            "default-pass-committee",
            "default-pass-guarded",
            "default-pass-informed-guarded",
            "default-pass-cost-guarded",
            "bicameral-majority",
            "presidential-veto"
    );
    private static final List<String> CHALLENGE_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-challenge",
            "default-pass-challenge-info",
            "default-pass-cost",
            "default-pass-informed-guarded",
            "bicameral-majority",
            "presidential-veto"
    );
    private static final List<String> CHALLENGE_SWEEP_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082"
    );
    private static final List<String> CROSS_BLOC_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082"
    );
    private static final List<String> ADAPTIVE_TRACK_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-adaptive-track",
            "default-pass-adaptive-track-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082"
    );
    private static final List<String> SUNSET_TRIAL_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-adaptive-track",
            "default-pass-adaptive-track-challenge",
            "default-pass-sunset-trial",
            "default-pass-sunset-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082"
    );
    private static final List<String> PROPOSAL_CREDIT_SCENARIOS = List.of(
            "simple-majority",
            "supermajority-60",
            "default-pass",
            "default-pass-informed-guarded",
            "default-pass-challenge",
            "default-pass-cross-bloc",
            "default-pass-cross-bloc-strong",
            "default-pass-cross-bloc-challenge",
            "default-pass-adaptive-track",
            "default-pass-adaptive-track-challenge",
            "default-pass-sunset-trial",
            "default-pass-sunset-challenge",
            "default-pass-earned-credits",
            "default-pass-earned-credits-challenge",
            "default-pass-challenge-party-t3-s082",
            "default-pass-challenge-party-t6-s082",
            "default-pass-challenge-party-t15-s082",
            "default-pass-challenge-party-t25-s082",
            "default-pass-challenge-party-t10-s050",
            "default-pass-challenge-party-t10-s065",
            "default-pass-challenge-party-t10-s100",
            "default-pass-challenge-party-t10-s125",
            "default-pass-challenge-member-t1-s082",
            "default-pass-challenge-member-t2-s082",
            "default-pass-challenge-member-t3-s082",
            "default-pass-escalation-q6-s082",
            "default-pass-escalation-q12-s082",
            "default-pass-escalation-q20-s082"
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
        return run(
                "Simulation Campaign v0",
                "simulation-campaign-v0",
                outputDir,
                v0Cases(legislators, bills),
                CORE_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV1(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v1",
                "simulation-campaign-v1",
                outputDir,
                v1Cases(legislators, bills),
                FLOODING_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV2(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v2",
                "simulation-campaign-v2",
                outputDir,
                v1Cases(legislators, bills),
                CHALLENGE_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV3(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v3",
                "simulation-campaign-v3",
                outputDir,
                v1Cases(legislators, bills),
                CHALLENGE_SWEEP_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV4(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v4",
                "simulation-campaign-v4",
                outputDir,
                v1Cases(legislators, bills),
                CROSS_BLOC_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV5(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v5",
                "simulation-campaign-v5",
                outputDir,
                v1Cases(legislators, bills),
                ADAPTIVE_TRACK_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV6(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v6",
                "simulation-campaign-v6",
                outputDir,
                v1Cases(legislators, bills),
                SUNSET_TRIAL_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    public static CampaignResult runV7(
            Path outputDir,
            int runs,
            int legislators,
            int bills,
            long seed
    ) throws IOException {
        return run(
                "Simulation Campaign v7",
                "simulation-campaign-v7",
                outputDir,
                v1Cases(legislators, bills),
                PROPOSAL_CREDIT_SCENARIOS,
                runs,
                legislators,
                bills,
                seed
        );
    }

    private static CampaignResult run(
            String name,
            String fileStem,
            Path outputDir,
            List<ExperimentCase> cases,
            List<String> scenarioKeys,
            int runs,
            int legislators,
            int baseBills,
            long seed
    ) throws IOException {
        Files.createDirectories(outputDir);

        List<Scenario> scenarios = ScenarioCatalog.scenariosForKeys(scenarioKeys);
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
                        scenarioKeys.get(scenarioIndex),
                        reports.get(scenarioIndex)
                ));
            }
        }

        CampaignResult result = new CampaignResult(
                name,
                rows,
                outputDir.resolve(fileStem + ".csv"),
                outputDir.resolve(fileStem + ".md")
        );
        Files.writeString(result.csvPath(), csv(result, runs));
        Files.writeString(result.markdownPath(), markdown(result, runs, legislators, baseBills, seed, scenarioKeys.size()));
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

    private static List<ExperimentCase> v1Cases(int legislators, int bills) {
        List<ExperimentCase> cases = new ArrayList<>(v0Cases(legislators, bills));
        cases.add(experiment("high-proposal-pressure", "High Proposal Pressure", "Three times as many potential proposals reach the institutional system.",
                legislators, bills * 3, 3, 0.72, 0.68, 0.48, 0.64, 0.52));
        cases.add(experiment("extreme-proposal-pressure", "Extreme Proposal Pressure", "Five times as many potential proposals reach the institutional system.",
                legislators, bills * 5, 3, 0.72, 0.68, 0.48, 0.64, 0.52));
        cases.add(experiment("lobby-fueled-flooding", "Lobby-Fueled Flooding", "High proposal pressure with strong lobbying and weaker constituency pressure.",
                legislators, bills * 3, 3, 0.72, 0.70, 0.88, 0.42, 0.38));
        cases.add(experiment("low-compromise-flooding", "Low-Compromise Flooding", "High proposal pressure in a low-compromise legislature.",
                legislators, bills * 3, 3, 0.82, 0.76, 0.52, 0.54, 0.16));
        return cases;
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

    private static String csv(CampaignResult result, int runs) {
        StringBuilder builder = new StringBuilder();
        builder.append("caseKey,caseName,caseDescription,scenarioKey,scenario,totalBills,potentialBillsPerRun,enactedBills,enactedPerRun,floorPerRun,productivity,floor,avgSupport,welfare,cooperation,compromise,gridlock,accessDenied,committeeRejected,challengeRate,lowSupport,popularFail,policyShift,proposerGain,vetoes,overriddenVetoes\n");
        for (CampaignRow row : result.rows()) {
            ScenarioReport report = row.report();
            builder.append(csvValue(row.caseKey())).append(',')
                    .append(csvValue(row.caseName())).append(',')
                    .append(csvValue(row.caseDescription())).append(',')
                    .append(csvValue(row.scenarioKey())).append(',')
                    .append(csvValue(report.scenarioName())).append(',')
                    .append(report.totalBills()).append(',')
                    .append(format((double) report.totalBills() / runs)).append(',')
                    .append(report.enactedBills()).append(',')
                    .append(format((double) report.enactedBills() / runs)).append(',')
                    .append(format((report.totalBills() * report.floorConsiderationRate()) / runs)).append(',')
                    .append(format(report.productivity())).append(',')
                    .append(format(report.floorConsiderationRate())).append(',')
                    .append(format(report.averageEnactedSupport())).append(',')
                    .append(format(report.averagePublicBenefit())).append(',')
                    .append(format(report.cooperationScore())).append(',')
                    .append(format(report.compromiseScore())).append(',')
                    .append(format(report.gridlockRate())).append(',')
                    .append(format(report.accessDenialRate())).append(',')
                    .append(format(report.committeeRejectionRate())).append(',')
                    .append(format(report.challengeRate())).append(',')
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
            long seed,
            int scenarioCount
    ) {
        Map<String, ScenarioAggregate> aggregateByScenario = aggregateByScenario(result.rows(), runs);
        StringBuilder builder = new StringBuilder();
        builder.append("# ").append(result.name()).append("\n\n");
        builder.append("Deterministic batch campaign for comparing institutional regimes across assumption sweeps.\n\n");
        builder.append("## Run Configuration\n\n");
        builder.append("- runs per case: ").append(runs).append('\n');
        builder.append("- legislators: ").append(legislators).append('\n');
        builder.append("- base bills per run: ").append(bills).append('\n');
        builder.append("- base seed: ").append(seed).append('\n');
        builder.append("- scenarios per case: ").append(scenarioCount).append('\n');
        builder.append("- experiment cases: ").append(caseCount(result.rows())).append("\n\n");

        builder.append("## Headline Findings\n\n");
        appendHeadlineFindings(builder, result.rows(), aggregateByScenario);

        builder.append("## Scenario Averages Across Cases\n\n");
        builder.append("| Scenario | Productivity | Enacted/run | Floor/run | Welfare | Low-support | Policy shift | Proposer gain | Challenge | Floor |\n");
        builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
        aggregateByScenario.values()
                .stream()
                .sorted(Comparator.comparing(ScenarioAggregate::scenarioKey))
                .forEach(summary -> builder.append("| ")
                        .append(summary.scenarioName()).append(" | ")
                        .append(format(summary.productivity())).append(" | ")
                        .append(format(summary.enactedPerRun())).append(" | ")
                        .append(format(summary.floorPerRun())).append(" | ")
                        .append(format(summary.welfare())).append(" | ")
                        .append(format(summary.lowSupport())).append(" | ")
                        .append(format(summary.policyShift())).append(" | ")
                        .append(format(summary.proposerGain())).append(" | ")
                        .append(format(summary.challengeRate())).append(" | ")
                        .append(format(summary.floor())).append(" |\n"));
        builder.append('\n');

        if (aggregateByScenario.containsKey("default-pass-challenge")) {
            builder.append("## Challenge-Voucher Deltas\n\n");
            builder.append("Delta values compare `default-pass-challenge` against open `default-pass` in the same case. The challenge rate is the share of potential bills diverted from default enactment into an active vote.\n\n");
            builder.append("| Case | Enacted/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String caseKey : caseKeys(result.rows())) {
                CampaignRow open = find(result.rows(), caseKey, "default-pass");
                CampaignRow challenge = find(result.rows(), caseKey, "default-pass-challenge");
                if (open != null && challenge != null) {
                    builder.append("| ")
                            .append(open.caseName()).append(" | ")
                            .append(format(enactedPerRun(challenge, runs) - enactedPerRun(open, runs))).append(" | ")
                            .append(format(challenge.report().productivity() - open.report().productivity())).append(" | ")
                            .append(format(challenge.report().averagePublicBenefit() - open.report().averagePublicBenefit())).append(" | ")
                            .append(format(challenge.report().controversialPassageRate() - open.report().controversialPassageRate())).append(" | ")
                            .append(format(challenge.report().averagePolicyShift() - open.report().averagePolicyShift())).append(" | ")
                            .append(format(challenge.report().averageProposerGain() - open.report().averageProposerGain())).append(" | ")
                            .append(format(challenge.report().challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-challenge-party-t3-s082")
                || aggregateByScenario.containsKey("default-pass-escalation-q6-s082")) {
            builder.append("## Challenge Sweep Summary\n\n");
            builder.append("Delta values compare each challenge variant against open `default-pass` across all cases. Negative low-support, policy-shift, and proposer-gain deltas are desirable; productivity deltas show the throughput cost or gain.\n\n");
            builder.append("| Scenario | Productivity delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: |\n");
            for (ScenarioAggregate summary : aggregateByScenario.values()) {
                if (summary.scenarioKey().startsWith("default-pass-challenge")
                        || summary.scenarioKey().startsWith("default-pass-escalation")) {
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - aggregateByScenario.get("default-pass").productivity())).append(" | ")
                            .append(format(summary.lowSupport() - aggregateByScenario.get("default-pass").lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - aggregateByScenario.get("default-pass").policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - aggregateByScenario.get("default-pass").proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-cross-bloc")) {
            builder.append("## Cross-Bloc Cosponsorship Deltas\n\n");
            builder.append("Delta values compare each cross-bloc agenda gate against open `default-pass` across all cases. Access-denial deltas expose the direct agenda-screening cost.\n\n");
            builder.append("| Scenario | Productivity delta | Floor delta | Access-denial delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-cross-bloc",
                    "default-pass-cross-bloc-strong",
                    "default-pass-cross-bloc-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.floor() - open.floor())).append(" | ")
                            .append(format(summary.accessDenied() - open.accessDenied())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-adaptive-track")) {
            builder.append("## Adaptive Track Deltas\n\n");
            builder.append("Delta values compare adaptive procedural routing against open `default-pass` across all cases. Access-denial, committee-rejection, and challenge rates show which review lanes are being used.\n\n");
            builder.append("| Scenario | Productivity delta | Floor delta | Access denied | Committee rejected | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-adaptive-track",
                    "default-pass-adaptive-track-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.floor() - open.floor())).append(" | ")
                            .append(format(summary.accessDenied())).append(" | ")
                            .append(format(summary.committeeRejected())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-sunset-trial")) {
            builder.append("## Sunset Trial Deltas\n\n");
            builder.append("Delta values compare provisional enactment with automatic review against open `default-pass` across all cases. The trial process expires risky enacted bills that fail review, rolling the status quo back.\n\n");
            builder.append("| Scenario | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-sunset-trial",
                    "default-pass-sunset-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-earned-credits")) {
            builder.append("## Earned Proposal-Credit Deltas\n\n");
            builder.append("Delta values compare stateful earned agenda credits against open `default-pass` across all cases. Access denial is the share of potential proposals whose sponsors lacked enough accumulated credit.\n\n");
            builder.append("| Scenario | Productivity delta | Floor delta | Access denied | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta | Challenge rate |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String scenarioKey : List.of(
                    "default-pass-earned-credits",
                    "default-pass-earned-credits-challenge"
            )) {
                ScenarioAggregate summary = aggregateByScenario.get(scenarioKey);
                if (summary != null) {
                    ScenarioAggregate open = aggregateByScenario.get("default-pass");
                    builder.append("| ")
                            .append(summary.scenarioName()).append(" | ")
                            .append(format(summary.productivity() - open.productivity())).append(" | ")
                            .append(format(summary.floor() - open.floor())).append(" | ")
                            .append(format(summary.accessDenied())).append(" | ")
                            .append(format(summary.welfare() - open.welfare())).append(" | ")
                            .append(format(summary.lowSupport() - open.lowSupport())).append(" | ")
                            .append(format(summary.policyShift() - open.policyShift())).append(" | ")
                            .append(format(summary.proposerGain() - open.proposerGain())).append(" | ")
                            .append(format(summary.challengeRate())).append(" |\n");
                }
            }
            builder.append('\n');
        }

        if (aggregateByScenario.containsKey("default-pass-cost")) {
            builder.append("## Proposal-Cost Deltas\n\n");
            builder.append("Delta values compare `default-pass-cost` against open `default-pass` in the same case. Negative enacted-per-run, floor-per-run, low-support, and policy-shift deltas show the proposal-cost screen reducing flooding and volatility.\n\n");
            builder.append("| Case | Enacted/run delta | Floor/run delta | Productivity delta | Welfare delta | Low-support delta | Policy-shift delta | Proposer-gain delta |\n");
            builder.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n");
            for (String caseKey : caseKeys(result.rows())) {
                CampaignRow open = find(result.rows(), caseKey, "default-pass");
                CampaignRow cost = find(result.rows(), caseKey, "default-pass-cost");
                if (open != null && cost != null) {
                    builder.append("| ")
                            .append(open.caseName()).append(" | ")
                            .append(format(enactedPerRun(cost, runs) - enactedPerRun(open, runs))).append(" | ")
                            .append(format(floorPerRun(cost, runs) - floorPerRun(open, runs))).append(" | ")
                            .append(format(cost.report().productivity() - open.report().productivity())).append(" | ")
                            .append(format(cost.report().averagePublicBenefit() - open.report().averagePublicBenefit())).append(" | ")
                            .append(format(cost.report().controversialPassageRate() - open.report().controversialPassageRate())).append(" | ")
                            .append(format(cost.report().averagePolicyShift() - open.report().averagePolicyShift())).append(" | ")
                            .append(format(cost.report().averageProposerGain() - open.report().averageProposerGain())).append(" |\n");
                }
            }
            builder.append('\n');
        }

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
        if (aggregateByScenario.containsKey("default-pass-cost")) {
            builder.append("- Proposal-cost screens are useful for measuring flooding as institutional load: floor/run and enacted/run expose costs hidden by percentage-only metrics.\n");
        }
        builder.append("- Challenge vouchers test whether default-pass can preserve throughput while forcing only the most contested bills into active votes.\n");
        if (aggregateByScenario.containsKey("default-pass-cost")) {
            builder.append("- The current cost screen reduces volume, but it also selects for proposals with high proposer value or positive lobby pressure; that makes cost design an object of study, not a solved safeguard.\n");
        }
        builder.append("- Welfare-oriented comparisons should be read alongside productivity: the same institution can pass fewer bills while improving enacted bill quality.\n");
        if (aggregateByScenario.containsKey("default-pass-challenge-party-t3-s082")) {
            builder.append("- The challenge sweep compares token budgets, challenge thresholds, party-held tokens, member-held tokens, and tokenless q-member escalation.\n");
            if (aggregateByScenario.containsKey("default-pass-cross-bloc")) {
                builder.append("- Cross-bloc cosponsorship tests coalition breadth as a pre-floor agenda gate, before default-pass or challenge mechanics can operate.\n");
                if (aggregateByScenario.containsKey("default-pass-adaptive-track")) {
                    builder.append("- Adaptive procedural tracks test whether low-risk bills can stay in a fast lane while high-risk bills receive stronger review.\n");
                    if (aggregateByScenario.containsKey("default-pass-sunset-trial")) {
                        builder.append("- Sunset trial rules test whether risky default enactments can be made reversible after automatic review.\n");
                        if (aggregateByScenario.containsKey("default-pass-earned-credits")) {
                            builder.append("- Earned proposal credits test whether agenda access can learn from proposer track records instead of using only fixed up-front costs.\n");
                            builder.append("- The next model extension should add structured amendment or mediation, because the current agenda systems screen and route bills but still rarely change bill content before final yes/no choice.\n\n");
                        } else {
                            builder.append("- The next model extension should add earned proposal credits, because agenda access still does not learn from proposer track records.\n\n");
                        }
                    } else {
                        builder.append("- The next model extension should add sunset trial legislation, because the remaining risk is bad-law persistence after enactment.\n\n");
                    }
                } else {
                    builder.append("- The next model extension should add adaptive procedural tracks, because the agenda system now needs to route bills by risk rather than screening every bill with one rule.\n\n");
                }
            } else {
                builder.append("- The next model extension should add coalition-breadth proposal access, because challenge mechanics still operate after a bill enters the agenda.\n\n");
            }
        } else {
            builder.append("- The next model extension should sweep challenge-token budgets, challenge thresholds, and proposal-cost mechanisms, because agenda screening is now the central default-pass tradeoff.\n\n");
        }
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
        ScenarioAggregate proposalCost = aggregateByScenario.get("default-pass-cost");
        ScenarioAggregate challenge = aggregateByScenario.get("default-pass-challenge");
        ScenarioAggregate crossBloc = aggregateByScenario.get("default-pass-cross-bloc");
        ScenarioAggregate adaptive = aggregateByScenario.get("default-pass-adaptive-track");
        ScenarioAggregate sunset = aggregateByScenario.get("default-pass-sunset-trial");
        ScenarioAggregate credits = aggregateByScenario.get("default-pass-earned-credits");
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
        if (proposalCost != null) {
            builder.append("- Proposal-cost screening reduced floor load by ")
                    .append(format(openDefault.floorPerRun() - proposalCost.floorPerRun()))
                    .append(" bills/run and enactments by ")
                    .append(format(openDefault.enactedPerRun() - proposalCost.enactedPerRun()))
                    .append(" bills/run, but raised proposer gain by ")
                    .append(format(proposalCost.proposerGain() - openDefault.proposerGain()))
                    .append(".\n");
        }
        if (challenge != null) {
            builder.append("- Challenge vouchers averaged ")
                    .append(format(challenge.challengeRate()))
                    .append(" challenge use, changed productivity by ")
                    .append(format(challenge.productivity() - openDefault.productivity()))
                    .append(", and changed low-support passage by ")
                    .append(format(challenge.lowSupport() - openDefault.lowSupport()))
                    .append(" relative to open default-pass.\n");
        }
        if (crossBloc != null) {
            builder.append("- Cross-bloc cosponsorship changed productivity by ")
                    .append(format(crossBloc.productivity() - openDefault.productivity()))
                    .append(", floor consideration by ")
                    .append(format(crossBloc.floor() - openDefault.floor()))
                    .append(", and low-support passage by ")
                    .append(format(crossBloc.lowSupport() - openDefault.lowSupport()))
                    .append(" relative to open default-pass.\n");
        }
        if (adaptive != null) {
            builder.append("- Adaptive tracks changed productivity by ")
                    .append(format(adaptive.productivity() - openDefault.productivity()))
                    .append(", low-support passage by ")
                    .append(format(adaptive.lowSupport() - openDefault.lowSupport()))
                    .append(", and policy shift by ")
                    .append(format(adaptive.policyShift() - openDefault.policyShift()))
                    .append(" relative to open default-pass.\n");
        }
        if (sunset != null) {
            builder.append("- Sunset trial review changed productivity by ")
                    .append(format(sunset.productivity() - openDefault.productivity()))
                    .append(", welfare by ")
                    .append(format(sunset.welfare() - openDefault.welfare()))
                    .append(", and policy shift by ")
                    .append(format(sunset.policyShift() - openDefault.policyShift()))
                    .append(" relative to open default-pass.\n");
        }
        if (credits != null) {
            builder.append("- Earned proposal credits denied ")
                    .append(format(credits.accessDenied()))
                    .append(" of potential proposals, changed welfare by ")
                    .append(format(credits.welfare() - openDefault.welfare()))
                    .append(", and changed proposer gain by ")
                    .append(format(credits.proposerGain() - openDefault.proposerGain()))
                    .append(" relative to open default-pass.\n");
        }
        builder.append("- Best average welfare in this campaign came from ")
                .append(bestWelfare.scenarioName())
                .append(" at ")
                .append(format(bestWelfare.welfare()))
                .append(".\n\n");
    }

    private static Map<String, ScenarioAggregate> aggregateByScenario(List<CampaignRow> rows, int runs) {
        Map<String, ScenarioAggregate> byScenario = new LinkedHashMap<>();
        for (CampaignRow row : rows) {
            byScenario.computeIfAbsent(
                    row.scenarioKey(),
                    key -> new ScenarioAggregate(key, row.report().scenarioName())
            ).add(row.report(), runs);
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

    private static double enactedPerRun(CampaignRow row, int runs) {
        return (double) row.report().enactedBills() / runs;
    }

    private static double floorPerRun(CampaignRow row, int runs) {
        return (row.report().totalBills() * row.report().floorConsiderationRate()) / runs;
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
        private double challengeRate;
        private double floor;
        private double accessDenied;
        private double committeeRejected;
        private double enactedPerRun;
        private double floorPerRun;

        private ScenarioAggregate(String scenarioKey, String scenarioName) {
            this.scenarioKey = scenarioKey;
            this.scenarioName = scenarioName;
        }

        private void add(ScenarioReport report, int runs) {
            count++;
            productivity += report.productivity();
            welfare += report.averagePublicBenefit();
            lowSupport += report.controversialPassageRate();
            policyShift += report.averagePolicyShift();
            proposerGain += report.averageProposerGain();
            challengeRate += report.challengeRate();
            floor += report.floorConsiderationRate();
            accessDenied += report.accessDenialRate();
            committeeRejected += report.committeeRejectionRate();
            enactedPerRun += (double) report.enactedBills() / runs;
            floorPerRun += (report.totalBills() * report.floorConsiderationRate()) / runs;
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

        private double challengeRate() {
            return challengeRate / count;
        }

        private double floor() {
            return floor / count;
        }

        private double accessDenied() {
            return accessDenied / count;
        }

        private double committeeRejected() {
            return committeeRejected / count;
        }

        private double enactedPerRun() {
            return enactedPerRun / count;
        }

        private double floorPerRun() {
            return floorPerRun / count;
        }
    }
}
