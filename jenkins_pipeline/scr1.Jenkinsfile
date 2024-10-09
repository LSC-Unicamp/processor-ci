
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf scr1'
                sh 'git clone --recursive https://github.com/syntacore/scr1 scr1'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("scr1") {
                    sh "iverilog -o simulation.out -g2012  -s scr1_core_top -I src/includes src/core/scr1_clk_ctrl.sv src/core/scr1_core_top.sv src/core/scr1_dm.sv src/core/scr1_dmi.sv src/core/scr1_scu.sv src/core/scr1_tapc.sv src/core/scr1_tapc_shift_reg.sv src/core/scr1_tapc_synchronizer.sv src/core/pipeline/scr1_ipic.sv src/core/pipeline/scr1_pipe_csr.sv src/core/pipeline/scr1_pipe_exu.sv src/core/pipeline/scr1_pipe_hdu.sv src/core/pipeline/scr1_pipe_ialu.sv src/core/pipeline/scr1_pipe_idu.sv src/core/pipeline/scr1_pipe_ifu.sv src/core/pipeline/scr1_pipe_lsu.sv src/core/pipeline/scr1_pipe_mprf.sv src/core/pipeline/scr1_pipe_tdu.sv src/core/pipeline/scr1_pipe_top.sv src/core/pipeline/scr1_tracelog.sv src/core/primitives/scr1_cg.sv src/core/primitives/scr1_reset_cells.sv "
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
                                dir("scr1") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p scr1 -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("scr1") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p scr1 -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("scr1") {
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
                                dir("scr1") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p scr1 -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("scr1") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p scr1 -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("scr1") {
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
