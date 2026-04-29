package congresssim.model;

import java.util.List;
import java.util.Map;

public record SimulationWorld(
        List<Legislator> legislators,
        List<Bill> bills,
        List<LobbyGroup> lobbyGroups,
        PolicyState initialPolicy,
        Map<String, Double> partyPositions
) {
    public SimulationWorld(
            List<Legislator> legislators,
            List<Bill> bills,
            PolicyState initialPolicy,
            Map<String, Double> partyPositions
    ) {
        this(legislators, bills, List.of(), initialPolicy, partyPositions);
    }

    public SimulationWorld {
        legislators = List.copyOf(legislators);
        bills = List.copyOf(bills);
        lobbyGroups = List.copyOf(lobbyGroups);
        partyPositions = Map.copyOf(partyPositions);
    }
}
