ifndef VIVADO_PATH
	VIVADO=/eda/vivado/Vivado/2023.2/bin/vivado
else
	VIVADO=$(VIVADO_PATH)/vivado
endif


all: out.bit

out.bit:
	@echo "Building the Design..."
	$(VIVADO) -mode batch -nolog -nojournal -source $(BUILD_SCRIPT)

clean:
	@echo "Cleaning the build folder..."
	rm -rf build

flash:
	@echo "Flashing the FPGA..."
	/eda/oss-cad-suite/bin/openFPGALoader -b nexys_a7_100 out.bit

run_all: out.bit flash