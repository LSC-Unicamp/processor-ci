
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
                    sh "iverilog -o simulation.out -g2005  -s tb_rv_core  rtl/rv_alu_ctrl.v rtl/rv_alu.v rtl/rv_branch_predict.v rtl/rv_branch_test.v rtl/rv_core.v rtl/rv_ctrl.v rtl/rv_data_mem.v rtl/rv_div.v rtl/rv_dpram.v rtl/rv_forward.v rtl/rv_hzd_detect.v rtl/rv_imm_gen.v rtl/rv_instr_mem.v rtl/rv_mem_map.v rtl/rv_mul.v rtl/rv_rf.v bench/tb_rv_core.v && vvp simulation.out"
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
                                    // Insira aqui os comandos de teste necessários
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
                                    // Insira aqui os comandos de teste necessários
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
            dir("DV-CPU-RV") {
                sh 'rm -rf *'
            }
        }
    }
}
