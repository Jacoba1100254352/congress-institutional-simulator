MAIN_SOURCES := $(shell find src/main/java -name '*.java')
TEST_SOURCES := $(shell find src/test/java -name '*.java')

.PHONY: build run campaign campaign-v0 campaign-v1 campaign-v2 paper paper-clean test clean

build:
	mkdir -p out/main
	javac --release 17 -d out/main $(MAIN_SOURCES)

run: build
	java -cp out/main congresssim.Main $(ARGS)

campaign: build
	java -cp out/main congresssim.Main --campaign v2 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v2: campaign

campaign-v1: build
	java -cp out/main congresssim.Main --campaign v1 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v0: build
	java -cp out/main congresssim.Main --campaign v0 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

paper:
	cd paper && TEXINPUTS=.: BIBINPUTS=.: BSTINPUTS=.: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex

paper-clean:
	cd paper && latexmk -C -outdir=build main.tex
	rm -rf paper/build

test: build
	mkdir -p out/test
	javac --release 17 -cp out/main -d out/test $(TEST_SOURCES)
	java -cp out/main:out/test congresssim.SimulatorTests

clean:
	rm -rf out
