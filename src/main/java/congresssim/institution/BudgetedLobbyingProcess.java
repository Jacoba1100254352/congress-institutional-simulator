package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.LobbyGroup;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class BudgetedLobbyingProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<LobbyGroup> lobbyGroups;
    private final Map<String, Double> remainingBudgetByGroup = new HashMap<>();
    private final double spendScale;
    private final double pressurePerSpend;
    private final double publicCampaignEffect;

    public BudgetedLobbyingProcess(
            String name,
            LegislativeProcess innerProcess,
            List<LobbyGroup> lobbyGroups,
            double spendScale,
            double pressurePerSpend,
            double publicCampaignEffect
    ) {
        Values.requireRange("spendScale", spendScale, 0.0, 10.0);
        Values.requireRange("pressurePerSpend", pressurePerSpend, 0.0, 1.0);
        Values.requireRange("publicCampaignEffect", publicCampaignEffect, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.lobbyGroups = List.copyOf(lobbyGroups);
        this.spendScale = spendScale;
        this.pressurePerSpend = pressurePerSpend;
        this.publicCampaignEffect = publicCampaignEffect;
        for (LobbyGroup group : lobbyGroups) {
            remainingBudgetByGroup.put(group.id(), group.budget());
        }
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Bill pressuredBill = applyLobbying(bill);
        return innerProcess.consider(pressuredBill, context);
    }

    private Bill applyLobbying(Bill bill) {
        double totalSpend = 0.0;
        double defensiveSpend = 0.0;
        double pressure = bill.lobbyPressure();
        double publicSupport = bill.publicSupport();
        double privateGain = bill.privateGain();

        for (LobbyGroup group : lobbyGroups) {
            if (!group.issueDomain().equals(bill.issueDomain()) && !bill.antiLobbyingReform()) {
                continue;
            }

            double remainingBudget = remainingBudgetByGroup.getOrDefault(group.id(), group.budget());
            if (remainingBudget <= 0.000001) {
                continue;
            }

            double spendIntent = bill.antiLobbyingReform()
                    ? defensiveSpendIntent(group, bill)
                    : supportiveSpendIntent(group, bill);
            double spend = Math.min(remainingBudget, spendIntent * spendScale);
            if (spend <= 0.000001) {
                continue;
            }

            remainingBudgetByGroup.put(group.id(), remainingBudget - spend);
            totalSpend += spend;

            if (bill.antiLobbyingReform()) {
                defensiveSpend += spend;
                pressure -= pressurePerSpend * group.influenceIntensity() * spend;
                publicSupport -= publicCampaignEffect * group.publicCampaignSkill() * spend * 0.18;
            } else {
                pressure += pressurePerSpend * group.influenceIntensity() * spend * policyFit(group, bill);
                publicSupport += publicCampaignEffect * group.publicCampaignSkill() * group.informationBias() * spend * 0.10;
                privateGain += group.influenceIntensity() * spend * 0.08;
            }
        }

        return bill.withLobbyActivity(
                Values.clamp(pressure, -1.0, 1.0),
                Values.clamp(publicSupport, 0.0, 1.0),
                Values.clamp(privateGain, 0.0, 1.0),
                totalSpend,
                defensiveSpend
        );
    }

    private static double supportiveSpendIntent(LobbyGroup group, Bill bill) {
        double fit = policyFit(group, bill);
        double privateUpside = 0.30 + bill.privateGain();
        double salience = 0.35 + bill.salience();
        return Values.clamp(group.influenceIntensity() * fit * privateUpside * salience, 0.0, 1.0);
    }

    private static double defensiveSpendIntent(LobbyGroup group, Bill bill) {
        double threat = (0.45 * bill.publicBenefit()) + (0.35 * bill.publicSupport()) + (0.20 * bill.salience());
        return Values.clamp(group.defensiveMultiplier() * group.influenceIntensity() * threat, 0.0, 1.5);
    }

    private static double policyFit(LobbyGroup group, Bill bill) {
        return Values.clamp(1.0 - (Math.abs(group.preferredPolicyPosition() - bill.ideologyPosition()) / 2.0), 0.0, 1.0);
    }
}
