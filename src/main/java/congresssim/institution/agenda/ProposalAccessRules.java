package congresssim.institution.agenda;

import congresssim.model.Legislator;

import java.util.List;

public final class ProposalAccessRules {
    private ProposalAccessRules() {
    }

    public static ProposalAccessRule open() {
        return new OpenProposalAccessRule();
    }

    public static ProposalAccessRule viabilityScreen(double minimumPublicSupport, double maximumPolicyShift) {
        return new ViabilityProposalAccessRule(minimumPublicSupport, maximumPolicyShift);
    }

    public static ProposalAccessRule proposalCost(double baseCost, double publicCreditWeight, double lobbyCreditWeight) {
        return new ProposalCostAccessRule(baseCost, publicCreditWeight, lobbyCreditWeight);
    }

    public static ProposalAccessRule lobbySurchargeCost(
            double baseCost,
            double publicCreditWeight,
            double lobbySurchargeWeight
    ) {
        return new LobbySurchargeProposalAccessRule(baseCost, publicCreditWeight, lobbySurchargeWeight);
    }

    public static ProposalAccessRule memberQuota(int quotaPerProposer) {
        return new MemberQuotaAccessRule(quotaPerProposer);
    }

    public static ProposalAccessRule publicInterestScreen(
            double minimumPublicInterest,
            double maximumCaptureRisk,
            double maximumPrivateGainRatio,
            double antiLobbyingBenefitFloor
    ) {
        return new PublicInterestScreenAccessRule(
                minimumPublicInterest,
                maximumCaptureRisk,
                maximumPrivateGainRatio,
                antiLobbyingBenefitFloor
        );
    }

    public static ProposalAccessRule currentSystemAgenda(double threshold) {
        return new CurrentSystemAgendaAccessRule(threshold);
    }

    public static ProposalAccessRule leadershipAgenda(
            List<Legislator> legislators,
            double threshold,
            double majorityFitWeight,
            double publicSignalWeight,
            double salienceWeight,
            double capturePenaltyWeight,
            double minorityHarmPenaltyWeight
    ) {
        return new LeadershipAgendaAccessRule(
                legislators,
                threshold,
                majorityFitWeight,
                publicSignalWeight,
                salienceWeight,
                capturePenaltyWeight,
                minorityHarmPenaltyWeight
        );
    }

    public static ProposalAccessRule crossBlocCosponsorship(
            List<Legislator> legislators,
            int minimumCosponsors,
            int minimumOutsideBlocs,
            double minimumIdeologicalDistance,
            double cosponsorThreshold
    ) {
        return new CrossBlocCosponsorshipAccessRule(
                legislators,
                minimumCosponsors,
                minimumOutsideBlocs,
                minimumIdeologicalDistance,
                cosponsorThreshold
        );
    }
}
