package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public final class CompetingAlternativesProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final AlternativeSelectionRule selectionRule;
    private final int generatedAlternatives;
    private final boolean includeStatusQuo;
    private final int strategicCloneCount;
    private final int strategicDecoyCount;

    public CompetingAlternativesProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            AlternativeSelectionRule selectionRule,
            int generatedAlternatives,
            boolean includeStatusQuo
    ) {
        this(name, innerProcess, legislators, selectionRule, generatedAlternatives, includeStatusQuo, 0, 0);
    }

    public CompetingAlternativesProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            AlternativeSelectionRule selectionRule,
            int generatedAlternatives,
            boolean includeStatusQuo,
            int strategicCloneCount,
            int strategicDecoyCount
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        if (generatedAlternatives < 1) {
            throw new IllegalArgumentException("generatedAlternatives must be positive.");
        }
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.selectionRule = selectionRule;
        this.generatedAlternatives = generatedAlternatives;
        this.includeStatusQuo = includeStatusQuo;
        this.strategicCloneCount = strategicCloneCount;
        this.strategicDecoyCount = strategicDecoyCount;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        List<Bill> alternatives = alternativesFor(bill, context);
        Bill selected = select(alternatives, context);
        boolean statusQuoWon = selected == null;
        double median = chamberMedian();
        double selectedDistance = statusQuoWon ? 0.0 : Math.abs(selected.ideologyPosition() - median);
        double proposerAdvantage = statusQuoWon
                ? 0.0
                : Math.max(0.0, Math.abs(context.currentPolicyPosition() - bill.proposerIdeology())
                - Math.abs(selected.ideologyPosition() - bill.proposerIdeology()));
        OutcomeSignals signals = OutcomeSignals.alternatives(
                alternatives.size() + (includeStatusQuo ? 1 : 0),
                statusQuoWon,
                selectedDistance,
                proposerAdvantage
        ).plus(OutcomeSignals.strategicAlternatives(strategicCloneCount + strategicDecoyCount));
        if (statusQuoWon) {
            return BillOutcome.accessDenied(
                    bill,
                    context.currentPolicyPosition(),
                    "status quo won alternative tournament"
            ).withSignals(signals);
        }
        return innerProcess.consider(selected, context).withSignals(signals);
    }

    private List<Bill> alternativesFor(Bill bill, VoteContext context) {
        List<Bill> alternatives = new ArrayList<>();
        alternatives.add(bill);
        double median = chamberMedian();
        double statusQuo = context.currentPolicyPosition();
        addAlternative(alternatives, bill, "median", median, 0.10, 0.12);
        if (generatedAlternatives >= 2) {
            double compromise = (0.45 * median) + (0.35 * statusQuo) + (0.20 * bill.proposerIdeology());
            addAlternative(alternatives, bill, "compromise", compromise, 0.08, 0.10);
        }
        if (generatedAlternatives >= 3) {
            double opposition = Values.clamp((2.0 * median) - bill.ideologyPosition(), -1.0, 1.0);
            addAlternative(alternatives, bill, "substitute", opposition, 0.02, 0.08);
        }
        if (generatedAlternatives >= 4) {
            double lowHarm = Values.clamp((0.55 * bill.ideologyPosition()) + (0.45 * statusQuo), -1.0, 1.0);
            addAlternative(alternatives, bill, "low-harm", lowHarm, 0.04, 0.16);
        }
        for (int i = 0; i < strategicCloneCount; i++) {
            double clonePosition = Values.clamp(
                    bill.ideologyPosition() + ((i + 1) * 0.025 * Math.signum(bill.ideologyPosition() - statusQuo)),
                    -1.0,
                    1.0
            );
            addAlternative(alternatives, bill, "clone-" + i, clonePosition, -0.02, -0.04);
        }
        for (int i = 0; i < strategicDecoyCount; i++) {
            double decoyDirection = Math.signum(bill.ideologyPosition() - median);
            if (Math.abs(decoyDirection) < 0.000001) {
                decoyDirection = 1.0;
            }
            double decoyPosition = Values.clamp(median - (decoyDirection * (0.42 + (i * 0.10))), -1.0, 1.0);
            addAlternative(alternatives, bill, "decoy-" + i, decoyPosition, -0.08, -0.10);
        }
        return alternatives;
    }

    private static void addAlternative(
            List<Bill> alternatives,
            Bill bill,
            String label,
            double position,
            double benefitAdjustment,
            double supportAdjustment
    ) {
        double movement = Math.abs(position - bill.ideologyPosition());
        double revisedBenefit = Values.clamp(
                bill.publicBenefit() + benefitAdjustment - (movement * 0.05),
                0.0,
                1.0
        );
        double revisedSupport = Values.clamp(
                bill.publicSupport() + supportAdjustment + (movement * 0.10),
                0.0,
                1.0
        );
        double revisedHarm = Values.clamp(bill.concentratedHarm() * (1.0 - Math.min(0.55, movement)), 0.0, 1.0);
        double revisedAffectedSupport = Values.clamp(
                bill.affectedGroupSupport() + ((bill.concentratedHarm() - revisedHarm) * 0.62),
                0.0,
                1.0
        );
        alternatives.add(bill.withAmendment(position, revisedSupport, revisedBenefit)
                .withAffectedGroup(bill.affectedGroup(), revisedAffectedSupport, revisedHarm, bill.compensationCost()));
    }

    private Bill select(List<Bill> alternatives, VoteContext context) {
        return switch (selectionRule) {
            case HIGHEST_PUBLIC_BENEFIT -> chooseBy(alternatives, Comparator.comparingDouble(Bill::publicBenefit));
            case HIGHEST_PUBLIC_SUPPORT -> chooseBy(alternatives, Comparator.comparingDouble(Bill::publicSupport));
            case CLOSEST_TO_CHAMBER_MEDIAN -> chooseClosestToMedian(alternatives);
            case PAIRWISE_MAJORITY -> choosePairwise(alternatives, context);
        };
    }

    private Bill chooseBy(List<Bill> alternatives, Comparator<Bill> comparator) {
        Bill best = alternatives.stream().max(comparator).orElseThrow();
        if (includeStatusQuo && statusQuoBeats(best)) {
            return null;
        }
        return best;
    }

    private Bill chooseClosestToMedian(List<Bill> alternatives) {
        double median = chamberMedian();
        Bill best = alternatives.stream()
                .min(Comparator.comparingDouble(bill -> Math.abs(bill.ideologyPosition() - median)))
                .orElseThrow();
        if (includeStatusQuo && statusQuoBeats(best)) {
            return null;
        }
        return best;
    }

    private Bill choosePairwise(List<Bill> alternatives, VoteContext context) {
        Bill best = null;
        int bestWins = -1;
        for (Bill candidate : alternatives) {
            int wins = 0;
            for (Bill opponent : alternatives) {
                if (candidate == opponent || pairwiseWins(candidate, opponent, context)) {
                    wins++;
                }
            }
            if (includeStatusQuo && pairwiseStatusQuoBeats(candidate, context)) {
                wins--;
            }
            if (wins > bestWins) {
                best = candidate;
                bestWins = wins;
            }
        }
        if (best == null || (includeStatusQuo && pairwiseStatusQuoBeats(best, context) && bestWins < alternatives.size())) {
            return null;
        }
        return best;
    }

    private boolean pairwiseWins(Bill candidate, Bill opponent, VoteContext context) {
        int candidateSupport = 0;
        int opponentSupport = 0;
        for (Legislator legislator : legislators) {
            double candidateUtility = utility(legislator.ideology(), candidate.ideologyPosition(), context.currentPolicyPosition(), candidate);
            double opponentUtility = utility(legislator.ideology(), opponent.ideologyPosition(), context.currentPolicyPosition(), opponent);
            if (candidateUtility >= opponentUtility) {
                candidateSupport++;
            } else {
                opponentSupport++;
            }
        }
        return candidateSupport > opponentSupport;
    }

    private boolean pairwiseStatusQuoBeats(Bill candidate, VoteContext context) {
        int statusQuoSupport = 0;
        int candidateSupport = 0;
        for (Legislator legislator : legislators) {
            double candidateUtility = utility(legislator.ideology(), candidate.ideologyPosition(), context.currentPolicyPosition(), candidate);
            double statusQuoUtility = -(context.currentPolicyPosition() - legislator.ideology())
                    * (context.currentPolicyPosition() - legislator.ideology());
            if (statusQuoUtility > candidateUtility) {
                statusQuoSupport++;
            } else {
                candidateSupport++;
            }
        }
        return statusQuoSupport > candidateSupport;
    }

    private static double utility(double idealPoint, double position, double statusQuo, Bill bill) {
        double spatial = -((position - idealPoint) * (position - idealPoint));
        double statusPenalty = 0.12 * Math.abs(position - statusQuo);
        double publicSignal = 0.16 * (bill.publicSupport() - 0.5);
        double harmPenalty = 0.18 * AffectedGroupScoring.minorityHarm(bill);
        return spatial - statusPenalty + publicSignal - harmPenalty;
    }

    private static boolean statusQuoBeats(Bill bill) {
        return bill.publicSupport() < 0.35 && bill.publicBenefit() < 0.45 && AffectedGroupScoring.minorityHarm(bill) > 0.16;
    }

    private double chamberMedian() {
        List<Double> positions = legislators.stream().map(Legislator::ideology).sorted().toList();
        int midpoint = positions.size() / 2;
        if (positions.size() % 2 == 1) {
            return positions.get(midpoint);
        }
        return (positions.get(midpoint - 1) + positions.get(midpoint)) / 2.0;
    }
}
