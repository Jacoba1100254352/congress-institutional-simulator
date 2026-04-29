package congresssim.institution;

import congresssim.behavior.VoteContext;
import congresssim.model.Bill;
import congresssim.util.Values;

public final class CitizenPanelReviewProcess implements LegislativeProcess {
    private final String name;
    private final LegislativeProcess certifiedProcess;
    private final LegislativeProcess uncertifiedProcess;
    private final CitizenPanelMode mode;
    private final int panelSize;
    private final double samplingNoise;
    private final double informationQuality;
    private final double manipulationRisk;
    private final double certificationThreshold;

    public CitizenPanelReviewProcess(
            String name,
            LegislativeProcess certifiedProcess,
            LegislativeProcess uncertifiedProcess,
            CitizenPanelMode mode,
            int panelSize,
            double samplingNoise,
            double informationQuality,
            double manipulationRisk,
            double certificationThreshold
    ) {
        if (panelSize <= 0) {
            throw new IllegalArgumentException("panelSize must be positive.");
        }
        Values.requireRange("samplingNoise", samplingNoise, 0.0, 1.0);
        Values.requireRange("informationQuality", informationQuality, 0.0, 1.0);
        Values.requireRange("manipulationRisk", manipulationRisk, 0.0, 1.0);
        Values.requireRange("certificationThreshold", certificationThreshold, 0.0, 1.0);
        this.name = name;
        this.certifiedProcess = certifiedProcess;
        this.uncertifiedProcess = uncertifiedProcess;
        this.mode = mode;
        this.panelSize = panelSize;
        this.samplingNoise = samplingNoise;
        this.informationQuality = informationQuality;
        this.manipulationRisk = manipulationRisk;
        this.certificationThreshold = certificationThreshold;
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BillOutcome consider(Bill bill, VoteContext context) {
        PanelResult result = review(bill, context);
        Bill reviewedBill = bill.withCitizenPanel(
                result.revisedPublicSupport(),
                result.revisedPublicBenefit(),
                result.legitimacy(),
                result.certified()
        );
        LegislativeProcess next = processFor(result);
        if (mode == CitizenPanelMode.AGENDA_PRIORITY) {
            double salienceBoost = result.certified() ? 0.08 : -0.06;
            reviewedBill = reviewedBill.withPublicSignal(
                    reviewedBill.publicSupport(),
                    Values.clamp(reviewedBill.salience() + salienceBoost, 0.0, 1.0)
            );
        }

        return next.consider(reviewedBill, context)
                .withSignals(OutcomeSignals.citizenReview(result.certified(), result.legitimacy()));
    }

    private LegislativeProcess processFor(PanelResult result) {
        if (mode == CitizenPanelMode.AGENDA_PRIORITY) {
            return certifiedProcess;
        }
        return result.certified() ? certifiedProcess : uncertifiedProcess;
    }

    private PanelResult review(Bill bill, VoteContext context) {
        double noiseScale = samplingNoise / Math.sqrt(Math.max(1.0, panelSize / 25.0));
        double noise = context.random().nextGaussian() * noiseScale;
        double manipulation = manipulationRisk
                * ((Math.max(0.0, bill.lobbyPressure()) * 0.16)
                + (bill.publicCampaignSpend() * 0.04)
                + (bill.informationLobbySpend() * 0.05));
        double harmPenalty = AffectedGroupScoring.minorityHarm(bill);
        double informedSupport = Values.clamp(
                ((1.0 - informationQuality) * bill.publicSupport())
                        + (informationQuality * bill.publicBenefit())
                        + manipulation
                        - (0.22 * harmPenalty)
                        + noise,
                0.0,
                1.0
        );
        double perceivedBenefit = Values.clamp(
                ((1.0 - informationQuality) * bill.publicBenefit())
                        + (informationQuality * ((0.65 * bill.publicBenefit()) + (0.35 * informedSupport)))
                        - (manipulationRisk * Math.max(0.0, bill.privateGain() - bill.publicBenefit()) * 0.08),
                0.0,
                1.0
        );
        double legitimacy = Values.clamp(
                (0.34 * informedSupport)
                        + (0.28 * perceivedBenefit)
                        + (0.20 * bill.affectedGroupSupport())
                        + (0.18 * (1.0 - harmPenalty))
                        - (manipulation * 0.12),
                0.0,
                1.0
        );
        boolean certified = legitimacy >= certificationThreshold;
        double adjustment = certified ? 0.70 : 0.45;
        double revisedSupport = Values.clamp(
                bill.publicSupport() + ((informedSupport - bill.publicSupport()) * adjustment),
                0.0,
                1.0
        );
        double revisedBenefit = Values.clamp(
                bill.publicBenefit() + ((perceivedBenefit - bill.publicBenefit()) * adjustment),
                0.0,
                1.0
        );
        return new PanelResult(revisedSupport, revisedBenefit, legitimacy, certified);
    }

    private record PanelResult(
            double revisedPublicSupport,
            double revisedPublicBenefit,
            double legitimacy,
            boolean certified
    ) {
    }
}
