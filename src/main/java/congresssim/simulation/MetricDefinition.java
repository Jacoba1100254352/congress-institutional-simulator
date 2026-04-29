package congresssim.simulation;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public record MetricDefinition(
        String key,
        String label,
        MetricDirection direction,
        String note
) {
    private static final List<MetricDefinition> DEFINITIONS = List.of(
            new MetricDefinition("productivity", "Productivity", MetricDirection.HIGHER_IS_BETTER, "Share of potential bills enacted."),
            new MetricDefinition("avgSupport", "Average enacted support", MetricDirection.HIGHER_IS_BETTER, "Average yes share among enacted bills."),
            new MetricDefinition("welfare", "Generated welfare", MetricDirection.HIGHER_IS_BETTER, "Average generated public-benefit score for enacted bills."),
            new MetricDefinition("cooperation", "Cooperation", MetricDirection.HIGHER_IS_BETTER, "Throughput weighted by enacted support."),
            new MetricDefinition("compromise", "Compromise", MetricDirection.HIGHER_IS_BETTER, "Moderation, support, and distance from proposer advantage."),
            new MetricDefinition("publicAlignment", "Public alignment", MetricDirection.HIGHER_IS_BETTER, "How closely enacted support tracks generated public support."),
            new MetricDefinition("legitimacy", "Legitimacy", MetricDirection.HIGHER_IS_BETTER, "Public, chamber, and affected-group support net of harm."),
            new MetricDefinition("antiLobbyingSuccess", "Anti-lobbying success", MetricDirection.HIGHER_IS_BETTER, "Share of generated anti-lobbying reforms enacted."),
            new MetricDefinition("citizenCertificationRate", "Citizen certification", MetricDirection.HIGHER_IS_BETTER, "Share of reviewed bills certified by a citizen panel."),
            new MetricDefinition("districtAlignment", "District alignment", MetricDirection.HIGHER_IS_BETTER, "Alignment between district/public signals and final action."),
            new MetricDefinition("welfarePerSubmittedBill", "Welfare per submitted bill", MetricDirection.HIGHER_IS_BETTER, "Public-benefit yield per proposal opportunity."),
            new MetricDefinition("publicBenefitPerLobbyDollar", "Public benefit per lobby dollar", MetricDirection.HIGHER_IS_BETTER, "Generated benefit per unit of explicit lobby spend."),
            new MetricDefinition("gridlock", "Gridlock", MetricDirection.LOWER_IS_BETTER, "Share of introduced bills that fail."),
            new MetricDefinition("lowSupport", "Low-support passage", MetricDirection.LOWER_IS_BETTER, "Enacted bills with less than majority yes support."),
            new MetricDefinition("popularFail", "Popular failure", MetricDirection.LOWER_IS_BETTER, "High-public-support bills that fail."),
            new MetricDefinition("lobbyCapture", "Lobby capture", MetricDirection.LOWER_IS_BETTER, "Capture risk from lobby pressure, private gain, and weak public value."),
            new MetricDefinition("publicPreferenceDistortion", "Public-preference distortion", MetricDirection.LOWER_IS_BETTER, "Gap between enacted yes share and generated public support."),
            new MetricDefinition("minorityHarm", "Minority harm", MetricDirection.LOWER_IS_BETTER, "Concentrated harm weighted by affected-group opposition."),
            new MetricDefinition("concentratedHarmPassage", "Concentrated-harm passage", MetricDirection.LOWER_IS_BETTER, "High-harm bills enacted."),
            new MetricDefinition("proposerGain", "Proposer gain", MetricDirection.LOWER_IS_BETTER, "Movement toward proposer ideal, normalized for directional scores."),
            new MetricDefinition("lowSupportActiveLawShare", "Low-support active-law share", MetricDirection.LOWER_IS_BETTER, "Persistent enacted law stock with weak support."),
            new MetricDefinition("falseNegativePassRate", "False-negative default passage", MetricDirection.LOWER_IS_BETTER, "Risky default enactments that passed unchallenged."),
            new MetricDefinition("privateGainRatio", "Private-gain ratio", MetricDirection.LOWER_IS_BETTER, "Private gain relative to generated public benefit."),
            new MetricDefinition("captureReturnOnSpend", "Capture return on spend", MetricDirection.LOWER_IS_BETTER, "Capture risk per unit of explicit lobby spend."),
            new MetricDefinition("floor", "Floor consideration", MetricDirection.DIAGNOSTIC, "Institutional load and access, not inherently good or bad."),
            new MetricDefinition("accessDenied", "Access denied", MetricDirection.DIAGNOSTIC, "Proposal-screening intensity."),
            new MetricDefinition("committeeRejected", "Committee rejected", MetricDirection.DIAGNOSTIC, "Committee gatekeeping intensity."),
            new MetricDefinition("challengeRate", "Challenge rate", MetricDirection.DIAGNOSTIC, "Contestation activity."),
            new MetricDefinition("amendmentRate", "Amendment rate", MetricDirection.DIAGNOSTIC, "Revision activity."),
            new MetricDefinition("compensationRate", "Compensation rate", MetricDirection.DIAGNOSTIC, "Affected-group compensation activity."),
            new MetricDefinition("reversalRate", "Reversal rate", MetricDirection.DIAGNOSTIC, "Correction activity, but also possible instability."),
            new MetricDefinition("attentionSpendPerBill", "Attention spend per bill", MetricDirection.DIAGNOSTIC, "Scarce attention use."),
            new MetricDefinition("objectionWindowRate", "Objection-window rate", MetricDirection.DIAGNOSTIC, "Public contestation activity."),
            new MetricDefinition("policyShift", "Policy shift", MetricDirection.DIAGNOSTIC, "Substantive movement; risky when uncontrolled, useful when reform is needed.")
    );

    private static final Map<String, MetricDefinition> BY_KEY = DEFINITIONS.stream()
            .collect(Collectors.toUnmodifiableMap(MetricDefinition::key, Function.identity()));

    public static List<MetricDefinition> definitions() {
        return DEFINITIONS;
    }

    public static MetricDefinition require(String key) {
        MetricDefinition definition = BY_KEY.get(key);
        if (definition == null) {
            throw new IllegalArgumentException("Unknown metric: " + key);
        }
        return definition;
    }

    public static double clamp01(double value) {
        return Math.clamp(value, 0.0, 1.0);
    }

    public static double higherIsBetter(double value) {
        return clamp01(value);
    }

    public static double lowerIsBetter(double value) {
        return 1.0 - clamp01(value);
    }

    public static double lowerIsBetter(double value, double maxValue) {
        if (maxValue <= 0.0) {
            return lowerIsBetter(value);
        }
        return 1.0 - clamp01(value / maxValue);
    }

    public static double average(double... values) {
        if (values.length == 0) {
            return 0.0;
        }
        double sum = 0.0;
        for (double value : values) {
            sum += clamp01(value);
        }
        return sum / values.length;
    }
}
