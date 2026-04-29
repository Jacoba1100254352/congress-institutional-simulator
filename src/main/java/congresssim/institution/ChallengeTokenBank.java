package congresssim.institution;

import congresssim.model.Legislator;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

final class ChallengeTokenBank {
    private final Map<String, Integer> remainingTokens;
    private int spentTokens;

    private ChallengeTokenBank(Map<String, Integer> remainingTokens) {
        this.remainingTokens = new LinkedHashMap<>(remainingTokens);
    }

    static ChallengeTokenBank byParty(List<Legislator> legislators, int tokensPerParty) {
        if (tokensPerParty < 0) {
            throw new IllegalArgumentException("tokensPerParty must not be negative.");
        }

        Map<String, Integer> tokens = new LinkedHashMap<>();
        for (Legislator legislator : legislators) {
            tokens.putIfAbsent(legislator.party(), tokensPerParty);
        }
        return new ChallengeTokenBank(tokens);
    }

    static ChallengeTokenBank byLegislator(List<Legislator> legislators, int tokensPerLegislator) {
        if (tokensPerLegislator < 0) {
            throw new IllegalArgumentException("tokensPerLegislator must not be negative.");
        }

        Map<String, Integer> tokens = new LinkedHashMap<>();
        for (Legislator legislator : legislators) {
            tokens.put(legislator.id(), tokensPerLegislator);
        }
        return new ChallengeTokenBank(tokens);
    }

    static ChallengeTokenBank create(
            List<Legislator> legislators,
            ChallengeTokenAllocation allocation,
            int tokensPerOwner
    ) {
        return switch (allocation) {
            case PARTY -> byParty(legislators, tokensPerOwner);
            case LEGISLATOR -> byLegislator(legislators, tokensPerOwner);
        };
    }

    boolean hasToken(String owner) {
        return remainingTokens.getOrDefault(owner, 0) > 0;
    }

    void spend(String owner) {
        int remaining = remainingTokens.getOrDefault(owner, 0);
        if (remaining <= 0) {
            throw new IllegalStateException("No challenge tokens remain for " + owner + ".");
        }
        remainingTokens.put(owner, remaining - 1);
        spentTokens++;
    }

    int spentTokens() {
        return spentTokens;
    }
}
