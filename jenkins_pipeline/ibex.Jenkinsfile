
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf ibex'
                sh 'git clone --recursive --depth=1 https://github.com/lowRISC/ibex ibex'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("ibex") {
                    sh "/eda/oss-cad-suite/bin/iverilog -o simulation.out -g2012                  -s ibex_core  rtl/ibex_alu.sv rtl/ibex_branch_predict.sv rtl/ibex_compressed_decoder.sv rtl/ibex_controller.sv rtl/ibex_core.sv rtl/ibex_counter.sv rtl/ibex_cs_registers.sv rtl/ibex_csr.sv rtl/ibex_decoder.sv rtl/ibex_dummy_instr.sv rtl/ibex_ex_block.sv rtl/ibex_fetch_fifo.sv rtl/ibex_icache.sv rtl/ibex_id_stage.sv rtl/ibex_if_stage.sv rtl/ibex_load_store_unit.sv rtl/ibex_lockstep.sv rtl/ibex_multdiv_fast.sv rtl/ibex_multdiv_slow.sv rtl/ibex_pkg.sv rtl/ibex_pmp.sv rtl/ibex_prefetch_buffer.sv rtl/ibex_register_file_ff.sv rtl/ibex_register_file_fpga.sv rtl/ibex_register_file_latch.sv rtl/ibex_top.sv rtl/ibex_top_tracing.sv rtl/ibex_tracer.sv rtl/ibex_tracer_pkg.sv rtl/ibex_wb_stage.sv "
                }
            }
        }
        
        stage('FPGA Build Pipeline') {
            parallel {
                
                stage('colorlight_i9') {
                    options {
                        lock(resource: 'colorlight_i9')
                    }
                    stages {
                        stage('Synthesis and PnR') {
                            steps {
                                dir("ibex") {
                                    echo 'Starting synthesis for FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p ibex -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("ibex") {
                                    echo 'Flashing FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p ibex -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Test colorlight_i9') {
                            steps {
                                echo 'Testing FPGA colorlight_i9.'
                                dir("ibex") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT="/dev/ttyACM0" \
                                    python /eda/processor-ci-communication/run_tests.py'
                                }
                            }
                        }
                    }
                }
                
                stage('digilent_nexys4_ddr') {
                    options {
                        lock(resource: 'digilent_nexys4_ddr')
                    }
                    stages {
                        stage('Synthesis and PnR') {
                            steps {
                                dir("ibex") {
                                    echo 'Starting synthesis for FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p ibex -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("ibex") {
                                    echo 'Flashing FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p ibex -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Test digilent_nexys4_ddr') {
                            steps {
                                echo 'Testing FPGA digilent_nexys4_ddr.'
                                dir("ibex") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT="/dev/ttyUSB1" \
                                    python /eda/processor-ci-communication/run_tests.py'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            junit '**/test-reports/*.xml'
        }
    }
}
