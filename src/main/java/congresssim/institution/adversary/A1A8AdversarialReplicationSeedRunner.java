package congresssim.institution.adversary;

import java.io.IOException;
import java.nio.file.Path;


public final class A1A8AdversarialReplicationSeedRunner
{
	private A1A8AdversarialReplicationSeedRunner() {
	}

	public static void main(String[] args) throws IOException {
		if (args.length > 5) {
			throw new IllegalArgumentException(
					"Usage: A1A8AdversarialReplicationSeedRunner [outputDir] [runs] [legislators] [bills] [seed]"
			);
		}
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		int runs = args.length > 1 ? Integer.parseInt(args[1]) : 5;
		int legislators = args.length > 2 ? Integer.parseInt(args[2]) : 101;
		int bills = args.length > 3 ? Integer.parseInt(args[3]) : 60;
		long seed = args.length > 4 ? Long.parseLong(args[4]) : 20260428L;
		run(outputDir, runs, legislators, bills, seed);
	}

	public static void run(Path outputDir, int runs, int legislators, int bills, long seed) throws IOException {
		if (runs <= 0 || legislators <= 0 || bills <= 0) {
			throw new IllegalArgumentException("Runs, legislators, and bills must all be positive.");
		}
		A1CloneDecoyAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
		A2PoisonPillAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
		A3PublicInputAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
		A4BadFaithHarmClaimAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
		A5ProposalFloodingAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
		A6LobbyingCamouflageAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
		A7AdministrativeOverloadAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
		A8PublicSupportDistortionAdversarialStressRunner.runSummaryOnly(outputDir, runs, legislators, bills, seed);
	}
}
