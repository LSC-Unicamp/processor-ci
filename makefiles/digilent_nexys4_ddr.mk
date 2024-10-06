ifndef VIVADO_PATH
	VIVADO=/eda/vivado/Vivado/2023.2/bin/vivado
else
	VIVADO=$(VIVADO_PATH)/vivado
endif


all: digilent_nexys4_ddr.bit

digilent_nexys4_ddr.bit:
	@echo "Building the Design..."
	$(VIVADO) -mode batch -nolog -nojournal -source $(BUILD_SCRIPT) $(MACROS)

clean:
	@echo "Cleaning the build folder..."
	rm -rf build

load:
	@echo "Flashing the FPGA..."
	/eda/oss-cad-suite/bin/openFPGALoader -b nexys_a7_100 digilent_nexys4_ddr.bit

run_all: digilent_nexys4_ddr.bit load