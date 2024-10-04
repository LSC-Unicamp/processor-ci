
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf tinyriscv'
                sh 'git clone --recursive https://github.com/liangkangnan/tinyriscv.git tinyriscv'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("tinyriscv") {
                    sh "iverilog -o simulation.out -g2005 -s tinyriscv_soc_tb -I rtl/core rtl/core/clint.v rtl/core/csr_reg.v rtl/core/ctrl.v rtl/core/defines.v rtl/core/div.v rtl/core/ex.v rtl/core/id_ex.v rtl/core/id.v rtl/core/if_id.v rtl/core/pc_reg.v rtl/core/regs.v rtl/core/rib.v rtl/core/tinyriscv.v tb/tinyriscv_soc_tb.v rtl/debug/jtag_dm.v rtl/debug/jtag_driver.v rtl/debug/jtag_top.v rtl/debug/uart_debug.v rtl/perips/gpio.v rtl/perips/ram.v rtl/perips/rom.v rtl/perips/spi.v rtl/perips/timer.v rtl/perips/uart.v rtl/soc/tinyriscv_soc_top.v rtl/utils/full_handshake_rx.v rtl/utils/full_handshake_tx.v rtl/utils/gen_buf.v rtl/utils/gen_dff.v && vvp simulation.out"
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("tinyriscv") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p tinyriscv -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("tinyriscv") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p tinyriscv -b digilent_nexys4_ddr'
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
            dir("tinyriscv") {
                sh 'rm -rf *'
            }
        }
    }
}
