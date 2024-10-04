
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf F03x'
                sh 'git clone --recursive https://github.com/klessydra/F03x.git F03x'
            }
        }

        stage('Simulation') {
            steps {
                dir("F03x") {
                    sh "ghdl -a --std=08   klessydra-f0-3th/PKG_RiscV_Klessydra_thread_parameters.vhd klessydra-f0-3th/PKG_RiscV_Klessydra.vhd klessydra-f0-3th/TMR_REG_PKG.vhd klessydra-f0-3th/RTL-CSR_Unit_TMR.vhd klessydra-f0-3th/RTL-Debug_Unit.vhd klessydra-f0-3th/RTL-Processing_Pipeline_TMR.vhd klessydra-f0-3th/RTL-Program_Counter_unit_TMR.vhd klessydra-f0-3th/CMP-TMR_REG.vhd klessydra-f0-3th/STR-Klessydra_top.vhd "
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
                                dir("F03x") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p F03x -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("F03x") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p F03x -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("F03x") {
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
                                dir("F03x") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p F03x -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("F03x") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p F03x -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("F03x") {
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
            dir("F03x") {
                sh 'rm -rf *'
            }
        }
    }
}
