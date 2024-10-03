all: out.bit

out.bit: out.config
	/eda/oss-cad-suite/bin/ecppack --compress --input out.config  --bit out.bit

out.config: out.json
	/eda/oss-cad-suite/bin/nextpnr-ecp5 --json out.json --write out_pnr.json --45k \
		--lpf /eda/processor-ci/constraints/colorlight_i9.lpf --textcfg out.config --package CABGA381 \
		--speed 6 --lpf-allow-unconstrained --report report_timing.json \
		--detailed-timing-report 

out.json:
	/eda/oss-cad-suite/bin/yosys -c $(BUILD_SCRIPT)

clean:
	rm -rf build

flash:
	/eda/oss-cad-suite/bin/openFPGALoader -b colorlight-i9 out.bit

run_all: out.bit flash