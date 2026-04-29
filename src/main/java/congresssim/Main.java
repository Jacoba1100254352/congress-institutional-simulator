package congresssim;

import congresssim.simulation.ScenarioCatalog;
import congresssim.simulation.ScenarioReport;
import congresssim.simulation.Simulator;
import congresssim.simulation.WorldSpec;

import java.util.List;

public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        Options options = Options.parse(args);
        if (options.help) {
            Options.printUsage();
            return;
        }

        WorldSpec worldSpec = new WorldSpec(
                options.legislators,
                options.bills,
                0.72,
                0.68,
                0.48,
                0.64,
                0.52
        );

        Simulator simulator = new Simulator();
        List<ScenarioReport> reports = simulator.compare(
                ScenarioCatalog.defaultScenarios(),
                worldSpec,
                options.runs,
                options.seed
        );

        printReports(options, reports);
    }

    private static void printReports(Options options, List<ScenarioReport> reports) {
        System.out.println("Congress Institutional Simulator");
        System.out.printf("runs=%d legislators=%d billsPerRun=%d seed=%d%n%n",
                options.runs,
                options.legislators,
                options.bills,
                options.seed
        );

        System.out.printf("%-48s %8s %8s %10s %8s %9s %9s %10s %10s %10s%n",
                "Scenario",
                "Prod",
                "Floor",
                "AvgSupport",
                "Compromise",
                "AccessD",
                "CmteRej",
                "LowSupport",
                "PolicyShift",
                "PropGain"
        );
        System.out.println("-".repeat(132));

        for (ScenarioReport report : reports) {
            System.out.printf("%-48s %8.3f %8.3f %10.3f %8.3f %9.3f %9.3f %10.3f %10.3f %10.3f%n",
                    report.scenarioName(),
                    report.productivity(),
                    report.floorConsiderationRate(),
                    report.averageEnactedSupport(),
                    report.compromiseScore(),
                    report.accessDenialRate(),
                    report.committeeRejectionRate(),
                    report.controversialPassageRate(),
                    report.averagePolicyShift(),
                    report.averageProposerGain()
            );
        }
    }

    private static final class Options {
        private final int runs;
        private final int legislators;
        private final int bills;
        private final long seed;
        private final boolean help;

        private Options(int runs, int legislators, int bills, long seed, boolean help) {
            this.runs = runs;
            this.legislators = legislators;
            this.bills = bills;
            this.seed = seed;
            this.help = help;
        }

        private static Options parse(String[] args) {
            int runs = 250;
            int legislators = 101;
            int bills = 60;
            long seed = 20260428L;
            boolean help = false;

            for (int i = 0; i < args.length; i++) {
                String arg = args[i];
                switch (arg) {
                    case "--runs" -> runs = parseInt(args, ++i, arg);
                    case "--legislators" -> legislators = parseInt(args, ++i, arg);
                    case "--bills" -> bills = parseInt(args, ++i, arg);
                    case "--seed" -> seed = parseLong(args, ++i, arg);
                    case "--help", "-h" -> help = true;
                    default -> throw new IllegalArgumentException("Unknown argument: " + arg);
                }
            }

            if (runs <= 0 || legislators <= 0 || bills <= 0) {
                throw new IllegalArgumentException("runs, legislators, and bills must all be positive.");
            }
            return new Options(runs, legislators, bills, seed, help);
        }

        private static int parseInt(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires a value.");
            }
            return Integer.parseInt(args[index]);
        }

        private static long parseLong(String[] args, int index, String name) {
            if (index >= args.length) {
                throw new IllegalArgumentException(name + " requires a value.");
            }
            return Long.parseLong(args[index]);
        }

        private static void printUsage() {
            System.out.println("""
                    Usage: make run ARGS="--runs 500 --legislators 101 --bills 60 --seed 42"

                    Options:
                      --runs <n>          Number of randomized worlds per scenario
                      --legislators <n>   Number of legislators in the generated Congress
                      --bills <n>         Number of bills introduced per run
                      --seed <n>          Reproducible random seed
                      --help              Show this message
                    """);
        }
    }
}
