package congresssim;

import congresssim.experiment.CampaignResult;
import congresssim.experiment.CampaignRunner;
import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.StringJoiner;

public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        Options options = Options.parse(args);
        if (options.help) {
            Options.printUsage();
            return;
        }
        if (options.campaignName != null) {
            runCampaign(options);
            return;
        }

        WorldSpec worldSpec = new WorldSpec(
                options.legislators,
                options.bills,
                options.partyCount,
                options.polarization,
                options.partyLoyalty,
                options.lobbyingSusceptibility,
                options.constituencySensitivity,
                options.compromiseCulture
        );

        Simulator simulator = new Simulator();
        List<congresssim.simulation.Scenario> scenarios = options.scenarioKeys.isEmpty()
                ? ScenarioCatalog.defaultScenarios()
                : ScenarioCatalog.scenariosForKeys(options.scenarioKeys);
        List<ScenarioReport> reports = simulator.compare(
                scenarios,
                worldSpec,
                options.runs,
                options.seed
        );

        printReports(options, reports, worldSpec);
    }

    private static void runCampaign(Options options) {
        try {
            CampaignResult result = switch (options.campaignName) {
                case "v0" -> CampaignRunner.runV0(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v1" -> CampaignRunner.runV1(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v2" -> CampaignRunner.runV2(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v3" -> CampaignRunner.runV3(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v4" -> CampaignRunner.runV4(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v5" -> CampaignRunner.runV5(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v6" -> CampaignRunner.runV6(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v7" -> CampaignRunner.runV7(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v8" -> CampaignRunner.runV8(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v9" -> CampaignRunner.runV9(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v10" -> CampaignRunner.runV10(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v11" -> CampaignRunner.runV11(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v12" -> CampaignRunner.runV12(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v13" -> CampaignRunner.runV13(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v14" -> CampaignRunner.runV14(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v15" -> CampaignRunner.runV15(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                case "v16" -> CampaignRunner.runV16(
                        options.outputDir,
                        options.runs,
                        options.legislators,
                        options.bills,
                        options.seed
                );
                default -> throw new IllegalArgumentException("Unknown campaign: " + options.campaignName);
            };
            System.out.println(result.name() + " complete.");
            System.out.println("CSV: " + result.csvPath());
            System.out.println("Markdown: " + result.markdownPath());
        } catch (IOException exception) {
            throw new IllegalStateException("Unable to write campaign output.", exception);
        }
    }

    private static void printReports(Options options, List<ScenarioReport> reports, WorldSpec worldSpec) {
        if (options.outputFormat == OutputFormat.CSV) {
            printCsv(reports);
            return;
        }

        System.out.println("Congress Institutional Simulator");
        System.out.printf("runs=%d legislators=%d billsPerRun=%d seed=%d%n%n",
                options.runs,
                options.legislators,
                options.bills,
                options.seed
        );
        System.out.printf(
                "assumptions: parties=%d polarization=%.2f partyLoyalty=%.2f compromise=%.2f constituency=%.2f lobbying=%.2f%n%n",
                worldSpec.partyCount(),
                worldSpec.polarization(),
                worldSpec.partyLoyalty(),
                worldSpec.compromiseCulture(),
                worldSpec.constituencySensitivity(),
                worldSpec.lobbyingSusceptibility()
        );

        if (options.outputFormat == OutputFormat.BARS) {
            printCharts(reports);
            return;
        }

        System.out.printf("%-48s %8s %8s %10s %8s %8s %8s %8s %8s %9s %9s %10s %10s %10s %10s%n",
                "Scenario",
                "Prod",
                "Floor",
                "AvgSupport",
                "Welfare",
                "Compromise",
                "Capture",
                "Spend",
                "Amend",
                "AccessD",
                "CmteRej",
                "AntiLobby",
                "LowSupport",
                "PolicyShift",
                "PropGain"
        );
        System.out.println("-".repeat(161));

        for (ScenarioReport report : reports) {
            System.out.printf("%-48s %8.3f %8.3f %10.3f %8.3f %8.3f %8.3f %8.3f %8.3f %9.3f %9.3f %10.3f %10.3f %10.3f %10.3f%n",
                    report.scenarioName(),
                    report.productivity(),
                    report.floorConsiderationRate(),
                    report.averageEnactedSupport(),
                    report.averagePublicBenefit(),
                    report.compromiseScore(),
                    report.lobbyCaptureIndex(),
                    report.lobbySpendPerBill(),
                    report.amendmentRate(),
                    report.accessDenialRate(),
                    report.committeeRejectionRate(),
                    report.antiLobbyingSuccessRate(),
                    report.controversialPassageRate(),
                    report.averagePolicyShift(),
                    report.averageProposerGain()
            );
        }

        if (options.charts || options.outputFormat == OutputFormat.BARS) {
            printCharts(reports);
        }
    }

    private static void printCsv(List<ScenarioReport> reports) {
        System.out.println("scenario,totalBills,enactedBills,productivity,floor,avgSupport,welfare,cooperation,compromise,gridlock,accessDenied,committeeRejected,challengeRate,lowSupport,popularFail,policyShift,proposerGain,lobbyCapture,publicAlignment,antiLobbyingSuccess,privateGainRatio,lobbySpendPerBill,defensiveLobbyingShare,captureReturnOnSpend,publicPreferenceDistortion,amendmentRate,amendmentMovement,vetoes,overriddenVetoes");
        for (ScenarioReport report : reports) {
            System.out.printf(Locale.ROOT,
                    "%s,%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d,%d%n",
                    report.scenarioName(),
                    report.totalBills(),
                    report.enactedBills(),
                    report.productivity(),
                    report.floorConsiderationRate(),
                    report.averageEnactedSupport(),
                    report.averagePublicBenefit(),
                    report.cooperationScore(),
                    report.compromiseScore(),
                    report.gridlockRate(),
                    report.accessDenialRate(),
                    report.committeeRejectionRate(),
                    report.challengeRate(),
                    report.controversialPassageRate(),
                    report.popularBillFailureRate(),
                    report.averagePolicyShift(),
                    report.averageProposerGain(),
                    report.lobbyCaptureIndex(),
                    report.publicAlignmentScore(),
                    report.antiLobbyingSuccessRate(),
                    report.privateGainRatio(),
                    report.lobbySpendPerBill(),
                    report.defensiveLobbyingShare(),
                    report.captureReturnOnSpend(),
                    report.publicPreferenceDistortion(),
                    report.amendmentRate(),
                    report.averageAmendmentMovement(),
                    report.vetoes(),
                    report.overriddenVetoes()
            );
        }
    }

    private static void printCharts(List<ScenarioReport> reports) {
        System.out.println();
        printChart("Productivity", reports, Metric.PRODUCTIVITY);
        printChart("Public welfare", reports, Metric.PUBLIC_WELFARE);
        printChart("Low-support passage", reports, Metric.LOW_SUPPORT);
        printChart("Policy shift", reports, Metric.POLICY_SHIFT);
    }

    private static void printChart(String title, List<ScenarioReport> reports, Metric metric) {
        System.out.println(title);
        for (ScenarioReport report : reports) {
            double value = metric.value(report);
            System.out.printf(Locale.ROOT,
                    "  %-48s %s %.3f%n",
                    report.scenarioName(),
                    bar(value, 24),
                    value
            );
        }
        System.out.println();
    }

    private static String bar(double value, int width) {
        double normalized = Math.clamp(value, 0.0, 1.0);
        int filled = (int) Math.round(normalized * width);
        return "[" + "#".repeat(filled) + ".".repeat(width - filled) + "]";
    }

    private enum Metric {
        PRODUCTIVITY {
            @Override
            double value(ScenarioReport report) {
                return report.productivity();
            }
        },
        LOW_SUPPORT {
            @Override
            double value(ScenarioReport report) {
                return report.controversialPassageRate();
            }
        },
        PUBLIC_WELFARE {
            @Override
            double value(ScenarioReport report) {
                return report.averagePublicBenefit();
            }
        },
        POLICY_SHIFT {
            @Override
            double value(ScenarioReport report) {
                return report.averagePolicyShift();
            }
        };

        abstract double value(ScenarioReport report);
    }

    private enum OutputFormat {
        TABLE,
        CSV,
        BARS
    }

    private static final class Options {
        private final int runs;
        private final int legislators;
        private final int bills;
        private final int partyCount;
        private final double polarization;
        private final double partyLoyalty;
        private final double lobbyingSusceptibility;
        private final double constituencySensitivity;
        private final double compromiseCulture;
        private final List<String> scenarioKeys;
        private final OutputFormat outputFormat;
        private final boolean charts;
        private final String campaignName;
        private final Path outputDir;
        private final long seed;
        private final boolean help;

        private Options(
                int runs,
                int legislators,
                int bills,
                int partyCount,
                double polarization,
                double partyLoyalty,
                double lobbyingSusceptibility,
                double constituencySensitivity,
                double compromiseCulture,
                List<String> scenarioKeys,
                OutputFormat outputFormat,
                boolean charts,
                String campaignName,
                Path outputDir,
                long seed,
                boolean help
        ) {
            this.runs = runs;
            this.legislators = legislators;
            this.bills = bills;
            this.partyCount = partyCount;
            this.polarization = polarization;
            this.partyLoyalty = partyLoyalty;
            this.lobbyingSusceptibility = lobbyingSusceptibility;
            this.constituencySensitivity = constituencySensitivity;
            this.compromiseCulture = compromiseCulture;
            this.scenarioKeys = List.copyOf(scenarioKeys);
            this.outputFormat = outputFormat;
            this.charts = charts;
            this.campaignName = campaignName;
            this.outputDir = outputDir;
            this.seed = seed;
            this.help = help;
        }

        private static Options parse(String[] args) {
            int runs = 250;
            int legislators = 101;
            int bills = 60;
            int partyCount = 3;
            double polarization = 0.72;
            double partyLoyalty = 0.68;
            double lobbyingSusceptibility = 0.48;
            double constituencySensitivity = 0.64;
            double compromiseCulture = 0.52;
            List<String> scenarioKeys = new ArrayList<>();
            OutputFormat outputFormat = OutputFormat.TABLE;
            boolean charts = false;
            String campaignName = null;
            Path outputDir = Path.of("reports");
            long seed = 20260428L;
            boolean help = false;

            for (int i = 0; i < args.length; i++) {
                String arg = args[i];
                switch (arg) {
                    case "--runs" -> runs = parseInt(args, ++i, arg);
                    case "--legislators" -> legislators = parseInt(args, ++i, arg);
                    case "--bills" -> bills = parseInt(args, ++i, arg);
                    case "--party-count" -> partyCount = parseInt(args, ++i, arg);
                    case "--polarization" -> polarization = parseDouble(args, ++i, arg);
                    case "--party-loyalty" -> partyLoyalty = parseDouble(args, ++i, arg);
                    case "--lobbying" -> lobbyingSusceptibility = parseDouble(args, ++i, arg);
                    case "--constituency" -> constituencySensitivity = parseDouble(args, ++i, arg);
                    case "--compromise" -> compromiseCulture = parseDouble(args, ++i, arg);
                    case "--scenarios" -> scenarioKeys = parseScenarioKeys(args, ++i, arg);
                    case "--format" -> outputFormat = parseOutputFormat(args, ++i, arg);
                    case "--charts" -> charts = true;
                    case "--campaign" -> campaignName = parseString(args, ++i, arg);
                    case "--output-dir" -> outputDir = Path.of(parseString(args, ++i, arg));
                    case "--seed" -> seed = parseLong(args, ++i, arg);
                    case "--help", "-h" -> help = true;
                    default -> throw new IllegalArgumentException("Unknown argument: " + arg);
                }
            }

            if (runs <= 0 || legislators <= 0 || bills <= 0) {
                throw new IllegalArgumentException("runs, legislators, and bills must all be positive.");
            }
            return new Options(
                    runs,
                    legislators,
                    bills,
                    partyCount,
                    polarization,
                    partyLoyalty,
                    lobbyingSusceptibility,
                    constituencySensitivity,
                    compromiseCulture,
                    scenarioKeys,
                    outputFormat,
                    charts,
                    campaignName,
                    outputDir,
                    seed,
                    help
            );
        }

        private static int parseInt(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires a value.");
            }
            return Integer.parseInt(args[index]);
        }

        private static double parseDouble(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires a value.");
            }
            return Double.parseDouble(args[index]);
        }

        private static String parseString(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires a value.");
            }
            return args[index];
        }

        private static long parseLong(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires a value.");
            }
            return Long.parseLong(args[index]);
        }

        private static List<String> parseScenarioKeys(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires a comma-separated value.");
            }
            return Arrays.stream(args[index].split(","))
                    .map(String::trim)
                    .filter(value -> !value.isEmpty())
                    .toList();
        }

        private static OutputFormat parseOutputFormat(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires table, csv, or bars.");
            }
            return switch (args[index].toLowerCase(Locale.ROOT)) {
                case "table" -> OutputFormat.TABLE;
                case "csv" -> OutputFormat.CSV;
                case "bars" -> OutputFormat.BARS;
                default -> throw new IllegalArgumentException(name + " must be table, csv, or bars.");
            };
        }

        private static void printUsage() {
            StringJoiner scenarioKeys = new StringJoiner(", ");
            for (String key : ScenarioCatalog.scenarioKeys()) {
                scenarioKeys.add(key);
            }

            System.out.println("""
                    Usage: make run ARGS="--runs 500 --legislators 101 --bills 60 --seed 42 --charts"

                    Options:
                      --runs <n>          Number of randomized worlds per scenario
                      --legislators <n>   Number of legislators in the generated Congress
                      --bills <n>         Number of bills introduced per run
                      --party-count <n>   Number of generated party labels
                      --polarization <x>  Ideological clustering, from 0.0 to 1.0
                      --party-loyalty <x> Party-pressure sensitivity, from 0.0 to 1.0
                      --compromise <x>    Compromise culture, from 0.0 to 1.0
                      --constituency <x>  Constituent-pressure sensitivity, from 0.0 to 1.0
                      --lobbying <x>      Lobby-pressure sensitivity, from 0.0 to 1.0
                      --scenarios <keys>  Comma-separated scenario keys
                      --format <kind>     table, csv, or bars
                      --charts            Add ASCII bar charts after the table
                      --campaign <name>   Run a named campaign, currently v0 through v16
                      --output-dir <path> Campaign output directory
                      --seed <n>          Reproducible random seed
                      --help              Show this message

                    Scenario keys:
                    """ + scenarioKeys + "\n");
        }
    }
}
