package congresssim.calibration;

import java.util.Objects;

public record CalibrationTarget(
        String key,
        String empiricalDataset,
        String empiricalQuantity,
        String simulatorMetric,
        String validationUse,
        String notes
) {
    public CalibrationTarget {
        key = requireText("key", key);
        empiricalDataset = requireText("empiricalDataset", empiricalDataset);
        empiricalQuantity = requireText("empiricalQuantity", empiricalQuantity);
        simulatorMetric = requireText("simulatorMetric", simulatorMetric);
        validationUse = requireText("validationUse", validationUse);
        notes = Objects.requireNonNullElse(notes, "");
    }

    private static String requireText(String name, String value) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(name + " must not be blank.");
        }
        return value;
    }
}
