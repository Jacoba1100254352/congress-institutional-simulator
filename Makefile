MAIN_SOURCES := $(shell find src/main/java -name '*.java')
TEST_SOURCES := $(shell find src/test/java -name '*.java')

.PHONY: build run campaign test clean

build:
	mkdir -p out/main
	javac --release 17 -d out/main $(MAIN_SOURCES)

run: build
	java -cp out/main congresssim.Main $(ARGS)

campaign: build
	java -cp out/main congresssim.Main --campaign v1 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

campaign-v0: build
	java -cp out/main congresssim.Main --campaign v0 --runs 150 --legislators 101 --bills 60 --seed 20260428 --output-dir reports $(ARGS)

test: build
	mkdir -p out/test
	javac --release 17 -cp out/main -d out/test $(TEST_SOURCES)
	java -cp out/main:out/test congresssim.SimulatorTests

clean:
	rm -rf out
