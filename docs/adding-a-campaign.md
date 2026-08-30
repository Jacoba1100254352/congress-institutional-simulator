# Adding A Campaign

Campaigns are named batches of scenario/case comparisons that write CSV,
Markdown, and manifest outputs under `reports/`.

## 1. Define The Purpose

Before adding a campaign, decide whether it is:

- a paper-facing campaign;
- a diagnostic campaign;
- a validation or calibration campaign;
- a robustness or stress-test campaign;
- an exploratory campaign that should stay outside paper-facing artifacts.

Paper-facing campaigns should have fixed seeds, stable scenario keys, and
documented output paths.

## 2. Select Scenario Keys

Scenario keys come from `ScenarioCatalog`. Reuse existing keys where possible.
If a new key is needed, add it in the appropriate scenario-family class and make
sure `ScenarioCatalog.scenariosForKeys(...)` can resolve it.

## 3. Add A CampaignRunner Method

Add a method to `CampaignRunner` that:

- selects cases and scenario keys;
- uses fixed seeds or receives the seed from `Main`;
- writes a CSV under `reports/`;
- writes a Markdown summary under `reports/`;
- writes a manifest when the campaign is paper-facing or long-running.

Keep case keys and scenario keys stable. Downstream scripts and paper tables
often join on those names.

## 4. Wire The CLI

Add the campaign name to the `Main.runCampaign` switch. Prefer descriptive
aliases only when they improve operator ergonomics, as with `v21-paper`,
`paper`, and `main-comparison`.

## 5. Add A Make Target

Add a Makefile target using the existing pattern:

```make
my-campaign: build
	java $(JAVA_PROPS) -cp $(APP_CP) congresssim.Main --campaign my-campaign --runs 64 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)
```

Use Java 21 and fixed seeds for reproducible campaign outputs.

## 6. Add Reporting Scripts Only When Needed

If the raw campaign CSV is enough, avoid adding a script. Add a Python reporting
script only when the campaign needs derived summaries, tables, or paper-facing
figures.

Generated files should go under:

- `reports/` for CSV, Markdown, and manifests;
- `paper/figures/` for LaTeX tables and figures used by the paper;
- `out/` for local build outputs.

## 7. Verify

For exploratory campaigns, run the new target and inspect the generated report.
For paper-facing campaigns, also run:

```sh
make paper-checks
```

If the campaign changes tracked generated artifacts, inspect the diff with:

```sh
git --no-pager diff --no-ext-diff
```
