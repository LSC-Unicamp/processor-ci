
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf T13x'
                sh 'git clone --recursive https://github.com/klessydra/T13x.git T13x'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("T13x") {
                    sh "ghdl -a --std=08  klessydra-t1-3th/PKG_RiscV_Klessydra.vhd klessydra-t1-3th/RTL-Accumulator.vhd klessydra-t1-3th/RTL-CSR_Unit.vhd klessydra-t1-3th/RTL-Debug_Unit.vhd klessydra-t1-3th/RTL-DSP_Unit.vhd klessydra-t1-3th/RTL-Scratchpad_Memory.vhd klessydra-t1-3th/RTL-Scratchpad_Memory_Interface.vhd klessydra-t1-3th/RTL-Program_Counter_unit.vhd klessydra-t1-3th/RTL-IF_STAGE.vhd klessydra-t1-3th/RTL-ID_STAGE.vhd klessydra-t1-3th/RTL-IE_STAGE.vhd klessydra-t1-3th/RTL-Load_Store_Unit.vhd klessydra-t1-3th/RTL-Processing_Pipeline.vhd klessydra-t1-3th/STR-Klessydra_top.vhd klessydra-t1-3th/RTL-Registerfile.vhd "
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("T13x") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p T13x -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("T13x") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p T13x -b digilent_nexys4_ddr'
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
            dir("T13x") {
                sh 'rm -rf *'
            }
        }
    }
}
