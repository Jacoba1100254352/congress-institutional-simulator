package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

import java.util.HashMap;
import java.util.Map;

public final class LobbyAuditProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess innerProcess;
    private final Map<String, Double> trustByProposer = new HashMap<>();
    private final double baseAuditRate;
    private final double captureAuditWeight;
    private final double failureThreshold;
    private final double sanctionSeverity;
    private final boolean reverseFailedAudits;

    public LobbyAuditProcess(
            String name,
            LegislativeProcess innerProcess,
            double baseAuditRate,
            double captureAuditWeight,
            double failureThreshold,
            double sanctionSeverity,
            boolean reverseFailedAudits
    ) {
        Values.requireRange("baseAuditRate", baseAuditRate, 0.0, 1.0);
        Values.requireRange("captureAuditWeight", captureAuditWeight, 0.0, 1.0);
        Values.requireRange("failureThreshold", failureThreshold, 0.0, 1.0);
        Values.requireRange("sanctionSeverity", sanctionSeverity, 0.0, 1.0);
        this.name = name;
        this.innerProcess = innerProcess;
        this.baseAuditRate = baseAuditRate;
        this.captureAuditWeight = captureAuditWeight;
        this.failureThreshold = failureThreshold;
        this.sanctionSeverity = sanctionSeverity;
        this.reverseFailedAudits = reverseFailedAudits;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double proposerTrust = trustByProposer.getOrDefault(bill.proposerId(), 1.0);
        if (proposerTrust < 0.22 && captureRisk > failureThreshold) {
            return BillOutcome.accessDenied(
                    bill,
                    context.currentPolicyPosition(),
                    "anti-capture audit sanctions blocked sponsor"
            );
        }

        BillOutcome outcome = innerProcess.consider(bill, context);
        if (!outcome.enacted() || bill.antiLobbyingReform()) {
            rewardIfPublicInterestBill(bill, outcome);
            return outcome;
        }

        double auditProbability = Values.clamp(
                baseAuditRate + (captureAuditWeight * captureRisk) + (0.12 * bill.privateGain()),
                0.0,
                1.0
        );
        if (context.random().nextDouble() >= auditProbability) {
            rewardIfPublicInterestBill(bill, outcome);
            return outcome;
        }

        double failureScore = auditFailureScore(bill, captureRisk);
        if (failureScore < failureThreshold) {
            rewardIfPublicInterestBill(bill, outcome);
            return outcome;
        }

        double updatedTrust = Values.clamp(
                proposerTrust - (sanctionSeverity * (0.40 + failureScore)),
                0.0,
                1.0
        );
        trustByProposer.put(bill.proposerId(), updatedTrust);

        if (!reverseFailedAudits) {
            return outcome;
        }
        return new BillOutcome(
                outcome.bill(),
                outcome.statusQuoBefore(),
                outcome.statusQuoBefore(),
                false,
                outcome.agendaDisposition(),
                outcome.gateResults(),
                outcome.chamberResults(),
                outcome.presidentialAction(),
                outcome.challenged(),
                "anti-capture audit reversed captured enactment; " + outcome.finalReason()
        );
    }

    private void rewardIfPublicInterestBill(Bill bill, BillOutcome outcome) {
        if (!outcome.enacted()) {
            return;
        }
        double publicInterest = LobbyCaptureScoring.publicInterestScore(bill);
        if (publicInterest < 0.68) {
            return;
        }
        double currentTrust = trustByProposer.getOrDefault(bill.proposerId(), 1.0);
        trustByProposer.put(bill.proposerId(), Values.clamp(currentTrust + 0.05, 0.0, 1.0));
    }

    private static double auditFailureScore(Bill bill, double captureRisk) {
        return Values.clamp(
                (0.54 * captureRisk)
                        + (0.26 * bill.privateGain())
                        + (0.20 * (1.0 - LobbyCaptureScoring.publicInterestScore(bill))),
                0.0,
                1.0
        );
    }
}
