package congresssim.simulation;

import congresssim.institution.BillOutcome;
import congresssim.institution.AgendaDisposition;
import congresssim.institution.AffectedGroupScoring;
import congresssim.institution.LobbyCaptureScoring;
import congresssim.institution.OutcomeSignals;

import java.util.HashMap;
import java.util.Map;

final class MetricsAccumulator {
    private int totalBills;
    private int enactedBills;
    private int controversialEnactedBills;
    private int weakPublicMandateEnactedBills;
    private int popularBills;
    private int failedPopularBills;
    private int antiLobbyingBills;
    private int enactedAntiLobbyingBills;
    private int amendedBills;
    private int concentratedHarmBills;
    private int enactedConcentratedHarmBills;
    private int compensationBills;
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
    private double amendmentMovementSum;
    private double minorityHarmSum;
    private double legitimacySum;
    private double activeLawWelfareSum;
    private double lowSupportActiveLawShareSum;
    private int lawReviews;
    private int lawReversals;
    private int lawCorrections;
    private double correctionDelaySum;
    private double alternativeMedianDistanceSum;
    private double proposerAgendaAdvantageSum;
    private int alternativeRounds;
    private int alternativesConsidered;
    private int statusQuoWins;
    private int citizenReviews;
    private int citizenCertifications;
    private double citizenLegitimacySum;
    private int objectionWindows;
    private int repealWindowReversals;
    private int fastLaneRoutes;
    private int middleLaneRoutes;
    private int highRiskRoutes;
    private int challengeTokenExhaustions;
    private int falseNegativePasses;
    private int publicWillReviews;
    private double publicSignalMovementSum;
    private double districtAlignmentSum;
    private int cosponsorshipReviews;
    private int crossBlocAdmissions;
    private int affectedGroupSponsors;
    private int totalCosponsors;
    private int proposalBondReviews;
    private double proposalBondForfeitureSum;
    private int strategicAlternativeRounds;
    private int strategicDecoys;
    private double directLobbySpendSum;
    private double agendaLobbySpendSum;
    private double informationLobbySpendSum;
    private double publicCampaignSpendSum;
    private double litigationThreatSpendSum;
    private double attentionSpendSum;
    private double submittedPublicBenefitSum;
    private final Map<String, Integer> submittedByProposer = new HashMap<>();
    private final Map<String, Integer> floorByProposer = new HashMap<>();

