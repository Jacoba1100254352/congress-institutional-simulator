MAIN_SOURCES := $(shell find src/main/java -name '*.java')
TEST_SOURCES := $(shell find src/test/java -name '*.java')
JAVA_RELEASE ?= 21

.PHONY: build run campaign campaign-v0 campaign-v1 campaign-v2 campaign-v3 campaign-v4 campaign-v5 campaign-v6 campaign-v7 campaign-v8 campaign-v9 campaign-v10 campaign-v11 paper paper-clean test clean

build:
	mkdir -p out/main
	javac --release $(JAVA_RELEASE) -d out/main $(MAIN_SOURCES)

run: build
	java -cp out/main congresssim.Main $(ARGS)

campaign: build
	java -cp out/main congresssim.Main --campaign v11 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v11: campaign

campaign-v10: build
	java -cp out/main congresssim.Main --campaign v10 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v9: build
	java -cp out/main congresssim.Main --campaign v9 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v8: build
	java -cp out/main congresssim.Main --campaign v8 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v7: build
	java -cp out/main congresssim.Main --campaign v7 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v6: build
	java -cp out/main congresssim.Main --campaign v6 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v5: build
	java -cp out/main congresssim.Main --campaign v5 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v4: build
	java -cp out/main congresssim.Main --campaign v4 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v3: build
	java -cp out/main congresssim.Main --campaign v3 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v2: build
	java -cp out/main congresssim.Main --campaign v2 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v1: build
	java -cp out/main congresssim.Main --campaign v1 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v0: build
	java -cp out/main congresssim.Main --campaign v0 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

paper:
	python3 paper/scripts/generate_figures.py
	cd paper && TEXINPUTS=.: BIBINPUTS=.: BSTINPUTS=.: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
	cp paper/build/main.pdf paper/main.pdf

paper-clean:
	cd paper && latexmk -C -outdir=build main.tex
	rm -rf paper/build

test: build
	mkdir -p out/test
	javac --release $(JAVA_RELEASE) -cp out/main -d out/test $(TEST_SOURCES)
	java -cp out/main:out/test congresssim.SimulatorTests

clean:
	rm -rf out
