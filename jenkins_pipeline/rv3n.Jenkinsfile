
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf rv3n'
                sh 'git clone --recursive https://github.com/risclite/rv3n rv3n'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("rv3n") {
                    sh "iverilog -o simulation.out -g2005  -s rv3n_top -I rtl rtl/define.v rtl/define_para.v rtl/include_func.v rtl/rv3n_chain_manager.v rtl/rv3n_csr.v rtl/rv3n_func_jcond.v rtl/rv3n_func_lsu.v rtl/rv3n_func_muldiv.v rtl/rv3n_func_op.v rtl/rv3n_gsr.v rtl/rv3n_predictor.v rtl/rv3n_stage_ch.v rtl/rv3n_stage_dc.v rtl/rv3n_stage_id.v rtl/rv3n_stage_if.v rtl/rv3n_top.v "
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
                                dir("rv3n") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p rv3n -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("rv3n") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p rv3n -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("rv3n") {
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
                                dir("rv3n") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p rv3n -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("rv3n") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p rv3n -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("rv3n") {
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
            dir("rv3n") {
                sh 'rm -rf *'
            }
        }
    }
}
