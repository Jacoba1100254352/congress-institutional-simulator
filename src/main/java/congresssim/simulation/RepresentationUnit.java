package congresssim.simulation;

import congresssim.util.Values;

public record RepresentationUnit(
        String id,
        double populationShare,
        double seatShare,
        int districtMagnitude,
        SelectionMode selectionMode
) {
    public RepresentationUnit {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("id must not be blank.");
        }
        Values.requireRange("populationShare", populationShare, 0.0, 1.0);
        Values.requireRange("seatShare", seatShare, 0.0, 1.0);
        if (districtMagnitude <= 0) {
            throw new IllegalArgumentException("districtMagnitude must be positive.");
        }
        if (selectionMode == null) {
            throw new IllegalArgumentException("selectionMode must not be null.");
        }
    }

    public boolean appointed() {
        return selectionMode == SelectionMode.APPOINTED_COMMISSION
                || selectionMode == SelectionMode.APPOINTED_PARTY
                || selectionMode == SelectionMode.VOCATIONAL
                || selectionMode == SelectionMode.MIXED;
    }
}
