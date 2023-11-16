import os
import sys
from time import time
from git import Repo, FetchInfo


BASE_PROCESSORS_DIR = "./processors"


def check_processor_repository(name: str, repository: str, folder: str) -> None:
    path = os.path.join(BASE_PROCESSORS_DIR, folder)

    repo = None

    if not os.path.exists(path):
        print(f"Log: cloning repository")
        repo = Repo.clone_from(repository, path)
    else:
        print(f"Log: Opening repository")
        repo = Repo(path)

    print(f"Log: Updating repository")
    repo.git.pull()


def check_and_clone_repositories(data: dict[str, any]) -> None:
    print(f"Log: Pulling changes from repositories")
    if not "cores" in data:
        sys.exit(f"[ {time()} ] Error: cores key not found in config file")

    for i, core in enumerate(data["cores"]):
        if not core["enable"]:
            continue
        name: str = core["name"]
        repository: str = core["repository"]
        folder: str = core["folder"]

        print(f"Log: updating repository {i + 1} processor: {name}")

        check_processor_repository(name, repository, folder)
