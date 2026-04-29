package congresssim.calibration;

import congresssim.util.Values;

public record CalibrationBenchmark(
        String key,
        String empiricalDataset,
        String empiricalQuantity,
        String scenarioKey,
        String simulatorMetric,
        double minimum,
        double maximum,
        String source,
        String notes
) {
    public CalibrationBenchmark {
        key = requireText("key", key);
        empiricalDataset = requireText("empiricalDataset", empiricalDataset);
        empiricalQuantity = requireText("empiricalQuantity", empiricalQuantity);
        scenarioKey = requireText("scenarioKey", scenarioKey);
        simulatorMetric = requireText("simulatorMetric", simulatorMetric);
        source = requireText("source", source);
        notes = notes == null ? "" : notes;
        Values.requireRange("minimum", minimum, 0.0, 100.0);
        Values.requireRange("maximum", maximum, 0.0, 100.0);
        if (minimum > maximum) {
            throw new IllegalArgumentException("minimum must be <= maximum.");
        }
    }

    private static String requireText(String name, String value) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(name + " must not be blank.");
        }
        return value;
    }
}
