package congresssim.simulation;

import congresssim.institution.BillOutcome;
import congresssim.institution.AgendaDisposition;
import congresssim.institution.LobbyCaptureScoring;

final class MetricsAccumulator {
    private int totalBills;
    private int enactedBills;
    private int controversialEnactedBills;
    private int popularBills;
    private int failedPopularBills;
    private int antiLobbyingBills;
    private int enactedAntiLobbyingBills;
    private int floorConsideredBills;
    private int accessDeniedBills;
    private int committeeRejectedBills;
    private int challengedBills;
    private int vetoes;
    private int overriddenVetoes;
    private double enactedSupportSum;
    private double enactedPublicBenefitSum;
    private double compromiseSum;
    private double policyShiftSum;
    private double proposerGainSum;
    private double lobbyCaptureSum;
    private double publicAlignmentSum;
    private double privateGainRatioSum;
    private double totalLobbySpendSum;
    private double defensiveLobbySpendSum;
    private double publicPreferenceDistortionSum;

    void add(BillOutcome outcome) {
        totalBills++;
        totalLobbySpendSum += outcome.bill().lobbySpend();
        defensiveLobbySpendSum += outcome.bill().defensiveLobbySpend();
        policyShiftSum += Math.abs(outcome.statusQuoAfter() - outcome.statusQuoBefore());
        if (outcome.agendaDisposition() == AgendaDisposition.FLOOR_CONSIDERED) {
            floorConsideredBills++;
        } else if (outcome.agendaDisposition() == AgendaDisposition.ACCESS_DENIED) {
            accessDeniedBills++;
        } else if (outcome.agendaDisposition() == AgendaDisposition.COMMITTEE_REJECTED) {
            committeeRejectedBills++;
        }
        if (outcome.challenged()) {
            challengedBills++;
        }

        if (outcome.bill().publicSupport() >= 0.60) {
            popularBills++;
            if (!outcome.enacted()) {
                failedPopularBills++;
            }
        }
        if (outcome.presidentialAction().vetoed()) {
            vetoes++;
            if (outcome.presidentialAction().overridden()) {
                overriddenVetoes++;
            }
        }
        if (outcome.bill().antiLobbyingReform()) {
            antiLobbyingBills++;
            if (outcome.enacted()) {
                enactedAntiLobbyingBills++;
            }
        }

        if (!outcome.enacted()) {
            return;
        }

        enactedBills++;
        double support = outcome.averageYayShare();
        enactedSupportSum += support;
        enactedPublicBenefitSum += outcome.bill().publicBenefit();
        if (support < 0.50) {
            controversialEnactedBills++;
        }

        double moderation = 1.0 - Math.abs(outcome.bill().ideologyPosition());
        double proposerConcession = proposerConcession(outcome);
        compromiseSum += moderation * support * proposerConcession;
        proposerGainSum += proposerGain(outcome);
        lobbyCaptureSum += LobbyCaptureScoring.captureRisk(outcome.bill());
        publicAlignmentSum += LobbyCaptureScoring.publicAlignment(support, outcome.bill());
        privateGainRatioSum += LobbyCaptureScoring.privateGainRatio(outcome.bill());
        publicPreferenceDistortionSum += Math.abs(support - outcome.bill().publicSupport());
    }

    ScenarioReport toReport(String scenarioName) {
        double productivity = ratio(enactedBills, totalBills);
        double avgSupport = enactedBills == 0 ? 0.0 : enactedSupportSum / enactedBills;
        double avgPublicBenefit = enactedBills == 0 ? 0.0 : enactedPublicBenefitSum / enactedBills;
        double compromise = enactedBills == 0 ? 0.0 : compromiseSum / enactedBills;
        double controversial = ratio(controversialEnactedBills, enactedBills);
        double lobbyCapture = enactedBills == 0 ? 0.0 : lobbyCaptureSum / enactedBills;
        double publicAlignment = enactedBills == 0 ? 0.0 : publicAlignmentSum / enactedBills;
        double privateGainRatio = enactedBills == 0 ? 0.0 : privateGainRatioSum / enactedBills;
        double lobbySpendPerBill = totalBills == 0 ? 0.0 : totalLobbySpendSum / totalBills;
        double defensiveLobbyingShare = totalLobbySpendSum == 0.0 ? 0.0 : defensiveLobbySpendSum / totalLobbySpendSum;
        double captureReturnOnSpend = totalLobbySpendSum == 0.0 ? 0.0 : lobbyCaptureSum / totalLobbySpendSum;
        double publicPreferenceDistortion = enactedBills == 0 ? 0.0 : publicPreferenceDistortionSum / enactedBills;
        return new ScenarioReport(
                scenarioName,
                totalBills,
                enactedBills,
                productivity,
                avgSupport,
                avgPublicBenefit,
                productivity * avgSupport,
                compromise,
                1.0 - productivity,
                controversial,
                ratio(failedPopularBills, popularBills),
                totalBills == 0 ? 0.0 : policyShiftSum / totalBills,
                enactedBills == 0 ? 0.0 : proposerGainSum / enactedBills,
                lobbyCapture,
                publicAlignment,
                ratio(enactedAntiLobbyingBills, antiLobbyingBills),
                privateGainRatio,
                lobbySpendPerBill,
                defensiveLobbyingShare,
                captureReturnOnSpend,
                publicPreferenceDistortion,
                ratio(floorConsideredBills, totalBills),
                ratio(accessDeniedBills, totalBills),
                ratio(committeeRejectedBills, totalBills),
                ratio(challengedBills, totalBills),
                vetoes,
                overriddenVetoes
        );
    }

    private static double ratio(int numerator, int denominator) {
        return denominator == 0 ? 0.0 : (double) numerator / denominator;
    }

    private static double proposerConcession(BillOutcome outcome) {
        double before = Math.abs(outcome.statusQuoBefore() - outcome.bill().proposerIdeology());
        double after = Math.abs(outcome.statusQuoAfter() - outcome.bill().proposerIdeology());
        if (before < 0.000001) {
            return 1.0;
        }
        return Math.max(0.0, Math.min(1.0, after / before));
    }

    private static double proposerGain(BillOutcome outcome) {
        double before = Math.abs(outcome.statusQuoBefore() - outcome.bill().proposerIdeology());
        double after = Math.abs(outcome.statusQuoAfter() - outcome.bill().proposerIdeology());
        return Math.max(0.0, before - after);
    }
}
