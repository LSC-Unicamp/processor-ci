import os
import sys
import argparse
from core.config_manager import open_config_file
from core.repository_manager import (
    check_and_clone_repositories,
    BASE_PROCESSORS_DIR,
)
from core.test_cores import build_and_check_cores
from litex.build.generic_toolchain import GenericToolchain
from litex_patch import _build

parser = argparse.ArgumentParser(
    prog="RISC-V ISA CI", description="CI/CD for RISC-V cores", epilog=""
)
parser.add_argument(
    "-u", "--update", action="store_true", default=False, help="Update git repositories"
)
parser.add_argument(
    "-b",
    "--build",
    action="store_true",
    default=False,
    help="Builds enabled repositories",
)
parser.add_argument(
    "-l",
    "--load",
    action="store_true",
    default=False,
    help="Loads the synthesized hardware description into the FPGA memory",
)
parser.add_argument(
    "-f",
    "--flash",
    action="store_true",
    default=False,
    help="Writes the synthesis of the hardware description to the FPGA flash",
)
parser.add_argument(
    "-t", "--test", action="store_true", default=False, help="Run the tests"
)
parser.add_argument(
    "-F", dest="verilog_files", type=str, nargs="+", help="Input verilog file names"
)
parser.add_argument(
    "-B",
    "--build-custom-files",
    dest="build_custom_files",
    action="store_true",
    default=False,
    help="Builds custom verilog files repositories",
)

parser.add_argument(
    "-p",
    "--platform",
    type=str,
    default="ecp5_45f",
    help="Platform/board to be used, options: tangnano9k, tangnano20k, ecp5_45f",
)
args = parser.parse_args()


def main() -> None:
    data: dict[str, any] = open_config_file()

    if args.update:
        check_and_clone_repositories(data)

    if args.build:
        build_and_check_cores(data, board="ecp5_45f")


# 111100
# 110
# 1000010
if __name__ == "__main__":
    if args.update or args.build:
        if not os.path.exists(BASE_PROCESSORS_DIR):
            os.mkdir(BASE_PROCESSORS_DIR)

    GenericToolchain.build = _build

    main()
