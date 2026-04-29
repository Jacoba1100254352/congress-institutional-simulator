package congresssim.simulation;

public enum MetricDirection {
    HIGHER_IS_BETTER("higher is better", "↑"),
    LOWER_IS_BETTER("lower is better", "↓"),
    DIAGNOSTIC("diagnostic", "diag.");

    private final String description;
    private final String marker;

    MetricDirection(String description, String marker) {
        this.description = description;
        this.marker = marker;
    }

    public String description() {
        return description;
    }

    public String marker() {
        return marker;
    }
}
