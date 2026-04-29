MAIN_SOURCES := $(shell find src/main/java -name '*.java')
TEST_SOURCES := $(shell find src/test/java -name '*.java')

.PHONY: build run test clean

build:
	mkdir -p out/main
	javac --release 17 -d out/main $(MAIN_SOURCES)

run: build
	java -cp out/main congresssim.Main $(ARGS)

test: build
	mkdir -p out/test
	javac --release 17 -cp out/main -d out/test $(TEST_SOURCES)
	java -cp out/main:out/test congresssim.SimulatorTests

clean:
	rm -rf out

