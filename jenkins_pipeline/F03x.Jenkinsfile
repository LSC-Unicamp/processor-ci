
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf F03x'
                sh 'git clone --recursive https://github.com/klessydra/F03x.git F03x'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("F03x") {
                    sh "ghdl -a --std=08  klessydra-f0-3th/PKG_RiscV_Klessydra_thread_parameters.vhd klessydra-f0-3th/PKG_RiscV_Klessydra.vhd klessydra-f0-3th/TMR_REG_PKG.vhd klessydra-f0-3th/RTL-CSR_Unit_TMR.vhd klessydra-f0-3th/RTL-Debug_Unit.vhd klessydra-f0-3th/RTL-Processing_Pipeline_TMR.vhd klessydra-f0-3th/RTL-Program_Counter_unit_TMR.vhd klessydra-f0-3th/CMP-TMR_REG.vhd klessydra-f0-3th/STR-Klessydra_top.vhd "
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("F03x") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p F03x -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("F03x") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p F03x -b digilent_nexys4_ddr'
                            }
                        }
                    }
                }
            }
        }

        stage('Run Tests') {
            parallel {
                stage('colorlight_i9 Tests') {
                    steps {
                        echo 'Executando testes para FPGA colorlight_i9.'
                        unlock(resource: 'colorlight_i9')
                    }
                }
                stage('digilent_nexys4_ddr Tests') {
                    steps {
                        echo 'Executando testes para FPGA digilent_nexys4_ddr.'
                        unlock(resource: 'digilent_nexys4_ddr')
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
