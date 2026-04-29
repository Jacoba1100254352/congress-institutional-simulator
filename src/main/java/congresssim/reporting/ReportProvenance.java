package congresssim.reporting;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.List;
import java.util.Locale;

public final class ReportProvenance {
    private ReportProvenance() {
    }

    public static void write(
            Path manifestPath,
            String reportName,
            int runs,
            int legislators,
            int bills,
            long seed,
            int caseCount,
            int scenarioCount,
            List<Path> artifacts
    ) throws IOException {
        Files.createDirectories(manifestPath.getParent());
        StringBuilder builder = new StringBuilder();
        builder.append("{\n");
        append(builder, "reportName", reportName, true);
        append(builder, "commit", command("git", "rev-parse", "HEAD"), true);
        append(builder, "tag", command("git", "describe", "--tags", "--always", "HEAD"), true);
        append(builder, "gitDirty", !command("git", "status", "--short").isBlank(), true);
        append(builder, "javaVersion", System.getProperty("java.version", "unknown"), true);
        append(builder, "javaCommand", System.getProperty("sun.java.command", "unknown"), true);
        append(builder, "runs", runs, true);
        append(builder, "legislators", legislators, true);
        append(builder, "bills", bills, true);
        append(builder, "seed", seed, true);
        append(builder, "caseCount", caseCount, true);
        append(builder, "scenarioCount", scenarioCount, true);
        builder.append("  \"artifacts\": [\n");
        for (int i = 0; i < artifacts.size(); i++) {
            Path artifact = artifacts.get(i);
            builder.append("    {");
            builder.append("\"path\": \"").append(json(artifact.toString())).append("\", ");
            builder.append("\"sha256\": \"").append(json(sha256(artifact))).append("\"");
            builder.append("}");
            if (i + 1 < artifacts.size()) {
                builder.append(',');
            }
            builder.append('\n');
        }
        builder.append("  ]\n");
        builder.append("}\n");
        Files.writeString(manifestPath, builder.toString());
    }

    private static void append(StringBuilder builder, String key, String value, boolean comma) {
        builder.append("  \"").append(json(key)).append("\": \"").append(json(value)).append("\"");
        if (comma) {
            builder.append(',');
        }
        builder.append('\n');
    }

    private static void append(StringBuilder builder, String key, boolean value, boolean comma) {
        builder.append("  \"").append(json(key)).append("\": ").append(value);
        if (comma) {
            builder.append(',');
        }
        builder.append('\n');
    }

    private static void append(StringBuilder builder, String key, int value, boolean comma) {
        builder.append("  \"").append(json(key)).append("\": ").append(value);
        if (comma) {
            builder.append(',');
        }
        builder.append('\n');
    }

    private static void append(StringBuilder builder, String key, long value, boolean comma) {
        builder.append("  \"").append(json(key)).append("\": ").append(value);
        if (comma) {
            builder.append(',');
        }
        builder.append('\n');
    }

    private static String sha256(Path path) throws IOException {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            return HexFormat.of().formatHex(digest.digest(Files.readAllBytes(path))).toLowerCase(Locale.ROOT);
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 digest is unavailable.", exception);
        }
    }

    private static String command(String... command) {
        try {
            Process process = new ProcessBuilder(command)
                    .redirectErrorStream(true)
                    .start();
            String output = new String(process.getInputStream().readAllBytes()).trim();
            int exit = process.waitFor();
            if (exit != 0) {
                return "unknown";
            }
            return output;
        } catch (IOException exception) {
            return "unknown";
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            return "unknown";
        }
    }

    private static String json(String value) {
        return value
                .replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }
}
