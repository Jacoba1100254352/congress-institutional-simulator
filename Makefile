MAIN_SOURCES := $(shell find src/main/java -name '*.java')
TEST_SOURCES := $(shell find src/test/java -name '*.java')
JAVA_RELEASE ?= 21
JAVA_PROPS ?= -Dcongresssim.javaRelease=$(JAVA_RELEASE)

.PHONY: check-java build run calibrate calibration-check campaign paper-campaign main-campaign campaign-v0 campaign-v1 campaign-v2 campaign-v3 campaign-v4 campaign-v5 campaign-v6 campaign-v7 campaign-v8 campaign-v9 campaign-v10 campaign-v11 campaign-v12 campaign-v13 campaign-v14 campaign-v15 campaign-v16 campaign-v17 campaign-v18 campaign-v19 campaign-v20 campaign-v21-paper chamber-structure chamber-structure-summary seed-robustness seed-robustness-check family-screen family-champions catalog-breadth findings-validation validation-readiness fetch-validation-samples empirical-validation empirical-bridge ablation-analysis manipulation-stress mechanism-diagnostics public-provenance paper paper-word-count paper-checks paper-anonymity-check figure-label-check pdf-render-check table-figure-consistency-check supplement-anonymous clean-regeneration-check paper-clean test ci clean

check-java:
	@actual="$$(javac -version 2>&1 | awk '{print $$2}' | cut -d. -f1)"; \
	if [ "$$actual" != "$(JAVA_RELEASE)" ]; then \
		echo "Expected javac $(JAVA_RELEASE), found $$actual. Set Java $(JAVA_RELEASE) on PATH before running this Makefile."; \
		echo "macOS: export JAVA_HOME=\$$(/usr/libexec/java_home -v $(JAVA_RELEASE)); export PATH=\$$JAVA_HOME/bin:\$$PATH"; \
		exit 1; \
	fi

build: check-java
	rm -rf out/main
	mkdir -p out/main
	javac --release $(JAVA_RELEASE) -d out/main $(MAIN_SOURCES)

run: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main $(ARGS)

calibrate: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --calibrate --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

calibration-check: calibrate
	python3 scripts/checks/check_calibration.py reports/calibration-baseline.csv

campaign: paper-campaign

paper-campaign: campaign-v21-paper

main-campaign: paper-campaign

campaign-v21-paper: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v21-paper --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v20: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v20 --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v19: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v19 --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v18: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v18 --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v17: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v17 --runs 80 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v16: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v16 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v15: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v15 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v14: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v14 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v13: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v13 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v12: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v12 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v11: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v11 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v10: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v10 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v9: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v9 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v8: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v8 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v7: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v7 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v6: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v6 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v5: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v5 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v4: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v4 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v3: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v3 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v2: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v2 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v1: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v1 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v0: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign v0 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

chamber-structure: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign chamber-structure --runs 80 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)
	python3 scripts/reporting/summarize_chamber_structure.py

chamber-structure-summary:
	python3 scripts/reporting/summarize_chamber_structure.py

seed-robustness: build
	JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/reporting/run_seed_robustness.py

seed-robustness-check: seed-robustness
	python3 scripts/checks/check_seed_robustness.py

family-champions: build
	JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/reporting/run_family_champions.py

family-screen: family-champions

catalog-breadth: build
	python3 scripts/reporting/report_catalog_breadth.py

findings-validation: paper-campaign
	python3 scripts/validation/write_findings_validation.py

validation-readiness:
	python3 scripts/validation/validate_empirical_inputs.py

fetch-validation-samples:
	python3 scripts/validation/fetch_public_api_samples.py $(ARGS)

empirical-validation:
	python3 scripts/validation/run_empirical_validation.py

empirical-bridge: empirical-validation
	python3 scripts/validation/run_empirical_bridge.py

ablation-analysis: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign ablation-analysis --runs 64 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)
	python3 scripts/reporting/summarize_ablation_analysis.py

manipulation-stress: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --campaign manipulation-stress --runs 64 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)
	python3 scripts/reporting/summarize_manipulation_stress.py

mechanism-diagnostics: empirical-bridge ablation-analysis manipulation-stress
	python3 scripts/reporting/write_paper_diagnostics.py

public-provenance:
	python3 scripts/reporting/write_public_provenance.py

paper: paper-campaign mechanism-diagnostics
	python3 paper/scripts/generate_figures.py
	cd paper && TEXINPUTS=.: BIBINPUTS=.: BSTINPUTS=.: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
	cd paper && TEXINPUTS=.: BIBINPUTS=.: BSTINPUTS=.: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build appendix-odd-d.tex
	cp paper/build/main.pdf paper/main.pdf
	cp paper/build/appendix-odd-d.pdf paper/appendix-odd-d.pdf

paper-word-count: paper
	python3 paper/scripts/check_word_count.py paper/main.pdf --max 6000

paper-checks: paper
	python3 paper/scripts/check_word_count.py paper/main.pdf --max 6000
	python3 scripts/checks/check_paper_anonymity.py paper/main.pdf paper/appendix-odd-d.pdf
	python3 scripts/checks/check_figure_labels.py
	python3 scripts/checks/check_table_figure_consistency.py
	python3 scripts/checks/check_pdf_render.py paper/main.pdf paper/appendix-odd-d.pdf

paper-anonymity-check: paper
	python3 scripts/checks/check_paper_anonymity.py paper/main.pdf paper/appendix-odd-d.pdf

figure-label-check: paper
	python3 scripts/checks/check_figure_labels.py

pdf-render-check: paper
	python3 scripts/checks/check_pdf_render.py paper/main.pdf paper/appendix-odd-d.pdf

table-figure-consistency-check: paper
	python3 scripts/checks/check_table_figure_consistency.py

supplement-anonymous: paper
	python3 scripts/packaging/build_anonymous_supplement.py

clean-regeneration-check:
	# PDF bytes vary across TeX/font environments; paper-checks validates rendered PDFs.
	git diff --no-ext-diff --exit-code -- . ':(exclude)paper/main.pdf' ':(exclude)paper/appendix-odd-d.pdf'

paper-clean:
	cd paper && latexmk -C -outdir=build main.tex
	cd paper && latexmk -C -outdir=build appendix-odd-d.tex
	rm -rf paper/build

test: build
	mkdir -p out/test
	javac --release $(JAVA_RELEASE) -cp out/main -d out/test $(TEST_SOURCES)
	java $(JAVA_PROPS) -cp out/main:out/test congresssim.SimulatorTests

ci: test calibration-check seed-robustness-check validation-readiness empirical-validation catalog-breadth paper-checks supplement-anonymous clean-regeneration-check

clean:
	rm -rf out
