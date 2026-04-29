package congresssim.simulation;

import congresssim.model.Legislator;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
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
        };
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

    private static double expertiseScore(Legislator legislator) {
        return legislator.compromisePreference()
                + legislator.reputationSensitivity()
                + legislator.constituencySensitivity()
                - legislator.lobbySensitivity();
    }
}
