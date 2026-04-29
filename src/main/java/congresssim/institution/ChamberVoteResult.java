package congresssim.institution;

public record ChamberVoteResult(
        String chamberName,
        String ruleName,
        int yayCount,
        int nayCount,
        boolean passed
) {
    public int totalVotes() {
        return yayCount + nayCount;
    }

    public double yayShare() {
        int total = totalVotes();
        return total == 0 ? 0.0 : (double) yayCount / total;
    }

    public double nayShare() {
        int total = totalVotes();
        return total == 0 ? 0.0 : (double) nayCount / total;
    }
}

