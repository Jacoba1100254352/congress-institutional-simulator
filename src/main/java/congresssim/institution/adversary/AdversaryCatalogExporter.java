package congresssim.institution.adversary;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;


public final class AdversaryCatalogExporter
{
	private static final String STATUS = "schema_only_not_experiment_evidence";

	private AdversaryCatalogExporter() {
	}

	public static void main(String[] args) throws IOException {
		Path outputDir = args.length == 0 ? Path.of("reports") : Path.of(args[0]);
		write(outputDir);
	}

	public static void write(Path outputDir) throws IOException {
		Files.createDirectories(outputDir);
		Path csv = outputDir.resolve("adversary-catalog.csv");
		Path markdown = outputDir.resolve("adversary-catalog.md");
		Path manifest = outputDir.resolve("adversarial-stress-manifest.json");

		Files.writeString(csv, csv());
		Files.writeString(markdown, markdown());
		Files.writeString(manifest, manifestJson(csv, markdown));

		System.out.println("Wrote " + csv);
		System.out.println("Wrote " + markdown);
		System.out.println("Wrote " + manifest);
	}

	private static String csv() {
		StringBuilder builder = new StringBuilder();
		builder.append("adversaryId,name,actorType,objective,informationLevels,budgetUnits,strategySet,successMetric,degradationMetric,claimBoundary\n");
		for (AdversarySpec spec : AdversaryCatalog.firstWave()) {
			builder.append(csv(spec.id())).append(',')
			       .append(csv(spec.name())).append(',')
			       .append(csv(spec.actorType())).append(',')
			       .append(csv(spec.objective())).append(',')
			       .append(csv(levelKeys(spec.informationLevels()))).append(',')
			       .append(csv(String.join("; ", spec.budgetUnits()))).append(',')
			       .append(csv(String.join("; ", spec.strategySet()))).append(',')
			       .append(csv(spec.successMetric())).append(',')
			       .append(csv(spec.degradationMetric())).append(',')
			       .append(csv(AdversaryCatalog.CLAIM_BOUNDARY)).append('\n');
		}
		return builder.toString();
	}

	private static String markdown() {
		StringBuilder builder = new StringBuilder();
		builder.append("# Adversary Catalog\n\n");
		builder.append("Status: `").append(STATUS).append("`.\n\n");
		builder.append(AdversaryCatalog.CLAIM_BOUNDARY).append("\n\n");
		builder.append("- First-wave adversaries: ").append(AdversaryCatalog.firstWave().size()).append('\n');
		builder.append("- Required trace fields: ").append(AdversaryCatalog.requiredTraceFields().size()).append("\n\n");
		builder.append("| ID | Name | Information | Budget units | Success metric | Degradation metric |\n");
		builder.append("| --- | --- | --- | --- | --- | --- |\n");
		for (AdversarySpec spec : AdversaryCatalog.firstWave()) {
			builder.append("| ")
			       .append(spec.id()).append(" | ")
			       .append(md(spec.name())).append(" | ")
			       .append(md(levelKeys(spec.informationLevels()))).append(" | ")
			       .append(md(String.join("; ", spec.budgetUnits()))).append(" | ")
			       .append(md(spec.successMetric())).append(" | ")
			       .append(md(spec.degradationMetric())).append(" |\n");
		}
		builder.append("\n## Required Trace Fields\n\n");
		for (String field : AdversaryCatalog.requiredTraceFields()) {
			builder.append("- `").append(field).append("`\n");
		}
		return builder.toString();
	}

	private static String manifestJson(Path csv, Path markdown) {
		StringBuilder builder = new StringBuilder();
		builder.append("{\n");
		property(builder, 1, "manifestVersion", "adversarial-stress-schema-v0", true);
		property(builder, 1, "status", STATUS, true);
		property(builder, 1, "claimBoundary", AdversaryCatalog.CLAIM_BOUNDARY, true);
		arrayProperty(builder, 1, "catalogOutputs", List.of(csv.toString(), markdown.toString()), true);
		arrayProperty(builder, 1, "requiredTraceFields", AdversaryCatalog.requiredTraceFields(), true);
		builder.append("\t\"firstWaveAdversaries\": [\n");
		List<AdversarySpec> specs = AdversaryCatalog.firstWave();
		for (int i = 0; i < specs.size(); i++) {
			AdversarySpec spec = specs.get(i);
			builder.append("\t\t{\n");
			property(builder, 3, "id", spec.id(), true);
			property(builder, 3, "name", spec.name(), true);
			property(builder, 3, "actorType", spec.actorType(), true);
			property(builder, 3, "objective", spec.objective(), true);
			arrayProperty(builder, 3, "informationLevels", spec.informationLevels().stream().map(InformationLevel::key).toList(), true);
			arrayProperty(builder, 3, "budgetUnits", spec.budgetUnits(), true);
			arrayProperty(builder, 3, "strategySet", spec.strategySet(), true);
			property(builder, 3, "successMetric", spec.successMetric(), true);
			property(builder, 3, "degradationMetric", spec.degradationMetric(), false);
			builder.append("\t\t}");
			if (i < specs.size() - 1) {
				builder.append(',');
			}
			builder.append('\n');
		}
		builder.append("\t]\n");
		builder.append("}\n");
		return builder.toString();
	}

	private static void property(StringBuilder builder, int tabs, String key, String value, boolean comma) {
		builder.append("\t".repeat(tabs))
		       .append('"').append(json(key)).append("\": \"").append(json(value)).append('"');
		if (comma) {
			builder.append(',');
		}
		builder.append('\n');
	}

	private static void arrayProperty(StringBuilder builder, int tabs, String key, Collection<String> values, boolean comma) {
		builder.append("\t".repeat(tabs))
		       .append('"').append(json(key)).append("\": [")
		       .append(values.stream().map(value -> "\"" + json(value) + "\"").collect(Collectors.joining(", ")))
		       .append(']');
		if (comma) {
			builder.append(',');
		}
		builder.append('\n');
	}

	private static String levelKeys(List<InformationLevel> levels) {
		return levels.stream().map(InformationLevel::key).collect(Collectors.joining("; "));
	}

	private static String csv(String value) {
		return "\"" + value.replace("\"", "\"\"") + "\"";
	}

	private static String md(String value) {
		return value.replace("|", "\\|");
	}

	private static String json(String value) {
		return value.replace("\\", "\\\\").replace("\"", "\\\"");
	}
}
