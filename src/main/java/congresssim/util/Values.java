package congresssim.util;

public final class Values {
    private Values() {
    }

    public static double clamp(double value, double min, double max) {
        return Math.clamp(value, min, max);
    }

    public static void requireRange(String name, double value, double min, double max) {
        if (Double.isNaN(value) || value < min || value > max) {
            throw new IllegalArgumentException(name + " must be between " + min + " and " + max + ".");
        }
    }
}
