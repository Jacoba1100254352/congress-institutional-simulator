# Codex Guidance

This is the Congress Institutional Simulator, a Java 21 comparative institutional-design simulator and paper workspace.

Use these commands from this directory:

- `make run` for the default simulator run.
- `make test` for Java tests.
- `make campaign` for the canonical batch/report workflow.
- `make paper-checks` before treating paper-facing output as ready.

Modeling guidance:

- Keep the simulator centered on status-quo-relative voting, agenda mechanics, institutional rules, and comparative report metrics.
- Preserve the Makefile-first workflow unless the user explicitly asks for a build-system migration.
- Put generated campaign outputs under `reports/` or `out/` as the existing project conventions require.
- When other simulator projects need legislative outputs, reference this project by its current path: `/Users/jacobanderson/Documents/simulators/Congress Institutional Simulator`.
