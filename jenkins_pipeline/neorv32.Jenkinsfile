
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf neorv32'
                sh 'git clone --recursive --depth=1 https://github.com/stnolting/neorv32.git neorv32'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("neorv32") {
                    sh "ghdl -a --std=08               rtl/core/neorv32_application_image.vhd rtl/core/neorv32_boot_rom.vhd rtl/core/neorv32_bootloader_image.vhd rtl/core/neorv32_bus.vhd rtl/core/neorv32_cache.vhd rtl/core/neorv32_cfs.vhd rtl/core/neorv32_clockgate.vhd rtl/core/neorv32_cpu.vhd rtl/core/neorv32_cpu_alu.vhd rtl/core/neorv32_cpu_control.vhd rtl/core/neorv32_cpu_cp_bitmanip.vhd rtl/core/neorv32_cpu_cp_cfu.vhd rtl/core/neorv32_cpu_cp_cond.vhd rtl/core/neorv32_cpu_cp_crypto.vhd rtl/core/neorv32_cpu_cp_fpu.vhd rtl/core/neorv32_cpu_cp_muldiv.vhd rtl/core/neorv32_cpu_cp_shifter.vhd rtl/core/neorv32_cpu_decompressor.vhd rtl/core/neorv32_cpu_lsu.vhd rtl/core/neorv32_cpu_pmp.vhd rtl/core/neorv32_cpu_regfile.vhd rtl/core/neorv32_crc.vhd rtl/core/neorv32_debug_dm.vhd rtl/core/neorv32_debug_dtm.vhd rtl/core/neorv32_dma.vhd rtl/core/neorv32_dmem.vhd rtl/core/neorv32_fifo.vhd rtl/core/neorv32_gpio.vhd rtl/core/neorv32_gptmr.vhd rtl/core/neorv32_imem.vhd rtl/core/neorv32_mtime.vhd rtl/core/neorv32_neoled.vhd rtl/core/neorv32_onewire.vhd rtl/core/neorv32_package.vhd rtl/core/neorv32_pwm.vhd rtl/core/neorv32_sdi.vhd rtl/core/neorv32_slink.vhd rtl/core/neorv32_spi.vhd rtl/core/neorv32_sys.vhd rtl/core/neorv32_sysinfo.vhd rtl/core/neorv32_top.vhd rtl/core/neorv32_trng.vhd rtl/core/neorv32_twi.vhd rtl/core/neorv32_uart.vhd rtl/core/neorv32_wdt.vhd rtl/core/neorv32_xbus.vhd rtl/core/neorv32_xip.vhd rtl/core/neorv32_xirq.vhd "
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
                        stage('Synthesis and PnR') {
                            steps {
                                dir("neorv32") {
                                    echo 'Starting synthesis for FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p neorv32 -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("neorv32") {
                                    echo 'Flashing FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p neorv32 -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Test colorlight_i9') {
                            steps {
                                echo 'Testing FPGA colorlight_i9.'
                                dir("neorv32") {
                                    sh 'echo "Test for FPGA in /dev/ttyACM0"'
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
                        stage('Synthesis and PnR') {
                            steps {
                                dir("neorv32") {
                                    echo 'Starting synthesis for FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p neorv32 -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("neorv32") {
                                    echo 'Flashing FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p neorv32 -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Test digilent_nexys4_ddr') {
                            steps {
                                echo 'Testing FPGA digilent_nexys4_ddr.'
                                dir("neorv32") {
                                    sh 'echo "Test for FPGA in /dev/ttyUSB1"'
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
