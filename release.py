"""
This script automatically uploads your notebooks to directus.
Example usage:

    python release.py notebooks/basics/**/*.ipynb


Each lesson folder must contain a `directus_info.json` file, which should look
like this:
```
  {
    "STAGING": {
      "url": "https://learning-api-dev.quantum-computing.ibm.com",
      "id": "11845b3b-1acc-4173-b93b-9f7cbcbb552a"
    }
  }
```

Explanation:
  * "STAGING" is an alias for the database you want to upload to. You'll
  probably want one for STAGING and one for PRODUCTION
  * "url" is the URL to the directus database
  * "id" is the lesson ID, you can get this from the URL of the lesson, which
  is: `{url}/admin/content/lessons/{lesson_id}`

"""
import json
import shutil
import os
from pathlib import Path
from getpass import getpass
import random
import sys
from dataclasses import dataclass
from types import SimpleNamespace
import requests


@dataclass
class Lesson:
    def __init__(self, notebook_path, database):
        self.path = Path(notebook_path).parents[0]
        self.name = self.path.parts[-1]
        self.zip_path = None

        directus_info_path = self.path / "directus_info.json"
        self.has_directus_info = directus_info_path.exists()

        if self.has_directus_info:
            with open(self.path / "directus_info.json") as file:
                data = json.loads(file.read())[database]
                self.directus = SimpleNamespace(**data)


def get_access_token(database_url):
    """
    Either token is in env variable, or we use login details
    to get temporary access token.
    """
    if os.environ.get("DIRECTUS_TOKEN", None) is not None:
        print("  * Using saved access token...")
        return os.environ.get("DIRECTUS_TOKEN")

    print("  🔑 Logging in:")
    response = requests.post(
        f"{database_url}/auth/login",
        json=(
            {"email": input("     > Email: "), "password": getpass("     > Password: ")}
        ),
    )
    if response.status_code != 200:
        print("    Couldn't log in 😕\n    Exiting...")
        sys.exit()

    token = response.json()["data"]["access_token"]
    os.environ["DIRECTUS_TOKEN"] = token
    print("    Saved temporary token for remaining uploads.\n")

    return token


def push_notebook(notebook_path):
    """
    Steps:
      1. Get access token from environment variable, or ask for login details
         to get temporary access token
      2. Get the translation ID of the English translation (needed for upload)
      3. Zip the folder containing notebook and images
      4. Upload the zip file to the database
      5. Link the zip file in the database to the lesson
      6. Clean up: delete the zip file from local disk

    Args:
        lesson_path (str): path to folder containing notebook and `directus_info.json`.
    """
    database_name = os.environ.get("DIRECTUS_DATABASE", "STAGING")
    lesson = Lesson(notebook_path, database_name)
    if not lesson.has_directus_info:
        print(f"No `directus_info.json` found for {lesson.name}; skipping...")
        return

    print(f"Pushing '{lesson.name}' to '{database_name}':")

    # 1. Sort out auth stuff
    auth_header = {"Authorization": f"Bearer {get_access_token(lesson.directus.url)}"}

    # 2. Get ID of english translation (needed for upload)
    print("  * Finding English translation...")
    response = requests.get(
        f"{lesson.directus.url}/items/lessons/{lesson.directus.id}"
         "?fields[]=translations.id,translations.languages_code",
        headers=auth_header,
    )

    for translation in response.json()["data"]["translations"]:
        if translation["languages_code"] == "en-US":
            translation_id = translation["id"]
            break
        raise ValueError("No 'en-US' translation found!")

    # 3. Zip file
    print("  * Zipping folder...")
    lesson.zip_path = Path(
        shutil.make_archive(
            lesson.path / f"{random.randint(0, 1_000_000_000)}_{lesson.name}",
            "zip",
            root_dir=lesson.path,
        )
    )

    # 4. Upload .zip
    print(f"  * Uploading `{lesson.zip_path.name}`...")
    with open(lesson.zip_path, "rb") as fileobj:
        response = requests.post(
            lesson.directus.url + "/files",
            files={"file": (fileobj)},
            data={"filename": lesson.zip_path.stem},
            headers=auth_header,
        )

    temp_file_id = response.json()["data"]["id"]
    if response.status_code != 200:
        raise Exception(
            f"Problem connecting to Directus (error code {response.status_code}."
        )

    print(f"  * Linking upload to lesson {lesson.directus.id}...")
    # 5. Link .zip to content
    response = requests.patch(
        lesson.directus.url + f"/items/lessons/{lesson.directus.id}",
        json={"translations": [{"id": translation_id, "temporal_file": temp_file_id}]},
        headers=auth_header,
    )
    if response.status_code != 200:
        raise Exception(
            f"Problem connecting to Directus (error code {response.status_code})."
        )

    # 6. Clean up zipped file afterwards
    print(f"  * Cleaning up `{lesson.zip_path.name}`...")
    os.remove(lesson.zip_path)

    print("  ✨ Complete! ✨")


if __name__ == "__main__":
    for notebook in sys.argv[1:]:
        push_notebook(notebook)
