package congresssim.institution.voting;

public final class DefaultPassUnlessVetoedRule implements VotingRule {
    private final double vetoThreshold;

    public DefaultPassUnlessVetoedRule(double vetoThreshold) {
        if (vetoThreshold <= 0.0 || vetoThreshold > 1.0) {
            throw new IllegalArgumentException("vetoThreshold must be in (0, 1].");
        }
        this.vetoThreshold = vetoThreshold;
    }

    @Override
    public String name() {
        return "default pass unless " + Math.round(vetoThreshold * 100.0) + " percent block";
    }

    @Override
    public boolean passes(int yayCount, int nayCount) {
        int total = yayCount + nayCount;
        if (total == 0) {
            return false;
        }
        int requiredBlockVotes = (int) Math.ceil(vetoThreshold * total);
        return nayCount < requiredBlockVotes;
    }
}

