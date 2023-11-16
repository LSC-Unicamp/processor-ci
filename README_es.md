# RISC-V ISA CI

CI/CD para núcleos RISC-V

Si no hablas portugués, [haz clic aquí](README_es.md)

![FPGA utilizados para pruebas](docs/imgs/fpgas.jpeg)

Software desarrollado para probar procesadores basados en la arquitectura RISC-V. El software cubre pruebas desde la síntesis del procesador en lenguaje HDL (Verilog o VHDL) hasta la ejecución de instrucciones con el procesador operando en FPGA.

## Requisitos:

Para la ejecución del software, será necesario instalar algunas dependencias. Entre ellas se encuentran:

- Litex: [https://github.com/enjoy-digital/litex](https://github.com/enjoy-digital/litex)
- Requests: [https://pypi.org/project/requests/](https://pypi.org/project/requests/)
- GitPython: [https://pypi.org/project/GitPython/0.3.2/](https://pypi.org/project/GitPython/0.3.2/)
- OSS-Cad-Suite: [https://github.com/YosysHQ/oss-cad-suite-build](https://github.com/YosysHQ/oss-cad-suite-build)
- Toolchain de la placa a utilizar: Gowin, Vivado, Quartus ...

## Hardware:

Para la ejecución de los procesadores, será necesario utilizar al menos una FPGA. Actualmente, se admiten las siguientes FPGAs:

- Tang nano 20k
- Tang nano 9k
- Lattice ECP5 45F

## Partes implementadas

- [x] Clonar y actualizar repositorios GIT
- [x] Síntesis de núcleo(s)/SoC(s)
- [ ] Estandarización de las conexiones para diversas FPGAs
- [ ] Verificación del proceso de síntesis
- [x] Grabación en FPGA
- [ ] Debugger serial con la FPGA
- [ ] Ejecución de instrucciones
- [ ] Envío automatizado de archivos de memoria a la FPGA

## Dudas y Errores:

En caso de alguna duda, error en la aplicación o sugerencia, utiliza el menú de [issues](https://github.com/JN513/riscv-isa-ci/issues) en Github.

## Licencia:

Este repositorio está bajo la Licencia Pública General de GNU V3. Las bibliotecas y software de terceros siguen las licencias utilizadas por los repositorios originales.

## Software de terceros:

- Implementación del Módulo UART: [https://github.com/ben-marshall/uart](https://github.com/ben-marshall/uart)
