all: impl/pnr/project.fs

impl/pnr/project.fs:
	/eda/gowin/IDE/bin/gw_sh $(BUILD_SCRIPT)

clean:
	rm -rf build

load:
	/eda/oss-cad-suite/bin/openFPGALoader -b tangnano20k impl/pnr/project.fs

run_all: ./impl/pnr/project.fs load