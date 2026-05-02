package congresssim.simulation;

import congresssim.institution.core.LegislativeProcess;

import congresssim.model.SimulationWorld;

public interface Scenario {
    String name();

    LegislativeProcess buildProcess(SimulationWorld world);
}

