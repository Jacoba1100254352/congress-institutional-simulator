package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.LobbyCaptureStrategy;
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
    private final double publicFinancingStrength;
    private final double publicAdvocateStrength;
    private final double blindReviewStrength;
    private final double defensiveCapShare;
    private final boolean adaptiveStrategies;
    private final Map<String, LobbyCaptureStrategy> strategyByGroup = new HashMap<>();

    public BudgetedLobbyingProcess(
            String name,
            LegislativeProcess innerProcess,
            List<LobbyGroup> lobbyGroups,
            double spendScale,
            double pressurePerSpend,
            double publicCampaignEffect
    ) {
        this(
                name,
                innerProcess,
                lobbyGroups,
                spendScale,
                pressurePerSpend,
                publicCampaignEffect,
                0.0,
                0.0,
                0.0,
                1.0
        );
    }

    public BudgetedLobbyingProcess(
            String name,
            LegislativeProcess innerProcess,
            List<LobbyGroup> lobbyGroups,
            double spendScale,
            double pressurePerSpend,
            double publicCampaignEffect,
            boolean adaptiveStrategies
    ) {
        this(
                name,
                innerProcess,
                lobbyGroups,
                spendScale,
                pressurePerSpend,
                publicCampaignEffect,
                0.0,
                0.0,
                0.0,
                1.0,
                adaptiveStrategies
        );
    }

    public BudgetedLobbyingProcess(
            String name,
            LegislativeProcess innerProcess,
            List<LobbyGroup> lobbyGroups,
            double spendScale,
            double pressurePerSpend,
            double publicCampaignEffect,
            double publicFinancingStrength,
            double publicAdvocateStrength,
            double blindReviewStrength,
            double defensiveCapShare
    ) {
        this(
                name,
                innerProcess,
                lobbyGroups,
                spendScale,
                pressurePerSpend,
                publicCampaignEffect,
                publicFinancingStrength,
                publicAdvocateStrength,
                blindReviewStrength,
                defensiveCapShare,
                false
        );
    }

    public BudgetedLobbyingProcess(
            String name,
            LegislativeProcess innerProcess,
            List<LobbyGroup> lobbyGroups,
            double spendScale,
            double pressurePerSpend,
            double publicCampaignEffect,
            double publicFinancingStrength,
            double publicAdvocateStrength,
            double blindReviewStrength,
            double defensiveCapShare,
            boolean adaptiveStrategies
    ) {
        Values.requireRange("spendScale", spendScale, 0.0, 10.0);
        Values.requireRange("pressurePerSpend", pressurePerSpend, 0.0, 1.0);
        Values.requireRange("publicCampaignEffect", publicCampaignEffect, 0.0, 1.0);
        Values.requireRange("publicFinancingStrength", publicFinancingStrength, 0.0, 1.0);
        Values.requireRange("publicAdvocateStrength", publicAdvocateStrength, 0.0, 1.0);
        Values.requireRange("blindReviewStrength", blindReviewStrength, 0.0, 1.0);
        Values.requireRange("defensiveCapShare", defensiveCapShare, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.lobbyGroups = List.copyOf(lobbyGroups);
        this.spendScale = spendScale;
        this.pressurePerSpend = pressurePerSpend;
        this.publicCampaignEffect = publicCampaignEffect;
        this.publicFinancingStrength = publicFinancingStrength;
        this.publicAdvocateStrength = publicAdvocateStrength;
        this.blindReviewStrength = blindReviewStrength;
        this.defensiveCapShare = defensiveCapShare;
        this.adaptiveStrategies = adaptiveStrategies;
        for (LobbyGroup group : lobbyGroups) {
            remainingBudgetByGroup.put(group.id(), group.budget());
            strategyByGroup.put(group.id(), group.captureStrategy());
        }
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Bill pressuredBill = applyLobbying(bill);
        BillOutcome outcome = innerProcess.consider(pressuredBill, context);
        if (adaptiveStrategies) {
            updateStrategies(pressuredBill, outcome);
        }
        return outcome;
    }

    private Bill applyLobbying(Bill bill) {
        double totalSpend = 0.0;
        double defensiveSpend = 0.0;
        double directSpend = 0.0;
        double agendaSpend = 0.0;
        double informationSpend = 0.0;
        double publicCampaignSpend = 0.0;
        double litigationThreatSpend = 0.0;
        double pressure = bill.lobbyPressure();
        double publicSupport = bill.publicSupport();
        double publicBenefit = bill.publicBenefit();
        double privateGain = bill.privateGain();

        for (LobbyGroup group : lobbyGroups) {
            double preference = bill.antiLobbyingReform()
                    ? Math.max(0.45, group.preferenceFor("democracy"))
                    : group.preferenceFor(bill.issueDomain());
            if (preference <= 0.000001) {
                continue;
            }

            double remainingBudget = remainingBudgetByGroup.getOrDefault(group.id(), group.budget());
            if (remainingBudget <= 0.000001) {
                continue;
            }

            double spendIntent = bill.antiLobbyingReform()
                    ? defensiveSpendIntent(group, bill)
                    : supportiveSpendIntent(group, bill, preference);
            double spend = Math.min(remainingBudget, spendIntent * spendScale);
            if (bill.antiLobbyingReform()) {
                spend = Math.min(spend, group.budget() * defensiveCapShare);
            }
            if (spend <= 0.000001) {
                continue;
            }

            remainingBudgetByGroup.put(group.id(), remainingBudget - spend);
            totalSpend += spend;
            LobbyCaptureStrategy strategy = strategyByGroup.getOrDefault(group.id(), group.captureStrategy());
            ChannelAllocation allocation = ChannelAllocation.forStrategy(strategy, spend);
            directSpend += allocation.direct();
            agendaSpend += allocation.agenda();
            informationSpend += allocation.information();
            publicCampaignSpend += allocation.publicCampaign();
            litigationThreatSpend += allocation.litigationThreat();

            if (bill.antiLobbyingReform()) {
                defensiveSpend += spend;
                pressure -= pressurePerSpend * group.influenceIntensity() * defensivePressure(allocation, group);
                publicSupport -= publicCampaignEffect * group.publicCampaignSkill() * allocation.publicCampaign() * 0.18;
                publicSupport -= pressurePerSpend * group.influenceIntensity() * allocation.litigationThreat() * 0.08;
                publicBenefit -= group.informationBias() * allocation.information() * 0.04;
            } else {
                double fit = policyFit(group, bill) * preference;
                double agendaEffectiveness = 1.0 - (blindReviewStrength * 0.75);
                double informationEffectiveness = 1.0 - (blindReviewStrength * 0.85);
                double publicCampaignEffectiveness = 1.0 - (blindReviewStrength * 0.35);
                double mismatchPenalty = publicMismatchPenalty(group, bill);
                pressure += pressurePerSpend * group.influenceIntensity() * fit
                        * ((0.95 * allocation.direct()) + (agendaEffectiveness * allocation.agenda() * 0.78));
                publicSupport += publicCampaignEffect * group.publicCampaignSkill() * group.informationBias()
                        * publicCampaignEffectiveness * allocation.publicCampaign() * 0.10;
                publicSupport += group.informationBias() * informationEffectiveness * allocation.information() * 0.05;
                publicSupport -= mismatchPenalty * allocation.publicCampaign() * 0.04;
                publicBenefit -= group.informationBias() * informationEffectiveness * allocation.information() * 0.03;
                publicBenefit -= allocation.litigationThreat() * 0.025;
                privateGain += group.influenceIntensity() * spend * (0.06 + (0.06 * fit));
            }
        }

        if (publicFinancingStrength > 0.0) {
            double publicCorrection = publicFinancingStrength * (publicBenefit - publicSupport) * 0.35;
            publicSupport += publicCorrection;
            pressure -= Math.max(0.0, pressure) * publicFinancingStrength * 0.22;
            privateGain -= privateGain * publicFinancingStrength * 0.08;
        }
        if (publicAdvocateStrength > 0.0) {
            double publicInterestGap = Math.max(0.0, publicBenefit - privateGain);
            publicSupport += publicAdvocateStrength * publicInterestGap * 0.18;
            publicBenefit += publicAdvocateStrength * publicInterestGap * 0.06;
            pressure -= Math.max(0.0, pressure) * publicAdvocateStrength * 0.30;
        }

        return bill.withLobbyActivity(
                Values.clamp(pressure, -1.0, 1.0),
                Values.clamp(publicSupport, 0.0, 1.0),
                Values.clamp(publicBenefit, 0.0, 1.0),
                Values.clamp(privateGain, 0.0, 1.0),
                totalSpend,
                defensiveSpend,
                directSpend,
                agendaSpend,
                informationSpend,
                publicCampaignSpend,
                litigationThreatSpend
        );
    }

    private void updateStrategies(Bill bill, BillOutcome outcome) {
        if (bill.lobbySpend() <= 0.000001) {
            return;
        }
        for (LobbyGroup group : lobbyGroups) {
            double preference = bill.antiLobbyingReform()
                    ? Math.max(0.45, group.preferenceFor("democracy"))
                    : group.preferenceFor(bill.issueDomain());
            if (preference <= 0.000001) {
                continue;
            }
            LobbyCaptureStrategy current = strategyByGroup.getOrDefault(group.id(), group.captureStrategy());
            strategyByGroup.put(group.id(), nextStrategy(current, bill, outcome));
        }
    }

    private static LobbyCaptureStrategy nextStrategy(
            LobbyCaptureStrategy current,
            Bill bill,
            BillOutcome outcome
    ) {
        if (bill.antiLobbyingReform()) {
            if (!outcome.enacted()) {
                return bill.litigationThreatSpend() >= bill.publicCampaignSpend()
                        ? LobbyCaptureStrategy.LITIGATION_DELAY
                        : LobbyCaptureStrategy.PUBLIC_CAMPAIGN;
            }
            return LobbyCaptureStrategy.PUBLIC_CAMPAIGN;
        }

        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double publicMismatch = Math.max(0.0, bill.publicBenefit() - bill.publicSupport());
        if (outcome.enacted() && captureRisk >= 0.45) {
            return current;
        }
        if (!outcome.enacted() && bill.salience() >= 0.65) {
            return LobbyCaptureStrategy.PUBLIC_CAMPAIGN;
        }
        if (!outcome.enacted() && Math.abs(bill.ideologyPosition() - bill.proposerIdeology()) >= 0.45) {
            return LobbyCaptureStrategy.AGENDA_ACCESS;
        }
        if (publicMismatch >= 0.20) {
            return LobbyCaptureStrategy.INFORMATION_DISTORTION;
        }
        if (bill.privateGain() >= 0.55) {
            return LobbyCaptureStrategy.DIRECT_PRESSURE;
        }
        return LobbyCaptureStrategy.BALANCED;
    }

    private static double supportiveSpendIntent(LobbyGroup group, Bill bill, double preference) {
        double fit = policyFit(group, bill);
        double privateUpside = 0.30 + bill.privateGain();
        double salience = 0.35 + bill.salience();
        double publicMismatch = publicMismatchPenalty(group, bill);
        return Values.clamp(
                group.influenceIntensity() * preference * fit * privateUpside * salience * (1.0 + publicMismatch),
                0.0,
                1.0
        );
    }

    private static double defensiveSpendIntent(LobbyGroup group, Bill bill) {
        double threat = (0.45 * bill.publicBenefit()) + (0.35 * bill.publicSupport()) + (0.20 * bill.salience());
        return Values.clamp(group.defensiveMultiplier() * group.influenceIntensity() * threat, 0.0, 1.5);
    }

    private static double policyFit(LobbyGroup group, Bill bill) {
        return Values.clamp(1.0 - (Math.abs(group.preferredPolicyPosition() - bill.ideologyPosition()) / 2.0), 0.0, 1.0);
    }

    private static double publicMismatchPenalty(LobbyGroup group, Bill bill) {
        double mismatch = Math.max(0.0, bill.publicBenefit() - bill.publicSupport());
        return Math.max(0.0, mismatch - group.publicSupportMismatchTolerance());
    }

    private static double defensivePressure(ChannelAllocation allocation, LobbyGroup group) {
        return (0.95 * allocation.direct())
                + (0.80 * allocation.agenda())
                + (0.55 * allocation.information())
                + (0.45 * allocation.publicCampaign())
                + (0.75 * allocation.litigationThreat())
                + (group.defensiveMultiplier() * 0.05);
    }

    private record ChannelAllocation(
            double direct,
            double agenda,
            double information,
            double publicCampaign,
            double litigationThreat
    ) {
        private static ChannelAllocation forStrategy(LobbyCaptureStrategy strategy, double spend) {
            double[] shares = switch (strategy) {
                case DIRECT_PRESSURE -> new double[]{0.55, 0.15, 0.10, 0.10, 0.10};
                case AGENDA_ACCESS -> new double[]{0.15, 0.48, 0.14, 0.08, 0.15};
                case INFORMATION_DISTORTION -> new double[]{0.10, 0.15, 0.48, 0.17, 0.10};
                case PUBLIC_CAMPAIGN -> new double[]{0.10, 0.10, 0.15, 0.55, 0.10};
                case LITIGATION_DELAY -> new double[]{0.10, 0.14, 0.10, 0.11, 0.55};
                case BALANCED -> new double[]{0.25, 0.20, 0.20, 0.20, 0.15};
            };
            return new ChannelAllocation(
                    spend * shares[0],
                    spend * shares[1],
                    spend * shares[2],
                    spend * shares[3],
                    spend * shares[4]
            );
        }
    }
}
