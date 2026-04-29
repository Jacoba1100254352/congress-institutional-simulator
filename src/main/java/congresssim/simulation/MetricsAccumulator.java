package congresssim.simulation;

import congresssim.institution.BillOutcome;
import congresssim.institution.AgendaDisposition;

final class MetricsAccumulator {
    private int totalBills;
    private int enactedBills;
    private int controversialEnactedBills;
    private int popularBills;
    private int failedPopularBills;
    private int floorConsideredBills;
    private int accessDeniedBills;
    private int committeeRejectedBills;
    private int vetoes;
    private int overriddenVetoes;
    private double enactedSupportSum;
    private double compromiseSum;
    private double policyShiftSum;
    private double proposerGainSum;

    void add(BillOutcome outcome) {
        totalBills++;
        policyShiftSum += Math.abs(outcome.statusQuoAfter() - outcome.statusQuoBefore());
        if (outcome.agendaDisposition() == AgendaDisposition.FLOOR_CONSIDERED) {
            floorConsideredBills++;
        } else if (outcome.agendaDisposition() == AgendaDisposition.ACCESS_DENIED) {
            accessDeniedBills++;
        } else if (outcome.agendaDisposition() == AgendaDisposition.COMMITTEE_REJECTED) {
            committeeRejectedBills++;
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

        if (!outcome.enacted()) {
            return;
        }

        enactedBills++;
        double support = outcome.averageYayShare();
        enactedSupportSum += support;
        if (support < 0.50) {
            controversialEnactedBills++;
        }

        double moderation = 1.0 - Math.abs(outcome.bill().ideologyPosition());
        double proposerConcession = proposerConcession(outcome);
        compromiseSum += moderation * support * proposerConcession;
        proposerGainSum += proposerGain(outcome);
    }

    ScenarioReport toReport(String scenarioName) {
        double productivity = ratio(enactedBills, totalBills);
        double avgSupport = enactedBills == 0 ? 0.0 : enactedSupportSum / enactedBills;
        double compromise = enactedBills == 0 ? 0.0 : compromiseSum / enactedBills;
        double controversial = ratio(controversialEnactedBills, enactedBills);
        return new ScenarioReport(
                scenarioName,
                totalBills,
                enactedBills,
                productivity,
                avgSupport,
                productivity * avgSupport,
                compromise,
                1.0 - productivity,
                controversial,
                ratio(failedPopularBills, popularBills),
                totalBills == 0 ? 0.0 : policyShiftSum / totalBills,
                enactedBills == 0 ? 0.0 : proposerGainSum / enactedBills,
                ratio(floorConsideredBills, totalBills),
                ratio(accessDeniedBills, totalBills),
                ratio(committeeRejectedBills, totalBills),
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
