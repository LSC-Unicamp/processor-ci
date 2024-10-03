all: ./impl/pnr/project.fs

./impl/pnr/project.fs:
	gw_sh $(BUILD_SCRIPT)

clean:
	rm -rf build

flash:
	/eda/oss-cad-suite/bin/openFPGALoader -b tangnano20k ./impl/pnr/project.fs

run_all: ./impl/pnr/project.fs flash