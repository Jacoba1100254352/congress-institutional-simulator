package congresssim.institution;

public record AccessDecision(boolean granted, String reason) {
    public static AccessDecision granted(String reason) {
        return new AccessDecision(true, reason);
    }

    public static AccessDecision denied(String reason) {
        return new AccessDecision(false, reason);
    }
}

