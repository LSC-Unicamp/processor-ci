
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf DV-CPU-RV'
                sh 'git clone --recursive https://github.com/devindang/dv-cpu-rv.git DV-CPU-RV'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("DV-CPU-RV") {
                    sh "iverilog -o simulation.out -g2005  -s rv_core  core/rtl/rv_alu.v core/rtl/rv_alu_ctrl.v core/rtl/rv_branch_predict.v core/rtl/rv_branch_test.v core/rtl/rv_core.v core/rtl/rv_ctrl.v core/rtl/rv_data_mem.v core/rtl/rv_div.v core/rtl/rv_dpram.v core/rtl/rv_forward.v core/rtl/rv_hzd_detect.v core/rtl/rv_imm_gen.v core/rtl/rv_instr_mem.v core/rtl/rv_mem_map.v core/rtl/rv_mul.v core/rtl/rv_rf.v core/rtl/rv_instr_mem.v core/rtl/rv_data_mem.v "
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
                        stage('Síntese e PnR') {
                            steps {
                                dir("DV-CPU-RV") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p DV-CPU-RV -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("DV-CPU-RV") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p DV-CPU-RV -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("DV-CPU-RV") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT=/dev/ttyACM0 python /eda/processor-ci-communication/run_tests.py' 
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
                        stage('Síntese e PnR') {
                            steps {
                                dir("DV-CPU-RV") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p DV-CPU-RV -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("DV-CPU-RV") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p DV-CPU-RV -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("DV-CPU-RV") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT=/dev/ttyUSB1 python /eda/processor-ci-communication/run_tests.py' 
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
