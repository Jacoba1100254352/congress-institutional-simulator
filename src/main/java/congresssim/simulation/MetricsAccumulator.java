package congresssim.simulation;

import congresssim.institution.BillOutcome;
import congresssim.institution.AgendaDisposition;
import congresssim.institution.AffectedGroupScoring;
import congresssim.institution.LobbyCaptureScoring;
import congresssim.institution.OutcomeSignals;

final class MetricsAccumulator {
    private int totalBills;
    private int enactedBills;
    private int controversialEnactedBills;
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
    private double directLobbySpendSum;
    private double agendaLobbySpendSum;
    private double informationLobbySpendSum;
    private double publicCampaignSpendSum;
    private double litigationThreatSpendSum;
    private double attentionSpendSum;

    void add(BillOutcome outcome) {
        totalBills++;
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
        if (outcome.bill().concentratedHarm() >= 0.45) {
            enactedConcentratedHarmBills++;
        }
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
        double defensiveLobbyingShare = totalLobbySpendSum == 0.0 ? 0.0 : defensiveLobbySpendSum / totalLobbySpendSum;
        double captureReturnOnSpend = totalLobbySpendSum == 0.0 ? 0.0 : lobbyCaptureSum / totalLobbySpendSum;
        double publicPreferenceDistortion = enactedBills == 0 ? 0.0 : publicPreferenceDistortionSum / enactedBills;
        double averageAmendmentMovement = totalBills == 0 ? 0.0 : amendmentMovementSum / totalBills;
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
                ratio(amendedBills, totalBills),
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
