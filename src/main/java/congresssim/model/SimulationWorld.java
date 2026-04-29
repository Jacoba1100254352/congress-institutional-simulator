package congresssim.model;

import java.util.List;
import java.util.Map;

public record SimulationWorld(
        List<Legislator> legislators,
        List<Bill> bills,
        PolicyState initialPolicy,
        Map<String, Double> partyPositions
) {
    public SimulationWorld {
        legislators = List.copyOf(legislators);
        bills = List.copyOf(bills);
        partyPositions = Map.copyOf(partyPositions);
    }
}
