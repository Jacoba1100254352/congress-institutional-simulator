package congresssim.institution;

import congresssim.model.Bill;

import java.util.ArrayList;
import java.util.List;

public record BillOutcome(
        Bill bill,
        double statusQuoBefore,
        double statusQuoAfter,
        boolean enacted,
        AgendaDisposition agendaDisposition,
        List<ChamberVoteResult> gateResults,
        List<ChamberVoteResult> chamberResults,
        PresidentialAction presidentialAction,
        boolean challenged,
        String finalReason
) {
    public BillOutcome {
        gateResults = List.copyOf(gateResults);
        chamberResults = List.copyOf(chamberResults);
    }

    public BillOutcome(
            Bill bill,
            double statusQuoBefore,
            double statusQuoAfter,
            boolean enacted,
            List<ChamberVoteResult> chamberResults,
            PresidentialAction presidentialAction,
            String finalReason
    ) {
        this(
                bill,
                statusQuoBefore,
                statusQuoAfter,
                enacted,
                AgendaDisposition.FLOOR_CONSIDERED,
                List.of(),
                chamberResults,
                presidentialAction,
                false,
                finalReason
        );
    }

    public static BillOutcome accessDenied(Bill bill, double statusQuo, String reason) {
        return new BillOutcome(
                bill,
                statusQuo,
                statusQuo,
                false,
                AgendaDisposition.ACCESS_DENIED,
                List.of(),
                List.of(),
                PresidentialAction.none(),
                false,
                reason
        );
    }

    public static BillOutcome committeeRejected(
            Bill bill,
            double statusQuo,
            ChamberVoteResult committeeResult,
            String reason
    ) {
        return new BillOutcome(
                bill,
                statusQuo,
                statusQuo,
                false,
                AgendaDisposition.COMMITTEE_REJECTED,
                List.of(committeeResult),
                List.of(),
                PresidentialAction.none(),
                false,
                reason
        );
    }

    public BillOutcome withGateResult(ChamberVoteResult gateResult) {
        List<ChamberVoteResult> updatedGateResults = new ArrayList<>(gateResults);
        updatedGateResults.add(gateResult);
        return new BillOutcome(
                bill,
                statusQuoBefore,
                statusQuoAfter,
                enacted,
                agendaDisposition,
                updatedGateResults,
                chamberResults,
                presidentialAction,
                challenged,
                finalReason
        );
    }

    public BillOutcome withChallenge(String reason) {
        return new BillOutcome(
                bill,
                statusQuoBefore,
                statusQuoAfter,
                enacted,
                agendaDisposition,
                gateResults,
                chamberResults,
                presidentialAction,
                true,
                reason
        );
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
