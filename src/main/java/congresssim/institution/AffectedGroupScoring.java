package congresssim.institution;

import congresssim.model.Bill;
import congresssim.util.Values;

public final class AffectedGroupScoring {
    private AffectedGroupScoring() {
    }

    public static double minorityHarm(Bill bill) {
        double consentDeficit = 1.0 - bill.affectedGroupSupport();
        double uncompensated = bill.compensationAdded() ? 0.55 : 1.0;
        return Values.clamp(bill.concentratedHarm() * consentDeficit * uncompensated, 0.0, 1.0);
    }

    public static double legitimacy(Bill bill, double chamberSupport) {
        double publicLegitimacy = 0.42 * bill.publicSupport();
        double chamberLegitimacy = 0.28 * chamberSupport;
        double affectedLegitimacy = 0.20 * bill.affectedGroupSupport();
        double harmPenalty = 0.32 * minorityHarm(bill);
        double certificationBonus = bill.citizenCertified() ? 0.08 * bill.citizenPanelLegitimacy() : 0.0;
        return Values.clamp(publicLegitimacy + chamberLegitimacy + affectedLegitimacy + certificationBonus - harmPenalty, 0.0, 1.0);
    }
}
