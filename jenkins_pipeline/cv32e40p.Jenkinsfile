
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf cv32e40p'
                sh 'git clone --recursive --depth=1 https://github.com/openhwgroup/cv32e40p cv32e40p'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("cv32e40p") {
                    sh "/eda/oss-cad-suite/bin/iverilog -o simulation.out -g2012                  -s  -I rtl/include/ rtl/cv32e40p_aligner.sv rtl/cv32e40p_alu.sv rtl/cv32e40p_alu_div.sv rtl/cv32e40p_apu_disp.sv rtl/cv32e40p_compressed_decoder.sv rtl/cv32e40p_controller.sv rtl/cv32e40p_core.sv rtl/cv32e40p_cs_registers.sv rtl/cv32e40p_decoder.sv rtl/cv32e40p_ex_stage.sv rtl/cv32e40p_ff_one.sv rtl/cv32e40p_fifo.sv rtl/cv32e40p_fp_wrapper.sv rtl/cv32e40p_hwloop_regs.sv rtl/cv32e40p_id_stage.sv rtl/cv32e40p_if_stage.sv rtl/cv32e40p_int_controller.sv rtl/cv32e40p_load_store_unit.sv rtl/cv32e40p_mult.sv rtl/cv32e40p_obi_interface.sv rtl/cv32e40p_popcnt.sv rtl/cv32e40p_prefetch_buffer.sv rtl/cv32e40p_prefetch_controller.sv rtl/cv32e40p_register_file_ff.sv rtl/cv32e40p_register_file_latch.sv rtl/cv32e40p_sleep_unit.sv rtl/cv32e40p_top.sv "
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
                                dir("cv32e40p") {
                                    echo 'Starting synthesis for FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p cv32e40p -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("cv32e40p") {
                                    echo 'Flashing FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p cv32e40p -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Test colorlight_i9') {
                            steps {
                                echo 'Testing FPGA colorlight_i9.'
                                dir("cv32e40p") {
                                    sh 'echo "Test for FPGA in /dev/ttyACM0"'
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
                                dir("cv32e40p") {
                                    echo 'Starting synthesis for FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p cv32e40p -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("cv32e40p") {
                                    echo 'Flashing FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p cv32e40p -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Test digilent_nexys4_ddr') {
                            steps {
                                echo 'Testing FPGA digilent_nexys4_ddr.'
                                dir("cv32e40p") {
                                    sh 'echo "Test for FPGA in /dev/ttyUSB1"'
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
