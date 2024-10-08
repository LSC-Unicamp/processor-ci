
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf dv-cpu-rv'
                sh 'git clone --recursive https://github.com/devindang/dv-cpu-rv dv-cpu-rv'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("dv-cpu-rv") {
                    sh "iverilog -o simulation.out -g2005  -s rv_core  core/rtl/rv_alu.v core/rtl/rv_alu_ctrl.v core/rtl/rv_branch_predict.v core/rtl/rv_core.v core/rtl/rv_ctrl.v core/rtl/rv_div.v core/rtl/rv_forward.v core/rtl/rv_hzd_detect.v core/rtl/rv_imm_gen.v core/rtl/rv_mem_map.v core/rtl/rv_mul.v core/rtl/rv_rf.v "
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
                                dir("dv-cpu-rv") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p dv-cpu-rv -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("dv-cpu-rv") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p dv-cpu-rv -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("dv-cpu-rv") {
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
                                dir("dv-cpu-rv") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p dv-cpu-rv -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("dv-cpu-rv") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p dv-cpu-rv -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("dv-cpu-rv") {
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
            dir("dv-cpu-rv") {
                sh 'rm -rf *'
            }
        }
    }
}
