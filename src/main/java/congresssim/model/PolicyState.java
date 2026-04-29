package congresssim.model;

import congresssim.util.Values;

public record PolicyState(double position) {
    public PolicyState {
        Values.requireRange("position", position, -1.0, 1.0);
    }

    public PolicyState moveTo(Bill bill) {
        return new PolicyState(bill.ideologyPosition());
    }
}

