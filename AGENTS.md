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
- When sibling simulator projects need legislative outputs, use the repository name or a portable sibling-relative path such as `../Congress Institutional Simulator`.

## Public Repository and Secret Handling

- Treat this repository and every committed file as public information.
- Never commit `.env`, `.env.*`, credentials, access tokens, private keys, signing material, restricted-source caches, or environment-specific private paths. Track only scrubbed templates such as `.env.example`, with blank or unmistakably fake values.
- Before staging or publishing, inspect `git status --short`, review the staged diff, and run a redacted secret scan when available. Confirm that ignored local credential files remain ignored.
- If a real secret ever enters tracked content or Git history, stop publication, remove it from the affected history, and rotate or revoke the credential before pushing or changing visibility.

## Commit, Tag, and Release Policy

- Commit coherent, validated increments frequently: normally after each focused change passes its relevant checks and before switching to a different concern. Preserve unrelated user work and do not fold it into an unclear commit.
- Push validated commits as the normal completion step so the public repository stays current.
- Create tags less frequently, only for meaningful version, citation, submission, or compatibility milestones. An ordinary commit does not need a tag.
- Publish a release only at a milestone with aligned version metadata, release notes, verified artifacts and checksums where applicable, and passing release checks. Use a draft or prerelease for genuinely provisional milestones, a source-only release when that is the intended artifact, and a stable release only when the documented stable benchmark is met.
