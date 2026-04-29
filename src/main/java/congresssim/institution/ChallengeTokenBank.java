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

    boolean hasToken(String party) {
        return remainingTokens.getOrDefault(party, 0) > 0;
    }

    void spend(String party) {
        int remaining = remainingTokens.getOrDefault(party, 0);
        if (remaining <= 0) {
            throw new IllegalStateException("No challenge tokens remain for " + party + ".");
        }
        remainingTokens.put(party, remaining - 1);
        spentTokens++;
    }

    int spentTokens() {
        return spentTokens;
    }
}
