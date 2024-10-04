
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf T03x'
                sh 'git clone --recursive https://github.com/klessydra/T03x.git T03x'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("T03x") {
                    sh "ghdl -a --std=08  klessydra-t0-3th/PKG_RiscV_Klessydra_thread_parameters.vhd klessydra-t0-3th/PKG_RiscV_Klessydra.vhd klessydra-t0-3th/RTL-CSR_Unit.vhd klessydra-t0-3th/RTL-Debug_Unit.vhd klessydra-t0-3th/RTL-Processing_Pipeline.vhd klessydra-t0-3th/RTL-Program_Counter_unit.vhd klessydra-t0-3th/STR-Klessydra_top.vhd "
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("T03x") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p T03x -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("T03x") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p T03x -b digilent_nexys4_ddr'
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
            dir("T03x") {
                sh 'rm -rf *'
            }
        }
    }
}