    void add(BillOutcome outcome) {
        totalBills++;
        submittedPublicBenefitSum += outcome.bill().publicBenefit();
        submittedByProposer.merge(outcome.bill().proposerId(), 1, Integer::sum);
        totalLobbySpendSum += outcome.bill().lobbySpend();
        defensiveLobbySpendSum += outcome.bill().defensiveLobbySpend();
        directLobbySpendSum += outcome.bill().directLobbySpend();
        agendaLobbySpendSum += outcome.bill().agendaLobbySpend();
        informationLobbySpendSum += outcome.bill().informationLobbySpend();
        publicCampaignSpendSum += outcome.bill().publicCampaignSpend();
        litigationThreatSpendSum += outcome.bill().litigationThreatSpend();
        attentionSpendSum += outcome.bill().attentionSpend();
        amendmentMovementSum += outcome.bill().amendmentMovement();
        if (outcome.bill().amendmentMovement() > 0.000001) {
            amendedBills++;
        }
        if (outcome.bill().concentratedHarm() >= 0.45) {
            concentratedHarmBills++;
        }
        if (outcome.bill().compensationAdded()) {
            compensationBills++;
        }
        policyShiftSum += Math.abs(outcome.statusQuoAfter() - outcome.statusQuoBefore());
        OutcomeSignals signals = outcome.signals();
        lawReviews += signals.lawReviews();
        lawReversals += signals.lawReversals();
        lawCorrections += signals.lawCorrections();
        correctionDelaySum += signals.correctionDelay();
        activeLawWelfareSum += signals.activeLawWelfare();
        lowSupportActiveLawShareSum += signals.lowSupportActiveLawShare();
        alternativeRounds += signals.alternativeRounds();
        alternativesConsidered += signals.alternativesConsidered();
        statusQuoWins += signals.statusQuoWins();
        alternativeMedianDistanceSum += signals.selectedAlternativeMedianDistance();
        proposerAgendaAdvantageSum += signals.proposerAgendaAdvantage();
        citizenReviews += signals.citizenReviews();
        citizenCertifications += signals.citizenCertifications();
        citizenLegitimacySum += signals.citizenLegitimacy();
        objectionWindows += signals.objectionWindows();
        repealWindowReversals += signals.repealWindowReversals();
        fastLaneRoutes += signals.fastLaneRoutes();
        middleLaneRoutes += signals.middleLaneRoutes();
        highRiskRoutes += signals.highRiskRoutes();
        challengeTokenExhaustions += signals.challengeTokenExhaustions();
        falseNegativePasses += signals.falseNegativePasses();
        publicWillReviews += signals.publicWillReviews();
        publicSignalMovementSum += signals.publicSignalMovement();
        districtAlignmentSum += signals.districtAlignment();
        cosponsorshipReviews += signals.cosponsorshipReviews();
        crossBlocAdmissions += signals.crossBlocAdmissions();
        affectedGroupSponsors += signals.affectedGroupSponsors();
        totalCosponsors += signals.totalCosponsors();
        proposalBondReviews += signals.proposalBondReviews();
        proposalBondForfeitureSum += signals.proposalBondForfeiture();
        strategicAlternativeRounds += signals.strategicAlternativeRounds();
        strategicDecoys += signals.strategicDecoys();
        if (outcome.agendaDisposition() == AgendaDisposition.FLOOR_CONSIDERED) {
            floorConsideredBills++;
            floorByProposer.merge(outcome.bill().proposerId(), 1, Integer::sum);
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
        if (outcome.bill().concentratedHarm() >= 0.45) {
            enactedConcentratedHarmBills++;
        }
        double support = outcome.averageYayShare();
        enactedSupportSum += support;
        enactedPublicBenefitSum += outcome.bill().publicBenefit();
        if (support < 0.50) {
            controversialEnactedBills++;
        }
        if (outcome.bill().publicSupport() < 0.50) {
            weakPublicMandateEnactedBills++;
        }

        double moderation = 1.0 - Math.abs(outcome.bill().ideologyPosition());
        double proposerConcession = proposerConcession(outcome);
        compromiseSum += moderation * support * proposerConcession;
        proposerGainSum += proposerGain(outcome);
        lobbyCaptureSum += LobbyCaptureScoring.captureRisk(outcome.bill());
        publicAlignmentSum += LobbyCaptureScoring.publicAlignment(support, outcome.bill());
        privateGainRatioSum += LobbyCaptureScoring.privateGainRatio(outcome.bill());
        publicPreferenceDistortionSum += Math.abs(support - outcome.bill().publicSupport());
        minorityHarmSum += AffectedGroupScoring.minorityHarm(outcome.bill());
        legitimacySum += AffectedGroupScoring.legitimacy(outcome.bill(), support);
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
        double attentionSpendPerBill = totalBills == 0 ? 0.0 : attentionSpendSum / totalBills;
        double defensiveLobbyingShare = totalLobbySpendSum == 0.0 ? 0.0 : defensiveLobbySpendSum / totalLobbySpendSum;
        double captureReturnOnSpend = totalLobbySpendSum == 0.0 ? 0.0 : lobbyCaptureSum / totalLobbySpendSum;
        double publicPreferenceDistortion = enactedBills == 0 ? 0.0 : publicPreferenceDistortionSum / enactedBills;
        double averageAmendmentMovement = totalBills == 0 ? 0.0 : amendmentMovementSum / totalBills;
        double amendmentRate = ratio(amendedBills, totalBills);
        double minorityHarm = enactedBills == 0 ? 0.0 : minorityHarmSum / enactedBills;
        double concentratedHarmPassage = ratio(enactedConcentratedHarmBills, concentratedHarmBills);
        double compensationRate = ratio(compensationBills, totalBills);
        double legitimacy = enactedBills == 0 ? 0.0 : legitimacySum / enactedBills;
        double activeLawWelfare = lawReviews == 0 ? 0.0 : activeLawWelfareSum / lawReviews;
        double lowSupportActiveLawShare = lawReviews == 0 ? 0.0 : lowSupportActiveLawShareSum / lawReviews;
        double selectedAlternativeMedianDistance = alternativeRounds == 0 ? 0.0 : alternativeMedianDistanceSum / alternativeRounds;
        double proposerAgendaAdvantage = alternativeRounds == 0 ? 0.0 : proposerAgendaAdvantageSum / alternativeRounds;
        double alternativeDiversity = alternativeRounds == 0 ? 0.0 : (double) alternativesConsidered / alternativeRounds;
        double publicBenefitPerLobbyDollar = totalLobbySpendSum == 0.0 ? 0.0 : enactedPublicBenefitSum / totalLobbySpendSum;
        double proposalBondForfeiture = proposalBondReviews == 0 ? 0.0 : proposalBondForfeitureSum / proposalBondReviews;
        double publicSignalMovement = publicWillReviews == 0 ? 0.0 : publicSignalMovementSum / publicWillReviews;
        double districtAlignment = publicWillReviews == 0 ? 0.0 : districtAlignmentSum / publicWillReviews;
        double administrativeCost = administrativeCostIndex(
                totalBills,
                floorConsideredBills,
                committeeRejectedBills,
                challengedBills,
                lawReviews,
                alternativeRounds,
                citizenReviews,
                objectionWindows,
                amendmentRate,
                attentionSpendPerBill
        );
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
                ratio(weakPublicMandateEnactedBills, enactedBills),
                amendmentRate,
                averageAmendmentMovement,
                minorityHarm,
                concentratedHarmPassage,
                compensationRate,
                legitimacy,
                activeLawWelfare,
                ratio(lawReversals, lawReviews),
                lawCorrections == 0 ? 0.0 : correctionDelaySum / lawCorrections,
                totalBills == 0 ? 0.0 : policyShiftSum / totalBills,
                lowSupportActiveLawShare,
                selectedAlternativeMedianDistance,
                proposerAgendaAdvantage,
                alternativeDiversity,
                ratio(statusQuoWins, alternativeRounds),
                publicBenefitPerLobbyDollar,
                share(directLobbySpendSum, totalLobbySpendSum),
                share(agendaLobbySpendSum, totalLobbySpendSum),
                share(informationLobbySpendSum, totalLobbySpendSum),
                share(publicCampaignSpendSum, totalLobbySpendSum),
                share(litigationThreatSpendSum, totalLobbySpendSum),
                ratio(citizenReviews, totalBills),
                ratio(citizenCertifications, citizenReviews),
                citizenReviews == 0 ? 0.0 : citizenLegitimacySum / citizenReviews,
                totalBills == 0 ? 0.0 : attentionSpendSum / totalBills,
                ratio(objectionWindows, totalBills),
                ratio(repealWindowReversals, objectionWindows),
                ratio(fastLaneRoutes, totalBills),
                ratio(middleLaneRoutes, totalBills),
                ratio(highRiskRoutes, totalBills),
                ratio(challengeTokenExhaustions, totalBills),
                ratio(falseNegativePasses, totalBills),
                ratio(publicWillReviews, totalBills),
                publicSignalMovement,
                districtAlignment,
                ratio(crossBlocAdmissions, cosponsorshipReviews),
                ratio(affectedGroupSponsors, cosponsorshipReviews),
                cosponsorshipReviews == 0 ? 0.0 : (double) totalCosponsors / cosponsorshipReviews,
                proposalBondForfeiture,
                ratio(strategicDecoys, strategicAlternativeRounds),
                gini(floorByProposer),
                totalBills == 0 ? 0.0 : enactedPublicBenefitSum / totalBills,
                administrativeCost,
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

    private static double share(double numerator, double denominator) {
        return denominator == 0.0 ? 0.0 : numerator / denominator;
    }

    private static double administrativeCostIndex(
            int totalBills,
            int floorConsideredBills,
            int committeeRejectedBills,
            int challengedBills,
            int lawReviews,
            int alternativeRounds,
            int citizenReviews,
            int objectionWindows,
            double amendmentRate,
            double attentionSpendPerBill
    ) {
        if (totalBills == 0) {
            return 0.0;
        }
        double floorRate = ratio(floorConsideredBills, totalBills);
        double committeeRate = ratio(committeeRejectedBills, totalBills);
        double challengeRate = ratio(challengedBills, totalBills);
        double lawReviewRate = ratio(lawReviews, totalBills);
        double alternativeRate = ratio(alternativeRounds, totalBills);
        double citizenReviewRate = ratio(citizenReviews, totalBills);
        double objectionRate = ratio(objectionWindows, totalBills);
        double attentionCost = Math.clamp(attentionSpendPerBill / 3.0, 0.0, 1.0);
        return Math.clamp(
                (0.18 * attentionCost)
                        + (0.14 * amendmentRate)
                        + (0.14 * alternativeRate)
                        + (0.12 * citizenReviewRate)
                        + (0.12 * lawReviewRate)
                        + (0.10 * objectionRate)
                        + (0.08 * challengeRate)
                        + (0.07 * floorRate)
                        + (0.05 * committeeRate),
                0.0,
                1.0
        );
    }

    private static double gini(Map<String, Integer> counts) {
        if (counts.isEmpty()) {
            return 0.0;
        }
        int size = counts.size();
        double mean = counts.values().stream().mapToInt(Integer::intValue).average().orElse(0.0);
        if (mean <= 0.000001) {
            return 0.0;
        }
        double differenceSum = 0.0;
        for (int left : counts.values()) {
            for (int right : counts.values()) {
                differenceSum += Math.abs(left - right);
            }
        }
        return differenceSum / (2.0 * size * size * mean);
    }

    private static double proposerConcession(BillOutcome outcome) {
        double before = Math.abs(outcome.statusQuoBefore() - outcome.bill().proposerIdeology());
        double after = Math.abs(outcome.statusQuoAfter() - outcome.bill().proposerIdeology());
        if (before < 0.000001) {
            return 1.0;
        }
        return Math.clamp(after / before, 0.0, 1.0);
    }

    private static double proposerGain(BillOutcome outcome) {
        double before = Math.abs(outcome.statusQuoBefore() - outcome.bill().proposerIdeology());
        double after = Math.abs(outcome.statusQuoAfter() - outcome.bill().proposerIdeology());
        return Math.max(0.0, before - after);
    }
}
