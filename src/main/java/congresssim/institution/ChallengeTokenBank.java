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

    static ChallengeTokenBank byProportionalParty(List<Legislator> legislators, int totalTokenMultiplier) {
        if (totalTokenMultiplier < 0) {
            throw new IllegalArgumentException("totalTokenMultiplier must not be negative.");
        }
        Map<String, Integer> partySizes = partySizes(legislators);
        int partyCount = partySizes.size();
        int totalTokens = Math.max(partyCount, totalTokenMultiplier * partyCount);
        Map<String, Integer> tokens = new LinkedHashMap<>();
        for (Map.Entry<String, Integer> entry : partySizes.entrySet()) {
            int allocation = Math.max(1, (int) Math.round(totalTokens * ((double) entry.getValue() / legislators.size())));
            tokens.put(entry.getKey(), allocation);
        }
        return new ChallengeTokenBank(tokens);
    }

    static ChallengeTokenBank byMinorityBonusParty(List<Legislator> legislators, int baseTokensPerParty) {
        if (baseTokensPerParty < 0) {
            throw new IllegalArgumentException("baseTokensPerParty must not be negative.");
        }
        Map<String, Integer> partySizes = partySizes(legislators);
        int largest = partySizes.values().stream().mapToInt(Integer::intValue).max().orElse(0);
        Map<String, Integer> tokens = new LinkedHashMap<>();
        for (Map.Entry<String, Integer> entry : partySizes.entrySet()) {
            int tokensForParty = baseTokensPerParty;
            if (entry.getValue() < largest) {
                tokensForParty = Math.max(tokensForParty + 1, (int) Math.ceil(baseTokensPerParty * 1.55));
            }
            tokens.put(entry.getKey(), tokensForParty);
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
            case PARTY_PROPORTIONAL -> byProportionalParty(legislators, tokensPerOwner);
            case PARTY_MINORITY_BONUS -> byMinorityBonusParty(legislators, tokensPerOwner);
            case LEGISLATOR -> byLegislator(legislators, tokensPerOwner);
        };
    }

    private static Map<String, Integer> partySizes(List<Legislator> legislators) {
        Map<String, Integer> partySizes = new LinkedHashMap<>();
        for (Legislator legislator : legislators) {
            partySizes.merge(legislator.party(), 1, Integer::sum);
        }
        return partySizes;
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
