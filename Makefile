MAIN_SOURCES := $(shell find src/main/java -name '*.java')
TEST_SOURCES := $(shell find src/test/java -name '*.java')
JAVA_RELEASE ?= 21
JAVA_PROPS ?= -Dcongresssim.javaRelease=$(JAVA_RELEASE)

.PHONY: build run calibrate calibration-check campaign campaign-v0 campaign-v1 campaign-v2 campaign-v3 campaign-v4 campaign-v5 campaign-v6 campaign-v7 campaign-v8 campaign-v9 campaign-v10 campaign-v11 campaign-v12 campaign-v13 campaign-v14 campaign-v15 campaign-v16 campaign-v17 campaign-v18 campaign-v19 campaign-v20 campaign-v21-paper seed-robustness paper paper-word-count paper-checks paper-anonymity-check figure-label-check supplement-anonymous clean-regeneration-check paper-clean test ci clean

build:
	mkdir -p out/main
	javac --release $(JAVA_RELEASE) -d out/main $(MAIN_SOURCES)

run: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main $(ARGS)

calibrate: build
	java $(JAVA_PROPS) -cp out/main congresssim.Main --calibrate --runs 120 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

calibration-check: calibrate
	python3 scripts/check_calibration.py reports/calibration-baseline.csv

campaign: campaign-v21-paper

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

seed-robustness: build
	JAVA_PROPS="$(JAVA_PROPS)" python3 scripts/run_seed_robustness.py

paper: campaign-v21-paper
	python3 paper/scripts/generate_figures.py
	cd paper && TEXINPUTS=.: BIBINPUTS=.: BSTINPUTS=.: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
	cd paper && TEXINPUTS=.: BIBINPUTS=.: BSTINPUTS=.: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build appendix-odd-d.tex
	cp paper/build/main.pdf paper/main.pdf
	cp paper/build/appendix-odd-d.pdf paper/appendix-odd-d.pdf

paper-word-count: paper
	python3 paper/scripts/check_word_count.py paper/main.pdf --max 6000

paper-checks: paper
	python3 paper/scripts/check_word_count.py paper/main.pdf --max 6000
	python3 scripts/check_paper_anonymity.py paper/main.pdf paper/appendix-odd-d.pdf
	python3 scripts/check_figure_labels.py

paper-anonymity-check: paper
	python3 scripts/check_paper_anonymity.py paper/main.pdf paper/appendix-odd-d.pdf

figure-label-check: paper
	python3 scripts/check_figure_labels.py

supplement-anonymous: paper
	python3 scripts/build_anonymous_supplement.py

clean-regeneration-check:
	git diff --no-ext-diff --exit-code -- .

paper-clean:
	cd paper && latexmk -C -outdir=build main.tex
	cd paper && latexmk -C -outdir=build appendix-odd-d.tex
	rm -rf paper/build

test: build
	mkdir -p out/test
	javac --release $(JAVA_RELEASE) -cp out/main -d out/test $(TEST_SOURCES)
	java $(JAVA_PROPS) -cp out/main:out/test congresssim.SimulatorTests

ci: test calibration-check paper-checks supplement-anonymous clean-regeneration-check

clean:
	rm -rf out
