package congresssim.simulation;

import congresssim.model.Legislator;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class CommitteeFactory {
    private CommitteeFactory() {
    }

    public static List<Legislator> select(
            List<Legislator> legislators,
            CommitteeComposition composition,
            int targetSize
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        int size = Math.clamp(targetSize, 1, legislators.size());
        return switch (composition) {
            case REPRESENTATIVE -> representative(legislators, size);
            case MAJORITY_CONTROLLED -> majorityControlled(legislators, size);
            case POLARIZED -> sortedTake(
                    legislators,
                    size,
                    Comparator.comparingDouble((Legislator legislator) -> Math.abs(legislator.ideology())).reversed()
            );
            case EXPERT -> sortedTake(
                    legislators,
                    size,
                    Comparator.comparingDouble(CommitteeFactory::expertiseScore).reversed()
            );
            case CAPTURED -> sortedTake(
                    legislators,
                    size,
                    Comparator.comparingDouble(Legislator::lobbySensitivity).reversed()
            );
            case PROPORTIONAL_PARTY -> proportionalParty(legislators, size);
            case FORCED_PARTY_BALANCE -> forcedPartyBalance(legislators, size);
            case MINORITY_PROTECTED -> minorityProtected(legislators, size);
            case RANDOM_LOTTERY -> deterministicLottery(legislators, size, 101L);
            case ROTATING_LOTTERY -> deterministicLottery(legislators, size, 202L + size);
            case INDEPENDENT_EXPERT, ISSUE_EXPERT -> independentExpert(legislators, size);
            case LEADERSHIP_STACKED -> leadershipStacked(legislators, size);
            case EXPERTISE_QUALIFIED_LOTTERY -> expertiseQualifiedLottery(legislators, size);
            case MIXED_LEGISLATOR_CITIZEN -> forcedPartyBalance(legislators, size);
            case MINORITY_VETO_HIGH_RISK -> minorityVetoSeat(legislators, size);
            case MIXED_PARLIAMENTARIAN_CITIZEN -> forcedPartyBalance(legislators, size);
            case OPPOSITION_CHAIRED, PUBLIC_ACCOUNTS_STYLE -> oppositionChaired(legislators, size);
        };
    }

    public static CommitteeSelectionResult select(
            List<Legislator> legislators,
            CommitteeSelectionConfig config
    ) {
        CommitteeComposition composition = switch (config.partyQuotaRule()) {
            case REPRESENTATIVE -> CommitteeComposition.REPRESENTATIVE;
            case PROPORTIONAL_PARTY -> CommitteeComposition.PROPORTIONAL_PARTY;
            case FORCED_BALANCE -> CommitteeComposition.FORCED_PARTY_BALANCE;
            case MINORITY_VETO_SEAT -> CommitteeComposition.MINORITY_VETO_HIGH_RISK;
            case EXPERTISE_WEIGHTED -> CommitteeComposition.EXPERTISE_QUALIFIED_LOTTERY;
            case LEADERSHIP_CONTROLLED -> CommitteeComposition.LEADERSHIP_STACKED;
            case INDEPENDENT -> CommitteeComposition.INDEPENDENT_EXPERT;
        };
        List<Legislator> selected = select(legislators, composition, config.targetSize());
        selected = applyConfigScoring(selected, legislators, config);
        Legislator chair = chairFor(selected, config.chairAllocationRule());
        double citizenWeight = config.citizenMemberRatio();
        return new CommitteeSelectionResult(
                selected,
                chair,
                1.0 - citizenWeight,
                citizenWeight,
                config.quorumPartyBalance(),
                config.topicReferralAuthority()
        );
    }

    private static List<Legislator> representative(List<Legislator> legislators, int size) {
        List<Legislator> sorted = new ArrayList<>(legislators);
        sorted.sort(Comparator.comparingDouble(Legislator::ideology));

        if (size <= 1) {
            return List.of(sorted.get(sorted.size() / 2));
        }

        List<Legislator> subset = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            int index = (int) Math.round(i * (sorted.size() - 1.0) / (size - 1.0));
            subset.add(sorted.get(index));
        }
        return subset;
    }

    private static List<Legislator> majorityControlled(List<Legislator> legislators, int size) {
        Map<String, Integer> partyCounts = new HashMap<>();
        for (Legislator legislator : legislators) {
            partyCounts.merge(legislator.party(), 1, Integer::sum);
        }

        String majorityParty = partyCounts.entrySet()
                .stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse(legislators.getFirst().party());

        List<Legislator> majorityMembers = legislators.stream()
                .filter(legislator -> legislator.party().equals(majorityParty))
                .toList();

        List<Legislator> committee = new ArrayList<>(representative(majorityMembers, Math.min(size, majorityMembers.size())));
        if (committee.size() >= size) {
            return committee;
        }

        Set<String> selectedIds = new HashSet<>();
        for (Legislator legislator : committee) {
            selectedIds.add(legislator.id());
        }
        for (Legislator legislator : representative(legislators, size)) {
            if (committee.size() >= size) {
                break;
            }
            if (selectedIds.add(legislator.id())) {
                committee.add(legislator);
            }
        }
        return committee;
    }

    private static List<Legislator> proportionalParty(List<Legislator> legislators, int size) {
        Map<String, List<Legislator>> byParty = byParty(legislators);
        List<String> parties = byParty.keySet().stream().sorted().toList();
        Map<String, Integer> seatTargets = proportionalSeatTargets(parties, byParty, legislators.size(), size);
        List<Legislator> committee = new ArrayList<>();
        for (String party : parties) {
            List<Legislator> partyMembers = new ArrayList<>(byParty.get(party));
            partyMembers.sort(Comparator.comparingDouble(Legislator::ideology));
            committee.addAll(evenlySpaced(partyMembers, seatTargets.getOrDefault(party, 0)));
        }
        return trimOrFill(committee, representative(legislators, size), size);
    }

    private static List<Legislator> forcedPartyBalance(List<Legislator> legislators, int size) {
        Map<String, List<Legislator>> byParty = byParty(legislators);
        List<String> parties = byParty.entrySet()
                .stream()
                .sorted(Map.Entry.<String, List<Legislator>>comparingByValue(Comparator.comparingInt(List::size)).reversed())
                .map(Map.Entry::getKey)
                .toList();
        List<Legislator> committee = new ArrayList<>();
        int cursor = 0;
        while (committee.size() < size && cursor < size * Math.max(1, parties.size())) {
            String party = parties.get(cursor % parties.size());
            List<Legislator> members = byParty.get(party).stream()
                    .sorted(Comparator.comparingDouble(Legislator::ideology))
                    .toList();
            int index = Math.min(members.size() - 1, cursor / parties.size());
            addIfAbsent(committee, members.get(index), size);
            cursor++;
        }
        return trimOrFill(committee, representative(legislators, size), size);
    }

    private static List<Legislator> minorityProtected(List<Legislator> legislators, int size) {
        Map<String, List<Legislator>> byParty = byParty(legislators);
        List<String> partiesByAscendingSize = byParty.entrySet()
                .stream()
                .sorted(Comparator.comparingInt(entry -> entry.getValue().size()))
                .map(Map.Entry::getKey)
                .toList();
        List<Legislator> committee = new ArrayList<>();
        for (String party : partiesByAscendingSize) {
            if (committee.size() >= Math.max(1, Math.min(size / 3, partiesByAscendingSize.size()))) {
                break;
            }
            List<Legislator> members = byParty.get(party);
            addIfAbsent(committee, representative(members, 1).getFirst(), size);
        }
        addUnique(committee, proportionalParty(legislators, size), size);
        return trimOrFill(committee, representative(legislators, size), size);
    }

    private static List<Legislator> deterministicLottery(List<Legislator> legislators, int size, long salt) {
        List<Legislator> shuffled = new ArrayList<>(legislators);
        Collections.shuffle(shuffled, new Random(salt + stableSeed(legislators)));
        return shuffled.stream().limit(size).toList();
    }

    private static List<Legislator> independentExpert(List<Legislator> legislators, int size) {
        return legislators.stream()
                .sorted(Comparator.comparingDouble(CommitteeFactory::independentExpertScore).reversed())
                .limit(size)
                .toList();
    }

    private static List<Legislator> leadershipStacked(List<Legislator> legislators, int size) {
        List<Legislator> majority = majorityControlled(legislators, size);
        return majority.stream()
                .sorted(Comparator.comparingDouble(Legislator::partyLoyalty).reversed())
                .limit(size)
                .toList();
    }

    private static List<Legislator> expertiseQualifiedLottery(List<Legislator> legislators, int size) {
        int poolSize = Math.clamp(size * 3, size, legislators.size());
        List<Legislator> pool = legislators.stream()
                .sorted(Comparator.comparingDouble(CommitteeFactory::expertiseScore).reversed())
                .limit(poolSize)
                .toList();
        return deterministicLottery(pool, size, 303L);
    }

    private static List<Legislator> oppositionChaired(List<Legislator> legislators, int size) {
        Map<String, Integer> counts = new HashMap<>();
        for (Legislator legislator : legislators) {
            counts.merge(legislator.party(), 1, Integer::sum);
        }
        String majorityParty = counts.entrySet()
                .stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse(legislators.getFirst().party());
        List<Legislator> committee = new ArrayList<>();
        legislators.stream()
                .filter(legislator -> !legislator.party().equals(majorityParty))
                .sorted(Comparator.comparingDouble(CommitteeFactory::expertiseScore).reversed())
                .findFirst()
                .ifPresent(legislator -> addIfAbsent(committee, legislator, size));
        addUnique(committee, proportionalParty(legislators, size), size);
        return trimOrFill(committee, representative(legislators, size), size);
    }

    private static List<Legislator> minorityVetoSeat(List<Legislator> legislators, int size) {
        List<Legislator> committee = new ArrayList<>();
        Map<String, List<Legislator>> byParty = byParty(legislators);
        byParty.entrySet()
                .stream()
                .min(Comparator.comparingInt(entry -> entry.getValue().size()))
                .map(entry -> representative(entry.getValue(), 1).getFirst())
                .ifPresent(legislator -> addIfAbsent(committee, legislator, size));
        addUnique(committee, minorityProtected(legislators, size), size);
        return trimOrFill(committee, representative(legislators, size), size);
    }

    private static List<Legislator> applyConfigScoring(
            List<Legislator> selected,
            List<Legislator> legislators,
            CommitteeSelectionConfig config
    ) {
        if (config.expertiseWeight() <= 0.000001
                && config.independenceWeight() <= 0.000001
                && config.leadershipControlStrength() <= 0.000001) {
            return selected;
        }
        List<Legislator> pool = new ArrayList<>(legislators);
        pool.sort(Comparator.<Legislator>comparingDouble(legislator -> configuredScore(legislator, config)).reversed());
        List<Legislator> adjusted = new ArrayList<>(selected);
        int replacements = (int) Math.round(config.targetSize()
                * Math.clamp((config.expertiseWeight() + config.independenceWeight() + config.leadershipControlStrength()) / 3.0, 0.0, 0.60));
        for (Legislator legislator : pool) {
            if (replacements <= 0) {
                break;
            }
            if (adjusted.stream().noneMatch(existing -> existing.id().equals(legislator.id()))) {
                if (!adjusted.isEmpty()) {
                    adjusted.remove(adjusted.size() - 1);
                }
                adjusted.add(legislator);
                replacements--;
            }
        }
        return trimOrFill(adjusted, selected, config.targetSize());
    }

    private static double configuredScore(Legislator legislator, CommitteeSelectionConfig config) {
        double expertise = expertiseScore(legislator);
        double independence = 1.0 - ((legislator.partyLoyalty() + legislator.lobbySensitivity()) / 2.0);
        double leadership = legislator.partyLoyalty();
        double issueFit = issueFit(legislator, config.issueDomain());
        return (config.expertiseWeight() * expertise)
                + (config.independenceWeight() * independence)
                + (config.leadershipControlStrength() * leadership)
                + (0.15 * issueFit);
    }

    private static double issueFit(Legislator legislator, String issueDomain) {
        int hash = Math.floorMod((legislator.id() + ":" + issueDomain).hashCode(), 1000);
        return hash / 1000.0;
    }

    private static Legislator chairFor(List<Legislator> members, ChairAllocationRule rule) {
        return switch (rule) {
            case MAJORITY -> members.getFirst();
            case OPPOSITION -> oppositionChaired(members, 1).getFirst();
            case EXPERT -> members.stream()
                    .max(Comparator.comparingDouble(CommitteeFactory::expertiseScore))
                    .orElse(members.getFirst());
            case RANDOM_LOTTERY -> deterministicLottery(members, 1, 707L).getFirst();
            case ROTATING -> deterministicLottery(members, 1, 909L + members.size()).getFirst();
        };
    }

    private static List<Legislator> sortedTake(
            List<Legislator> legislators,
            int size,
            Comparator<Legislator> comparator
    ) {
        return legislators.stream()
                .sorted(comparator)
                .limit(size)
                .toList();
    }

    private static Map<String, List<Legislator>> byParty(List<Legislator> legislators) {
        Map<String, List<Legislator>> byParty = new HashMap<>();
        for (Legislator legislator : legislators) {
            byParty.computeIfAbsent(legislator.party(), ignored -> new ArrayList<>()).add(legislator);
        }
        return byParty;
    }

    private static Map<String, Integer> proportionalSeatTargets(
            List<String> parties,
            Map<String, List<Legislator>> byParty,
            int totalMembers,
            int size
    ) {
        Map<String, Integer> seats = new HashMap<>();
        Map<String, Double> remainders = new HashMap<>();
        int assigned = 0;
        for (String party : parties) {
            double exact = ((double) byParty.get(party).size() / totalMembers) * size;
            int whole = (int) Math.floor(exact);
            seats.put(party, whole);
            remainders.put(party, exact - whole);
            assigned += whole;
        }
        while (assigned < size) {
            String best = parties.stream()
                    .max(Comparator.comparingDouble(party -> remainders.getOrDefault(party, 0.0)))
                    .orElse(parties.getFirst());
            seats.merge(best, 1, Integer::sum);
            remainders.put(best, -1.0);
            assigned++;
        }
        return seats;
    }

    private static List<Legislator> evenlySpaced(List<Legislator> sorted, int size) {
        if (sorted.isEmpty() || size <= 0) {
            return List.of();
        }
        if (size == 1) {
            return List.of(sorted.get(sorted.size() / 2));
        }
        List<Legislator> subset = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            int index = (int) Math.round(i * (sorted.size() - 1.0) / (size - 1.0));
            subset.add(sorted.get(index));
        }
        return subset;
    }

    private static List<Legislator> trimOrFill(List<Legislator> committee, List<Legislator> fallback, int size) {
        List<Legislator> result = new ArrayList<>();
        for (Legislator legislator : committee) {
            addIfAbsent(result, legislator, size);
        }
        for (Legislator legislator : fallback) {
            addIfAbsent(result, legislator, size);
        }
        return result;
    }

    private static void addUnique(List<Legislator> committee, List<Legislator> candidates, int size) {
        for (Legislator legislator : candidates) {
            addIfAbsent(committee, legislator, size);
        }
    }

    private static void addIfAbsent(List<Legislator> committee, Legislator legislator, int size) {
        if (committee.size() >= size) {
            return;
        }
        boolean alreadyPresent = committee.stream().anyMatch(member -> member.id().equals(legislator.id()));
        if (!alreadyPresent) {
            committee.add(legislator);
        }
    }

    private static long stableSeed(List<Legislator> legislators) {
        long seed = 17L;
        for (Legislator legislator : legislators) {
            seed = (seed * 31L) + legislator.id().hashCode();
        }
        return seed;
    }

    private static double expertiseScore(Legislator legislator) {
        return legislator.compromisePreference()
                + legislator.reputationSensitivity()
                + legislator.constituencySensitivity()
                - legislator.lobbySensitivity();
    }

    private static double independentExpertScore(Legislator legislator) {
        return expertiseScore(legislator)
                - (0.30 * legislator.partyLoyalty())
                - (0.45 * legislator.lobbySensitivity())
                - (0.15 * Math.abs(legislator.ideology()));
    }
}
