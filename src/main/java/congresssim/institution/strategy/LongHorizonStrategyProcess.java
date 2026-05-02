package congresssim.institution.strategy;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;
import congresssim.institution.lobbying.LobbyCaptureScoring;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class LongHorizonStrategyProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final List<Legislator> legislators;
    private final int sessionLength;
    private final double learningRate;
    private final double exploitationPenalty;
    private final Map<String, ActorMemory> memoryByProposer = new HashMap<>();
    private int billCounter;

    public LongHorizonStrategyProcess(
            String name,
            LegislativeProcess innerProcess,
            List<Legislator> legislators,
            int sessionLength,
            double learningRate,
            double exploitationPenalty
    ) {
        if (legislators.isEmpty()) {
            throw new IllegalArgumentException("legislators must not be empty.");
        }
        if (sessionLength < 1) {
            throw new IllegalArgumentException("sessionLength must be positive.");
        }
        Values.requireRange("learningRate", learningRate, 0.0, 1.0);
        Values.requireRange("exploitationPenalty", exploitationPenalty, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.legislators = List.copyOf(legislators);
        this.sessionLength = sessionLength;
        this.learningRate = learningRate;
        this.exploitationPenalty = exploitationPenalty;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        if (billCounter > 0 && billCounter % sessionLength == 0) {
            for (ActorMemory memory : memoryByProposer.values()) {
                memory.endSession();
            }
        }
        billCounter++;
        ActorMemory memory = memoryByProposer.computeIfAbsent(bill.proposerId(), ignored -> new ActorMemory());
        double risk = proposalRisk(bill, context);
        double riskySubmission = risk >= memory.riskTolerance ? 1.0 : 0.0;
        if (memory.shouldDelay(risk, bill)) {
            memory.delays++;
            memory.observe(false, bill, risk, learningRate, exploitationPenalty);
            return BillOutcome.accessDenied(bill, context.currentPolicyPosition(), "long-horizon strategic timing delay")
                    .withSignals(OutcomeSignals.diagnostics(Map.of(
                            "strategyLearningPressure", memory.pressure(),
                            "strategicTimingDelayRate", 1.0,
                            "riskySubmissionRate", riskySubmission,
                            "ruleLearningGain", memory.learningGain()
                    )));
        }

        Bill revised = reviseBill(bill, context, memory, risk);
        BillOutcome outcome = innerProcess.consider(revised, context);
        double beforeTrust = memory.trust;
        memory.observe(outcome.enacted(), revised, risk, learningRate, exploitationPenalty);
        return outcome.withSignals(OutcomeSignals.diagnostics(Map.of(
                "strategyLearningPressure", memory.pressure(),
                "strategicTimingDelayRate", 0.0,
                "riskySubmissionRate", riskySubmission,
                "ruleLearningGain", Math.abs(memory.trust - beforeTrust),
                "strategyModerationRate", Math.abs(revised.ideologyPosition() - bill.ideologyPosition()) / 2.0,
                "adaptiveCoalitionSeekingRate", revised.outsideBlocCosponsorCount() > bill.outsideBlocCosponsorCount() ? 1.0 : 0.0
        )));
    }

    private Bill reviseBill(Bill bill, VoteContext context, ActorMemory memory, double risk) {
        double median = chamberMedian();
        double moderation = Values.clamp(
                learningRate * risk * (1.10 - memory.trust) * (0.35 + memory.concession),
                0.0,
                0.72
        );
        double target = (0.46 * median) + (0.34 * context.currentPolicyPosition()) + (0.20 * bill.proposerIdeology());
        Bill revised = bill.withAmendment(
                Values.clamp(bill.ideologyPosition() + moderation * (target - bill.ideologyPosition()), -1.0, 1.0),
                Values.clamp(bill.publicSupport() + (0.14 * moderation) + (0.05 * memory.coalitionSkill), 0.0, 1.0),
                Values.clamp(bill.publicBenefit() - (0.04 * moderation * Math.max(0.0, bill.privateGain() - bill.publicBenefit())), 0.0, 1.0)
        );
        if (risk >= 0.42) {
            int addedOutsideSponsors = outsideSponsorCount(revised, memory);
            revised = revised.withCosponsorship(
                    revised.cosponsorCount() + addedOutsideSponsors + 1,
                    revised.outsideBlocCosponsorCount() + addedOutsideSponsors,
                    revised.affectedGroupSponsor() || revised.affectedGroupSupport() >= 0.48
            );
        }
        if (LobbyCaptureScoring.captureRisk(revised) > memory.lobbyRiskTolerance) {
            double cut = Values.clamp((LobbyCaptureScoring.captureRisk(revised) - memory.lobbyRiskTolerance) * 0.60, 0.0, 0.55);
            revised = revised.withLobbyActivity(
                    Values.clamp(revised.lobbyPressure() * (1.0 - cut), -1.0, 1.0),
                    Values.clamp(revised.publicSupport() + (0.04 * cut), 0.0, 1.0),
                    Values.clamp(revised.publicBenefit() + (0.03 * cut), 0.0, 1.0),
                    Values.clamp(revised.privateGain() * (1.0 - (0.28 * cut)), 0.0, 1.0),
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0
            );
        }
        if (revised.concentratedHarm() >= 0.42 && memory.concession >= 0.48) {
            double harmCut = Values.clamp(0.20 + (0.30 * memory.concession * risk), 0.0, 0.70);
            revised = revised.withCompensation(
                    Values.clamp(revised.publicBenefit() - (0.08 * revised.compensationCost() * memory.concession), 0.0, 1.0),
                    Values.clamp(revised.affectedGroupSupport() + (0.18 * memory.concession), 0.0, 1.0),
                    Values.clamp(revised.concentratedHarm() * (1.0 - harmCut), 0.0, 1.0)
            );
        }
        return revised;
    }

    private int outsideSponsorCount(Bill bill, ActorMemory memory) {
        int count = 0;
        String proposerParty = partyOf(bill.proposerId());
        for (Legislator legislator : legislators) {
            if (legislator.id().equals(bill.proposerId()) || legislator.party().equals(proposerParty)) {
                continue;
            }
            double fit = 1.0 - Math.abs(legislator.ideology() - bill.ideologyPosition()) / 2.0;
            double score = (0.36 * fit)
                    + (0.26 * bill.publicSupport())
                    + (0.22 * legislator.compromisePreference())
                    + (0.16 * memory.coalitionSkill);
            if (score >= 0.56) {
                count++;
            }
        }
        return Math.min(5, count);
    }

    private String partyOf(String legislatorId) {
        for (Legislator legislator : legislators) {
            if (legislator.id().equals(legislatorId)) {
                return legislator.party();
            }
        }
        return "";
    }

    private double chamberMedian() {
        List<Double> ideologies = legislators.stream().map(Legislator::ideology).sorted().toList();
        int middle = ideologies.size() / 2;
        if (ideologies.size() % 2 == 1) {
            return ideologies.get(middle);
        }
        return (ideologies.get(middle - 1) + ideologies.get(middle)) / 2.0;
    }

    private static double proposalRisk(Bill bill, VoteContext context) {
        return Values.clamp(
                (0.20 * (1.0 - bill.publicSupport()))
                        + (0.19 * Math.abs(bill.ideologyPosition() - context.currentPolicyPosition()) / 2.0)
                        + (0.18 * LobbyCaptureScoring.captureRisk(bill))
                        + (0.17 * bill.concentratedHarm())
                        + (0.14 * bill.publicBenefitUncertainty())
                        + (0.12 * Math.max(0.0, bill.privateGain() - bill.publicBenefit())),
                0.0,
                1.0
        );
    }

    private static final class ActorMemory {
        private double trust = 0.54;
        private double riskTolerance = 0.54;
        private double concession = 0.42;
        private double coalitionSkill = 0.38;
        private double lobbyRiskTolerance = 0.48;
        private double proposalPace = 1.0;
        private int delays;
        private int badStreak;
        private int goodStreak;

        private boolean shouldDelay(double risk, Bill bill) {
            if (bill.publicBenefit() >= 0.72 || bill.publicSupport() >= 0.66 || risk < riskTolerance) {
                return false;
            }
            double deterministicDraw = Math.floorMod((bill.id() + ":" + delays + ":" + badStreak).hashCode(), 100) / 100.0;
            return deterministicDraw > proposalPace;
        }

        private void observe(boolean enacted, Bill bill, double risk, double learningRate, double exploitationPenalty) {
            double quality = (0.34 * bill.publicBenefit())
                    + (0.24 * bill.publicSupport())
                    + (0.18 * (1.0 - LobbyCaptureScoring.captureRisk(bill)))
                    + (0.14 * bill.affectedGroupSupport())
                    + (0.10 * (1.0 - bill.publicBenefitUncertainty()));
            double success = enacted ? 1.0 : 0.0;
            double signal = (0.58 * quality) + (0.42 * success) - 0.50;
            trust = Values.clamp(trust + (learningRate * 0.22 * signal), 0.0, 1.0);
            if (signal < -0.04 || risk > 0.70) {
                badStreak++;
                goodStreak = 0;
                proposalPace = Values.clamp(proposalPace - (learningRate * (0.08 + 0.05 * risk)), 0.18, 1.35);
                riskTolerance = Values.clamp(riskTolerance - (learningRate * 0.040), 0.22, 0.84);
                concession = Values.clamp(concession + (learningRate * 0.075), 0.12, 0.96);
                coalitionSkill = Values.clamp(coalitionSkill + (learningRate * 0.055), 0.10, 0.94);
                lobbyRiskTolerance = Values.clamp(lobbyRiskTolerance - (learningRate * exploitationPenalty * 0.060), 0.16, 0.82);
            } else {
                goodStreak++;
                badStreak = 0;
                proposalPace = Values.clamp(proposalPace + (learningRate * 0.050), 0.18, 1.35);
                riskTolerance = Values.clamp(riskTolerance + (learningRate * 0.025), 0.22, 0.84);
                concession = Values.clamp(concession - (learningRate * 0.025), 0.12, 0.96);
                coalitionSkill = Values.clamp(coalitionSkill + (learningRate * 0.020), 0.10, 0.94);
                lobbyRiskTolerance = Values.clamp(lobbyRiskTolerance + (learningRate * 0.010), 0.16, 0.82);
            }
        }

        private void endSession() {
            trust = Values.clamp((0.94 * trust) + 0.03, 0.0, 1.0);
            proposalPace = Values.clamp((0.92 * proposalPace) + 0.08, 0.18, 1.35);
            badStreak = Math.max(0, badStreak - 1);
            goodStreak = Math.max(0, goodStreak - 1);
        }

        private double pressure() {
            return Values.clamp((0.40 * (1.0 - trust)) + (0.24 * (1.0 - proposalPace / 1.35))
                    + (0.20 * concession) + (0.16 * badStreak / 4.0), 0.0, 1.0);
        }

        private double learningGain() {
            return Values.clamp((0.34 * trust) + (0.26 * coalitionSkill) + (0.22 * concession)
                    + (0.18 * (1.0 - lobbyRiskTolerance)), 0.0, 1.0);
        }
    }
}
