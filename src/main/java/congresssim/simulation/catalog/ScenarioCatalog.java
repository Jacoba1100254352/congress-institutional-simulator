package congresssim.simulation.catalog;

import congresssim.simulation.Scenario;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class ScenarioCatalog {
    private static final List<String> DEFAULT_SCENARIO_KEYS = List.of(
            "current-system",
            "simple-majority",
            "supermajority-60",
            "bicameral-majority",
            "presidential-veto",
            "leadership-cartel-majority",
            "committee-regular-order",
            "cloture-conference-review",
            "constitutional-court-architecture-majority",
            "parliamentary-coalition-confidence",
            "citizen-initiative-referendum",
            "district-population-majority",
            "simple-majority-alternatives-pairwise",
            "citizen-assembly-threshold",
            "public-interest-majority",
            "agenda-lottery-majority",
            "quadratic-attention-majority",
            "proposal-bond-majority",
            "harm-weighted-majority",
            "compensation-majority",
            "package-bargaining-majority",
            "multidimensional-package-majority",
            "omnibus-bargaining-majority",
            "law-registry-majority",
            "public-objection-majority",
            "anti-capture-majority-bundle",
            "influence-system-majority",
            "risk-routed-majority",
            "portfolio-hybrid-legislature",
            "expanded-portfolio-hybrid-legislature",
            "norm-erosion-majority",
            "long-horizon-learning-majority",
            "default-pass",
            "default-pass-challenge",
            "default-pass-multiround-mediation-challenge"
    );

    private ScenarioCatalog() {
    }

    public static List<Scenario> defaultScenarios() {
        return scenariosForKeys(DEFAULT_SCENARIO_KEYS);
    }

    public static List<String> defaultScenarioKeys() {
        return DEFAULT_SCENARIO_KEYS;
    }

    public static List<Scenario> allScenarios() {
        return entries().stream()
                .filter(entry -> isBreadthCatalogKey(entry.key()))
                .map(ScenarioEntry::scenario)
                .toList();
    }

    public static List<String> allScenarioKeys() {
        return entries().stream()
                .map(ScenarioEntry::key)
                .filter(ScenarioCatalog::isBreadthCatalogKey)
                .toList();
    }

    public static List<Scenario> historicalScenarios() {
        return entries().stream().map(ScenarioEntry::scenario).toList();
    }

    public static List<Scenario> scenariosForKeys(List<String> keys) {
        Map<String, Scenario> byKey = new LinkedHashMap<>();
        for (ScenarioEntry entry : entries()) {
            byKey.put(entry.key(), entry.scenario());
        }

        List<Scenario> scenarios = new ArrayList<>();
        for (String key : keys) {
            Scenario scenario = byKey.get(key);
            if (scenario == null) {
                throw new IllegalArgumentException("Unknown scenario key: " + key);
            }
            scenarios.add(scenario);
        }
        return scenarios;
    }

    public static List<String> scenarioKeys() {
        return entries().stream().map(ScenarioEntry::key).toList();
    }

    private static boolean isBreadthCatalogKey(String key) {
        return !key.startsWith("default-pass") || DEFAULT_SCENARIO_KEYS.contains(key);
    }

    private static List<ScenarioEntry> entries() {
        List<ScenarioEntry> entries = new ArrayList<>();
        entries.addAll(BroadSystemScenarioFamily.entries());
        entries.addAll(DefaultPassSafeguardScenarioFamily.entries());
        entries.addAll(PolicyTournamentScenarioFamily.entries());
        entries.addAll(DefaultPassStressScenarioFamily.entries());
        entries.addAll(ChamberCommitteeScenarioFamily.entries());
        return List.copyOf(entries);
    }
}
