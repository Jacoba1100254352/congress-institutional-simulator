package congresssim.institution;

public final class AffirmativeThresholdRule implements VotingRule {
    private final String name;
    private final double threshold;

    public AffirmativeThresholdRule(String name, double threshold) {
        if (threshold <= 0.0 || threshold > 1.0) {
            throw new IllegalArgumentException("threshold must be in (0, 1].");
        }
        this.name = name;
        this.threshold = threshold;
    }

    public static AffirmativeThresholdRule simpleMajority() {
        return new AffirmativeThresholdRule("simple majority", 0.5);
    }

    public static AffirmativeThresholdRule supermajority(double threshold) {
        return new AffirmativeThresholdRule(Math.round(threshold * 100.0) + " percent passage", threshold);
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public boolean passes(int yayCount, int nayCount) {
        int total = yayCount + nayCount;
        if (total == 0) {
            return false;
        }
        if (threshold == 0.5) {
            return yayCount > nayCount;
        }
        return yayCount >= requiredVotes(total);
    }

    private int requiredVotes(int total) {
        return (int) Math.ceil(threshold * total);
    }
}

