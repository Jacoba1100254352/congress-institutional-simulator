package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class PublicInterestScreenAccessRule implements ProposalAccessRule {
    private final double minimumPublicInterest;
    private final double maximumCaptureRisk;
    private final double maximumPrivateGainRatio;
    private final double antiLobbyingBenefitFloor;

    public PublicInterestScreenAccessRule(
            double minimumPublicInterest,
            double maximumCaptureRisk,
            double maximumPrivateGainRatio,
            double antiLobbyingBenefitFloor
    ) {
        Values.requireRange("minimumPublicInterest", minimumPublicInterest, 0.0, 1.0);
        Values.requireRange("maximumCaptureRisk", maximumCaptureRisk, 0.0, 1.0);
        Values.requireRange("maximumPrivateGainRatio", maximumPrivateGainRatio, 0.0, 5.0);
        Values.requireRange("antiLobbyingBenefitFloor", antiLobbyingBenefitFloor, 0.0, 1.0);
        this.minimumPublicInterest = minimumPublicInterest;
        this.maximumCaptureRisk = maximumCaptureRisk;
        this.maximumPrivateGainRatio = maximumPrivateGainRatio;
        this.antiLobbyingBenefitFloor = antiLobbyingBenefitFloor;
    }

    @Override
    public String name() {
        return "public-interest anti-capture screen";
    }

    @Override
    public AccessDecision evaluate(Bill bill, VoteContext context) {
        if (bill.antiLobbyingReform()) {
            if (bill.publicBenefit() >= antiLobbyingBenefitFloor) {
                return AccessDecision.granted("anti-lobbying reform public-benefit showing");
            }
            return AccessDecision.denied("anti-lobbying reform lacks public-benefit showing");
        }

        double publicInterest = LobbyCaptureScoring.publicInterestScore(bill);
        double captureRisk = LobbyCaptureScoring.captureRisk(bill);
        double privateGainRatio = LobbyCaptureScoring.privateGainRatio(bill);

        if (captureRisk > maximumCaptureRisk && publicInterest < minimumPublicInterest) {
            return AccessDecision.denied("public-interest screen blocked capture-risk proposal");
        }
        if (privateGainRatio > maximumPrivateGainRatio && bill.publicSupport() < 0.55) {
            return AccessDecision.denied("public-interest screen blocked private-gain proposal");
        }
        return AccessDecision.granted("public-interest screen cleared");
    }
}
