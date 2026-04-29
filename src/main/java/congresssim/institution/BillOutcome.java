package congresssim.institution;

import congresssim.model.Bill;

import java.util.List;

public record BillOutcome(
        Bill bill,
        double statusQuoBefore,
        double statusQuoAfter,
        boolean enacted,
        List<ChamberVoteResult> chamberResults,
        PresidentialAction presidentialAction,
        String finalReason
) {
    public BillOutcome {
        chamberResults = List.copyOf(chamberResults);
    }

    public double averageYayShare() {
        if (chamberResults.isEmpty()) {
            return 0.0;
        }

        double sum = 0.0;
        for (ChamberVoteResult result : chamberResults) {
            sum += result.yayShare();
        }
        return sum / chamberResults.size();
    }
}
