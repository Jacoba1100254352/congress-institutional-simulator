package congresssim.simulation;

import congresssim.model.Legislator;

import java.util.List;

public record CommitteeSelectionResult(
        List<Legislator> members,
        Legislator chair,
        double legislatorVotingWeight,
        double citizenAdvisoryWeight,
        double quorumPartyBalance,
        boolean topicReferralAuthority
) {
    public CommitteeSelectionResult {
        if (members.isEmpty()) {
            throw new IllegalArgumentException("members must not be empty.");
        }
        members = List.copyOf(members);
        if (chair == null) {
            chair = members.getFirst();
        }
        legislatorVotingWeight = Math.clamp(legislatorVotingWeight, 0.0, 1.0);
        citizenAdvisoryWeight = Math.clamp(citizenAdvisoryWeight, 0.0, 1.0);
        quorumPartyBalance = Math.clamp(quorumPartyBalance, 0.0, 1.0);
    }
}
