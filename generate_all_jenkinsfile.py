import os
from core.jenkins_pipeline import generate_jenkinsfile
from main import load_config, get_processor_data

# Load configuration from JSON file

BASE_DIR = "jenkins_pipeline/"
FPGAs = [
    "colorlight_i9",
    "digilent_nexys4_ddr",
    # "gowin_tangnano_20k",
    # "xilinx_vc709",
    # "digilent_arty_a7_100t"
]
main_script_path = "/eda/processor-ci/main.py"


def main() -> None:
    config = load_config("config.json")

    for key in config["cores"].keys():
        processor_data = get_processor_data(config, key)
        generate_jenkinsfile(
            processor_data,
            FPGAs,
            main_script_path,
            processor_data["language_version"],
            processor_data["extra_flags"],
        )
        os.rename("Jenkinsfile", f'{BASE_DIR}{processor_data["name"]}.Jenkinsfile')

    print("Jenkinsfiles generated successfully.")


if __name__ == "__main__":
    main()
