package congresssim.institution.accountability;

import congresssim.institution.core.BillOutcome;
import congresssim.institution.core.LegislativeProcess;
import congresssim.institution.core.OutcomeSignals;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.model.Legislator;
import congresssim.util.Values;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public final class EligibilityDiagnosticsProcess implements LegislativeProcess {
    private final String name;
    private final List<Legislator> fullLegislature;
    private final List<Legislator> eligibleLegislature;
    private final EligibilityRule rule;
    private final LegislativeProcess innerProcess;

    public EligibilityDiagnosticsProcess(
            String name,
            List<Legislator> fullLegislature,
            List<Legislator> eligibleLegislature,
            EligibilityRule rule,
            LegislativeProcess innerProcess
    ) {
        if (fullLegislature.isEmpty() || eligibleLegislature.isEmpty()) {
            throw new IllegalArgumentException("eligibility diagnostics require nonempty full and eligible legislatures.");
        }
        this.name = name;
        this.fullLegislature = List.copyOf(fullLegislature);
        this.eligibleLegislature = List.copyOf(eligibleLegislature);
        this.rule = rule == null ? EligibilityRule.expertiseMajority() : rule;
        this.innerProcess = innerProcess;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        BillOutcome outcome = innerProcess.consider(bill, context);
        return outcome.withSignals(OutcomeSignals.diagnostics(metricsFor(bill)));
    }

    private Map<String, Double> metricsFor(Bill bill) {
        double exclusionRate = 1.0 - ((double) eligibleLegislature.size() / fullLegislature.size());
        double appointmentShare = average(eligibleLegislature, legislator -> legislator.representationProfile().appointed() ? 1.0 : 0.0);
        double averageLobby = average(eligibleLegislature, Legislator::lobbySensitivity);
        double averageExpertise = average(eligibleLegislature, EligibilityRule::expertiseProxy);
        double fullExpertise = average(fullLegislature, EligibilityRule::expertiseProxy);
        double constituencyAccountability = average(eligibleLegislature, Legislator::constituencySensitivity) * (1.0 - appointmentShare);
        double experienceStock = average(eligibleLegislature, legislator -> {
            int term = legislator.representationProfile().renewalCycleLength();
            double renewalDistance = legislator.representationProfile().nextRenewalRound() / (double) Math.max(1, term);
            return Math.clamp((term / 12.0) * (0.75 + (0.25 * renewalDistance)), 0.0, 1.0);
        });
        double renewalStaggering = renewalStaggeringIndex(eligibleLegislature);
        double nearTermRenewalShare = average(
                eligibleLegislature,
                legislator -> legislator.representationProfile().nextRenewalRound() <= 2 ? 1.0 : 0.0
        );
        double recusalRate = rule.sectorRecusalRule()
                ? average(eligibleLegislature, legislator -> recused(legislator, bill) ? 1.0 : 0.0)
                : 0.0;
        double contestedSeatRate = Values.clamp(
                (1.0 - appointmentShare) * (1.0 - (0.50 * rule.selectorCaptureRisk())) * (1.0 - (0.35 * exclusionRate)),
                0.0,
                1.0
        );
        double vacancyRate = Values.clamp(exclusionRate - 0.34 + (recusalRate * 0.18), 0.0, 1.0);
        return Map.ofEntries(
                Map.entry("appointmentCaptureRisk", Values.clamp(appointmentShare * (0.45 + (0.55 * averageLobby)) + (0.25 * rule.selectorCaptureRisk()), 0.0, 1.0)),
                Map.entry("eligibilityExclusionRate", Values.clamp(exclusionRate, 0.0, 1.0)),
                Map.entry("expertiseRepresentationGap", Values.clamp(Math.max(0.0, averageExpertise - fullExpertise), 0.0, 1.0)),
                Map.entry("constituencyAccountability", Values.clamp(constituencyAccountability, 0.0, 1.0)),
                Map.entry("selectorCaptureIndex", Values.clamp(rule.selectorCaptureRisk() * (0.45 + (0.55 * appointmentShare)), 0.0, 1.0)),
                Map.entry("legislatorExperienceStock", Values.clamp(experienceStock, 0.0, 1.0)),
                Map.entry("electoralResponsiveness", Values.clamp((1.0 - appointmentShare) * average(eligibleLegislature, Legislator::constituencySensitivity), 0.0, 1.0)),
                Map.entry("turnoverOutsideInfluenceShift", Values.clamp(rule.turnoverRate() * averageLobby * (1.0 - experienceStock), 0.0, 1.0)),
                Map.entry("candidatePoolDiversity", Values.clamp(uniqueParties(eligibleLegislature) / (double) Math.max(1, uniqueParties(fullLegislature)), 0.0, 1.0)),
                Map.entry("contestedSeatRate", contestedSeatRate),
                Map.entry("vacancyRate", vacancyRate),
                Map.entry("renewalStaggeringIndex", renewalStaggering),
                Map.entry("nearTermRenewalShare", Values.clamp(nearTermRenewalShare, 0.0, 1.0)),
                Map.entry("recusalRate", Values.clamp(recusalRate, 0.0, 1.0)),
                Map.entry("conflictDisclosureRate", Values.clamp((rule.removalAfterSanctions() ? 0.22 : 0.0) + (rule.postOfficeCoolingOffYears() / 8.0) + (rule.sectorRecusalRule() ? 0.26 : 0.0), 0.0, 1.0)),
                Map.entry("revolvingDoorTransitionRate", Values.clamp((1.0 - Math.clamp(rule.postOfficeCoolingOffYears() / 8.0, 0.0, 1.0)) * averageLobby, 0.0, 1.0)),
                Map.entry("sponsorIndustryAlignment", Values.clamp(sponsorIndustryAlignment(bill), 0.0, 1.0))
        );
    }

    private boolean recused(Legislator legislator, Bill bill) {
        return EligibilityRule.sectorAlignment(legislator, bill.issueDomain()) > 0.74
                && EligibilityRule.conflictProxy(legislator) > rule.conflictOfInterestThreshold();
    }

    private double sponsorIndustryAlignment(Bill bill) {
        return fullLegislature.stream()
                .filter(legislator -> legislator.id().equals(bill.proposerId()))
                .findFirst()
                .map(legislator -> EligibilityRule.sectorAlignment(legislator, bill.issueDomain()) * legislator.lobbySensitivity())
                .orElse(0.0);
    }

    private static int uniqueParties(List<Legislator> legislators) {
        Set<String> parties = new HashSet<>();
        for (Legislator legislator : legislators) {
            parties.add(legislator.party());
        }
        return parties.size();
    }

    private static double renewalStaggeringIndex(List<Legislator> legislators) {
        Set<Integer> cohorts = new HashSet<>();
        int maxCycle = 1;
        for (Legislator legislator : legislators) {
            cohorts.add(legislator.representationProfile().renewalCohort());
            maxCycle = Math.max(maxCycle, legislator.representationProfile().renewalCycleLength());
        }
        return Values.clamp(cohorts.size() / (double) maxCycle, 0.0, 1.0);
    }

    private static double average(List<Legislator> legislators, LegislatorMetric metric) {
        double sum = 0.0;
        for (Legislator legislator : legislators) {
            sum += metric.apply(legislator);
        }
        return sum / legislators.size();
    }

    @FunctionalInterface
    private interface LegislatorMetric {
        double apply(Legislator legislator);
    }
}
