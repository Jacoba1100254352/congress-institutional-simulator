package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.behavior.VotingStrategy;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class BicameralRoutingProcess implements LegislativeProcess {
    private final String name;
    private final Chamber lowerChamber;
    private final Chamber upperChamber;
    private final VotingStrategy votingStrategy;
    private final BicameralOriginRule originRule;
    private final BicameralConflictMode conflictMode;
    private final VotingRule jointSittingRule;
    private final double conflictTrigger;
    private final double revisionTarget;
    private final double revisionRate;
    private final double revisionCost;
    private final double suspensiveOverrideThreshold;
    private final int maxShuttleRounds;

    public BicameralRoutingProcess(
            String name,
            Chamber lowerChamber,
            Chamber upperChamber,
            VotingStrategy votingStrategy,
            BicameralOriginRule originRule,
            BicameralConflictMode conflictMode,
            VotingRule jointSittingRule,
            double conflictTrigger,
            double revisionTarget,
            double revisionRate,
            double revisionCost,
            double suspensiveOverrideThreshold,
            int maxShuttleRounds
    ) {
        Values.requireRange("conflictTrigger", conflictTrigger, 0.0, 1.0);
        Values.requireRange("revisionTarget", revisionTarget, -1.0, 1.0);
        Values.requireRange("revisionRate", revisionRate, 0.0, 1.0);
        Values.requireRange("revisionCost", revisionCost, 0.0, 1.0);
        Values.requireRange("suspensiveOverrideThreshold", suspensiveOverrideThreshold, 0.0, 1.0);
        if (maxShuttleRounds < 1) {
            throw new IllegalArgumentException("maxShuttleRounds must be positive.");
        }
        this.name = name;
        this.lowerChamber = lowerChamber;
        this.upperChamber = upperChamber;
        this.votingStrategy = votingStrategy;
        this.originRule = originRule;
        this.conflictMode = conflictMode;
        this.jointSittingRule = jointSittingRule;
        this.conflictTrigger = conflictTrigger;
        this.revisionTarget = revisionTarget;
        this.revisionRate = revisionRate;
        this.revisionCost = revisionCost;
        this.suspensiveOverrideThreshold = suspensiveOverrideThreshold;
        this.maxShuttleRounds = maxShuttleRounds;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        Chamber firstChamber = firstChamberFor(bill);
        Chamber secondChamber = firstChamber == upperChamber ? lowerChamber : upperChamber;
        List<ChamberVoteResult> results = new ArrayList<>();
        double statusQuoBefore = context.currentPolicyPosition();

        ChamberVoteResult firstResult = firstChamber.voteOn(bill, context);
        results.add(firstResult);
        if (!firstResult.passed()) {
            return outcome(
                    bill,
                    statusQuoBefore,
                    false,
                    results,
                    "failed in originating chamber",
                    routingSignals(bill, firstChamber, secondChamber, false, true, 0.02, 0, false, false, false, 0.0, false)
            );
        }

        ChamberVoteResult secondResult = secondChamber.voteOn(bill, context);
        results.add(secondResult);
        if (secondResult.passed()) {
            return outcome(
                    bill,
                    statusQuoBefore,
                    true,
                    results,
                    "passed routed bicameral process",
                    routingSignals(bill, firstChamber, secondChamber, true, false, 0.04, 0, false, false, false, 0.0, false)
            );
        }

        return switch (conflictMode) {
            case SECOND_CHAMBER_KILL -> outcome(
                    bill,
                    statusQuoBefore,
                    false,
                    results,
                    "second chamber killed bill",
                    routingSignals(bill, firstChamber, secondChamber, false, true, 0.05, 0, false, false, false, 0.0, false)
            );
            case SUSPENSIVE_VETO -> suspensiveVetoOutcome(bill, statusQuoBefore, results, firstResult);
            case REVISION_COUNCIL -> revisionCouncilOutcome(bill, context, statusQuoBefore, results, firstChamber, secondChamber);
            case SECOND_CHAMBER_AMENDMENT -> secondChamberAmendmentOutcome(bill, context, statusQuoBefore, results, firstChamber, secondChamber);
            case LIMITED_NAVETTE -> limitedNavetteOutcome(bill, context, statusQuoBefore, results, firstChamber, secondChamber);
            case JOINT_SITTING -> jointSittingOutcome(bill, context, statusQuoBefore, results);
            case MEDIATION_COMMITTEE -> mediationCommitteeOutcome(bill, context, statusQuoBefore, results, firstChamber, secondChamber);
            case LAST_OFFER_BARGAINING -> lastOfferBargainingOutcome(bill, context, statusQuoBefore, results, firstChamber, secondChamber);
            case LOWER_OVERRIDE_AFTER_DISAGREEMENT -> lowerOverrideOutcome(bill, statusQuoBefore, results, firstChamber, firstResult);
        };
    }

    private Chamber firstChamberFor(Bill bill) {
        return originRule.startsInUpper(bill) ? upperChamber : lowerChamber;
    }

    private BillOutcome suspensiveVetoOutcome(
            Bill bill,
            double statusQuoBefore,
            List<ChamberVoteResult> results,
            ChamberVoteResult firstResult
    ) {
        if (firstResult.yayShare() < suspensiveOverrideThreshold) {
            return outcome(
                    bill,
                    statusQuoBefore,
                    false,
                    results,
                    "suspensive veto not overridden",
                    routingSignals(bill, lowerChamber, upperChamber, false, true, 0.08, 0, false, false, false, 0.0, false)
            );
        }
        results.add(new ChamberVoteResult(
                firstResult.chamberName() + " override",
                "suspensive override " + String.format("%.0f%%", suspensiveOverrideThreshold * 100.0),
                firstResult.yayCount(),
                firstResult.nayCount(),
                true
        ));
        return outcome(
                bill,
                statusQuoBefore,
                true,
                results,
                "suspensive veto overridden",
                routingSignals(bill, lowerChamber, upperChamber, true, false, 0.10, 0, false, true, false, 0.0, false)
        );
    }

    private BillOutcome revisionCouncilOutcome(
            Bill bill,
            VoteContext context,
            double statusQuoBefore,
            List<ChamberVoteResult> results,
            Chamber firstChamber,
            Chamber secondChamber
    ) {
        if (averageSupport(results) < conflictTrigger) {
            return outcome(
                    bill,
                    statusQuoBefore,
                    false,
                    results,
                    "revision threshold not reached",
                    routingSignals(bill, firstChamber, secondChamber, false, true, 0.08, 0, false, false, false, 0.0, false)
            );
        }
        Bill revised = revise(bill, revisionRate);
        ChamberVoteResult firstRevision = firstChamber.voteOn(revised, context);
        ChamberVoteResult secondRevision = secondChamber.voteOn(revised, context);
        results.add(firstRevision);
        results.add(secondRevision);
        boolean enacted = firstRevision.passed() && secondRevision.passed();
        return outcome(
                revised,
                statusQuoBefore,
                enacted,
                results,
                enacted
                        ? "revision council report passed"
                        : "revision council report failed",
                routingSignals(
                        revised,
                        firstChamber,
                        secondChamber,
                        enacted,
                        !enacted,
                        0.14,
                        0,
                        false,
                        false,
                        true,
                        Math.abs(revised.ideologyPosition() - bill.ideologyPosition()) * 0.35,
                        secondChamber == upperChamber
                )
        );
    }

    private BillOutcome secondChamberAmendmentOutcome(
            Bill bill,
            VoteContext context,
            double statusQuoBefore,
            List<ChamberVoteResult> results,
            Chamber firstChamber,
            Chamber secondChamber
    ) {
        Bill amended = revise(bill, revisionRate * 0.80);
        ChamberVoteResult secondAmendment = secondChamber.voteOn(amended, context);
        ChamberVoteResult firstFinal = firstChamber.voteOn(amended, context);
        results.add(secondAmendment);
        results.add(firstFinal);
        boolean enacted = secondAmendment.passed() && firstFinal.passed();
        return outcome(
                amended,
                statusQuoBefore,
                enacted,
                results,
                enacted ? "second-chamber amendment retained" : "second-chamber amendment failed final report",
                routingSignals(
                        amended,
                        firstChamber,
                        secondChamber,
                        enacted,
                        !enacted,
                        0.12,
                        0,
                        false,
                        false,
                        true,
                        Math.abs(amended.ideologyPosition() - bill.ideologyPosition()) * 0.22,
                        secondChamber == upperChamber
                )
        );
    }

    private BillOutcome limitedNavetteOutcome(
            Bill bill,
            VoteContext context,
            double statusQuoBefore,
            List<ChamberVoteResult> results,
            Chamber firstChamber,
            Chamber secondChamber
    ) {
        if (averageSupport(results) < conflictTrigger) {
            return outcome(
                    bill,
                    statusQuoBefore,
                    false,
                    results,
                    "navette threshold not reached",
                    routingSignals(bill, firstChamber, secondChamber, false, true, 0.08, 0, false, false, false, 0.0, false)
            );
        }
        Bill working = bill;
        for (int round = 0; round < maxShuttleRounds; round++) {
            double roundRate = revisionRate / (round + 1.0);
            working = revise(working, roundRate);
            ChamberVoteResult secondRevision = secondChamber.voteOn(working, context);
            ChamberVoteResult firstRevision = firstChamber.voteOn(working, context);
            results.add(secondRevision);
            results.add(firstRevision);
            if (firstRevision.passed() && secondRevision.passed()) {
                int rounds = round + 1;
                return outcome(
                        working,
                        statusQuoBefore,
                        true,
                        results,
                        "limited navette agreement",
                        routingSignals(
                                working,
                                firstChamber,
                                secondChamber,
                                true,
                                false,
                                0.10 + (0.05 * rounds),
                                rounds,
                                true,
                                false,
                                true,
                                Math.abs(working.ideologyPosition() - bill.ideologyPosition()) * 0.25,
                                secondChamber == upperChamber
                        )
                );
            }
        }
        return outcome(
                working,
                statusQuoBefore,
                false,
                results,
                "limited navette exhausted",
                routingSignals(
                        working,
                        firstChamber,
                        secondChamber,
                        false,
                        true,
                        0.10 + (0.05 * maxShuttleRounds),
                        maxShuttleRounds,
                        false,
                        false,
                        true,
                        Math.abs(working.ideologyPosition() - bill.ideologyPosition()) * 0.25,
                        false
                )
        );
    }

    private BillOutcome jointSittingOutcome(
            Bill bill,
            VoteContext context,
            double statusQuoBefore,
            List<ChamberVoteResult> results
    ) {
        if (averageSupport(results) < conflictTrigger) {
            return outcome(
                    bill,
                    statusQuoBefore,
                    false,
                    results,
                    "joint sitting threshold not reached",
                    routingSignals(bill, lowerChamber, upperChamber, false, true, 0.08, 0, false, false, false, 0.0, false)
            );
        }
        Chamber jointChamber = new Chamber(
                "Joint sitting",
                uniqueMembers(lowerChamber.legislators(), upperChamber.legislators()),
                votingStrategy,
                jointSittingRule
        );
        ChamberVoteResult jointResult = jointChamber.voteOn(bill, context);
        results.add(jointResult);
        return outcome(
                bill,
                statusQuoBefore,
                jointResult.passed(),
                results,
                jointResult.passed() ? "joint sitting enacted bill" : "joint sitting rejected bill",
                routingSignals(bill, lowerChamber, upperChamber, jointResult.passed(), !jointResult.passed(), 0.12, 0, false, false, false, 0.0, false)
        );
    }

    private BillOutcome mediationCommitteeOutcome(
            Bill bill,
            VoteContext context,
            double statusQuoBefore,
            List<ChamberVoteResult> results,
            Chamber firstChamber,
            Chamber secondChamber
    ) {
        double mediatorTarget = (revisionTarget + context.currentPolicyPosition()) / 2.0;
        Bill mediated = bill.withAmendment(
                Math.clamp(bill.ideologyPosition() + (revisionRate * (mediatorTarget - bill.ideologyPosition())), -1.0, 1.0),
                Math.clamp(bill.publicSupport() + 0.08 + (0.12 * revisionRate), 0.0, 1.0),
                Math.clamp(bill.publicBenefit() - (revisionCost * 0.05), 0.0, 1.0)
        );
        ChamberVoteResult firstFinal = firstChamber.voteOn(mediated, context);
        ChamberVoteResult secondFinal = secondChamber.voteOn(mediated, context);
        results.add(firstFinal);
        results.add(secondFinal);
        boolean enacted = firstFinal.passed() && secondFinal.passed();
        return outcome(
                mediated,
                statusQuoBefore,
                enacted,
                results,
                enacted ? "mediation committee final report passed" : "mediation committee final report failed",
                routingSignals(
                        mediated,
                        firstChamber,
                        secondChamber,
                        enacted,
                        !enacted,
                        0.16,
                        0,
                        false,
                        false,
                        true,
                        Math.abs(mediated.ideologyPosition() - bill.ideologyPosition()) * 0.45,
                        false
                )
        );
    }

    private BillOutcome lastOfferBargainingOutcome(
            Bill bill,
            VoteContext context,
            double statusQuoBefore,
            List<ChamberVoteResult> results,
            Chamber firstChamber,
            Chamber secondChamber
    ) {
        Bill secondOffer = revise(bill, revisionRate);
        double originalSupport = averageSupport(results);
        ChamberVoteResult secondOfferVote = secondChamber.voteOn(secondOffer, context);
        ChamberVoteResult firstOfferVote = firstChamber.voteOn(secondOffer, context);
        double revisedSupport = (secondOfferVote.yayShare() + firstOfferVote.yayShare()) / 2.0;
        Bill selected = revisedSupport >= originalSupport ? secondOffer : bill;
        ChamberVoteResult finalFirst = firstChamber.voteOn(selected, context);
        ChamberVoteResult finalSecond = secondChamber.voteOn(selected, context);
        results.add(secondOfferVote);
        results.add(firstOfferVote);
        results.add(finalFirst);
        results.add(finalSecond);
        boolean enacted = finalFirst.passed() && finalSecond.passed();
        return outcome(
                selected,
                statusQuoBefore,
                enacted,
                results,
                enacted ? "last-offer bargain selected a final bill" : "last-offer bargain selected status quo",
                routingSignals(
                        selected,
                        firstChamber,
                        secondChamber,
                        enacted,
                        !enacted,
                        0.18,
                        1,
                        enacted,
                        false,
                        selected != bill,
                        selected == bill ? 0.0 : Math.abs(selected.ideologyPosition() - bill.ideologyPosition()) * 0.30,
                        selected != bill && secondChamber == upperChamber
                )
        );
    }

    private BillOutcome lowerOverrideOutcome(
            Bill bill,
            double statusQuoBefore,
            List<ChamberVoteResult> results,
            Chamber firstChamber,
            ChamberVoteResult firstResult
    ) {
        boolean lowerCanOverride = firstChamber == lowerChamber && firstResult.yayShare() >= suspensiveOverrideThreshold;
        if (lowerCanOverride) {
            results.add(new ChamberVoteResult(
                    firstResult.chamberName() + " repeated-disagreement override",
                    "lower override " + String.format("%.0f%%", suspensiveOverrideThreshold * 100.0),
                    firstResult.yayCount(),
                    firstResult.nayCount(),
                    true
            ));
        }
        return outcome(
                bill,
                statusQuoBefore,
                lowerCanOverride,
                results,
                lowerCanOverride ? "lower house overrode repeated disagreement" : "lower override failed",
                routingSignals(bill, firstChamber, upperChamber, lowerCanOverride, !lowerCanOverride, 0.14, 0, false, lowerCanOverride, false, 0.0, false)
        );
    }

    private Bill revise(Bill bill, double rate) {
        double revisedPosition = Math.clamp(
                bill.ideologyPosition() + (rate * (revisionTarget - bill.ideologyPosition())),
                -1.0,
                1.0
        );
        double movement = Math.abs(revisedPosition - bill.ideologyPosition());
        double supportGain = movement * 0.15;
        double benefitCost = revisionCost * (0.04 + (0.08 * bill.publicBenefitUncertainty()));
        return bill.withAmendment(
                revisedPosition,
                Math.clamp(bill.publicSupport() + supportGain, 0.0, 1.0),
                Math.clamp(bill.publicBenefit() - benefitCost, 0.0, 1.0)
        );
    }

    private BillOutcome outcome(
            Bill bill,
            double statusQuoBefore,
            boolean enacted,
            List<ChamberVoteResult> results,
            String reason
    ) {
        return outcome(bill, statusQuoBefore, enacted, results, reason, OutcomeSignals.none());
    }

    private BillOutcome outcome(
            Bill bill,
            double statusQuoBefore,
            boolean enacted,
            List<ChamberVoteResult> results,
            String reason,
            OutcomeSignals signals
    ) {
        return new BillOutcome(
                bill,
                statusQuoBefore,
                enacted ? bill.ideologyPosition() : statusQuoBefore,
                enacted,
                results,
                PresidentialAction.none(),
                reason
        ).withSignals(signals);
    }

    private static double averageSupport(List<ChamberVoteResult> results) {
        double sum = 0.0;
        for (ChamberVoteResult result : results) {
            sum += result.yayShare();
        }
        return results.isEmpty() ? 0.0 : sum / results.size();
    }

    private static List<Legislator> uniqueMembers(List<Legislator> lowerMembers, List<Legislator> upperMembers) {
        Map<String, Legislator> byId = new LinkedHashMap<>();
        for (Legislator legislator : lowerMembers) {
            byId.putIfAbsent(legislator.id(), legislator);
        }
        for (Legislator legislator : upperMembers) {
            byId.putIfAbsent(legislator.id(), legislator);
        }
        return List.copyOf(byId.values());
    }

    private OutcomeSignals routingSignals(
            Bill bill,
            Chamber firstChamber,
            Chamber secondChamber,
            boolean enacted,
            boolean deadlock,
            double routingDelayCost,
            int shuttleRounds,
            boolean shuttleAgreement,
            boolean suspensiveOverride,
            boolean revised,
            double mediatorAddedTextShare,
            boolean upperAmendmentRetained
    ) {
        boolean upperBlock = deadlock && secondChamber == upperChamber && upperChamber.legislators().size() < lowerChamber.legislators().size();
        boolean populationSupportedBlocked = deadlock && bill.publicSupport() >= 0.50;
        return OutcomeSignals.bicameralRouting(
                routingDelayCost,
                shuttleRounds,
                shuttleAgreement,
                suspensiveOverride,
                deadlock
        ).plus(OutcomeSignals.diagnostics(Map.of(
                "smallConstituencyVetoRate", upperBlock ? 1.0 : 0.0,
                "populationSupportedButBlockedRate", populationSupportedBlocked ? 1.0 : 0.0,
                "firstMoverWinRate", enacted ? 1.0 : 0.0,
                "amendmentSurvivalRate", revised && enacted ? 1.0 : 0.0,
                "mediatorAddedTextShare", Math.clamp(mediatorAddedTextShare, 0.0, 1.0),
                "upperHouseAmendmentRetentionRate", upperAmendmentRetained && enacted ? 1.0 : 0.0,
                "suspensiveDelayUseRate", conflictMode == BicameralConflictMode.SUSPENSIVE_VETO ? 1.0 : 0.0
        )));
    }
}
