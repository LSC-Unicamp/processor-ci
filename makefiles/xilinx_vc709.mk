ifndef VIVADO_PATH
	VIVADO=/eda/vivado19/Vivado/2019.1/bin/vivado
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

# openFPGALoader funciona apenas na versão nightly, a versão estavel atual não suporta a vc709 ainda
flash:
	@echo "Flashing the FPGA..."
	/eda/oss-cad-suite/bin/openFPGALoader -b vc709 out.bit
#$(VIVADO_PATH)/vivado  -mode batch -nolog -nojournal -source flash.tcl

run_all: out.bit flash