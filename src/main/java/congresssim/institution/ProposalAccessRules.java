package congresssim.institution;

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
}
