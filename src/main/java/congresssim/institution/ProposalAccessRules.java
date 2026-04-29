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
}

