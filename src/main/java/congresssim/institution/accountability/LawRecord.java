package congresssim.institution.accountability;

import congresssim.model.Bill;

record LawRecord(
        Bill sourceBill,
        double previousStatusQuo,
        double enactedPosition,
        int enactedRound,
        int reviewDueRound,
        boolean active
) {
    LawRecord deactivate() {
        return new LawRecord(sourceBill, previousStatusQuo, enactedPosition, enactedRound, reviewDueRound, false);
    }
}
