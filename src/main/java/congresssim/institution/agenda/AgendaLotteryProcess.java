package congresssim.institution.agenda;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public final class AgendaLotteryProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess downstreamProcess;
    private final List<Bill> agendaPool;
    private final double slotShare;
    private final boolean weighted;
    private Set<String> selectedBillIds;

    public AgendaLotteryProcess(
            String name,
            LegislativeProcess downstreamProcess,
            List<Bill> agendaPool,
            double slotShare,
            boolean weighted
    ) {
        Values.requireRange("slotShare", slotShare, 0.0, 1.0);
        this.name = name;
        this.downstreamProcess = downstreamProcess;
        this.agendaPool = List.copyOf(agendaPool);
        this.slotShare = slotShare;
        this.weighted = weighted;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        if (selectedBillIds == null) {
            selectedBillIds = selectBills(context);
        }
        if (!selectedBillIds.contains(bill.id())) {
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "not selected by agenda lottery");
        }
        return downstreamProcess.consider(bill, context);
    }

    private Set<String> selectBills(VoteContext context) {
        int slots = Math.clamp((int) Math.round(agendaPool.size() * slotShare), 1, agendaPool.size());
        List<Bill> remaining = new ArrayList<>(agendaPool);
        Set<String> selected = new HashSet<>();
        while (selected.size() < slots && !remaining.isEmpty()) {
            int index = weighted ? weightedIndex(remaining, context) : context.random().nextInt(remaining.size());
            selected.add(remaining.remove(index).id());
        }
        return selected;
    }

    private static int weightedIndex(List<Bill> bills, VoteContext context) {
        double totalWeight = 0.0;
        for (Bill bill : bills) {
            totalWeight += lotteryWeight(bill);
        }
        double draw = context.random().nextDouble() * totalWeight;
        double cumulative = 0.0;
        for (int i = 0; i < bills.size(); i++) {
            cumulative += lotteryWeight(bills.get(i));
            if (draw <= cumulative) {
                return i;
            }
        }
        return bills.size() - 1;
    }

    private static double lotteryWeight(Bill bill) {
        double lowLobbyPressure = 1.0 - Math.max(0.0, bill.lobbyPressure());
        double moderatePosition = 1.0 - Math.abs(bill.ideologyPosition());
        return Math.max(
                0.05,
                0.20
                        + (0.95 * bill.publicSupport())
                        + (1.15 * bill.publicBenefit())
                        + (0.35 * lowLobbyPressure)
                        + (0.25 * moderatePosition)
                        + (0.25 * bill.affectedGroupSupport())
                        - (0.45 * bill.concentratedHarm())
        );
    }
}
