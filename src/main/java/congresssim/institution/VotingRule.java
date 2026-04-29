package congresssim.institution;

public interface VotingRule {
    String name();

    boolean passes(int yayCount, int nayCount);
}

