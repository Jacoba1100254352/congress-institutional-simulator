package congresssim.institution.voting;

public interface VotingRule {
    String name();

    boolean passes(int yayCount, int nayCount);
}

