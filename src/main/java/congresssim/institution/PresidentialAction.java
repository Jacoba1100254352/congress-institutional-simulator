package congresssim.institution;

public record PresidentialAction(
        boolean vetoed,
        boolean overrideAttempted,
        boolean overridden
) {
    public static PresidentialAction none() {
        return new PresidentialAction(false, false, false);
    }
}

