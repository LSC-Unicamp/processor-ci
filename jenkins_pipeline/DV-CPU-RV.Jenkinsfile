
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf DV-CPU-RV'
                sh 'git clone --recursive https://github.com/devindang/dv-cpu-rv.git DV-CPU-RV'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("DV-CPU-RV") {
                    sh "iverilog -o simulation.out -g2005 -s tb_rv_core  rtl/rv_alu_ctrl.v rtl/rv_alu.v rtl/rv_branch_predict.v rtl/rv_branch_test.v rtl/rv_core.v rtl/rv_ctrl.v rtl/rv_data_mem.v rtl/rv_div.v rtl/rv_dpram.v rtl/rv_forward.v rtl/rv_hzd_detect.v rtl/rv_imm_gen.v rtl/rv_instr_mem.v rtl/rv_mem_map.v rtl/rv_mul.v rtl/rv_rf.v bench/tb_rv_core.v && vvp simulation.out"
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("DV-CPU-RV") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p DV-CPU-RV -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("DV-CPU-RV") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p DV-CPU-RV -b digilent_nexys4_ddr'
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
            dir("DV-CPU-RV") {
                sh 'rm -rf *'
            }
        }
    }
}
