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
import requests
import shutil
import os
from pathlib import Path
from getpass import getpass
import random
import sys
from dataclasses import dataclass
from types import SimpleNamespace

@dataclass
class Lesson:
    def __init__(self, notebook_path, database):
        self.path = Path(notebook_path).parents[0]
        self.name = self.path.parts[-1]
        self.zip_path = None

        with open(self.path / "directus_info.json") as f:
            data = json.loads(f.read())[database]
            self.directus = SimpleNamespace(**data)


def input_login_environment_variables():
    os.environ["DIRECTUS_EMAIL"] = input("Email: ")
    os.environ["DIRECTUS_PASSWORD"] = getpass()

def push_content(notebook_path):
    """
    Args:
        lesson_path (str): path to folder containing notebook and `directus_info.json`.
    """
    if os.environ.get("DIRECTUS_PASSWORD", None) is None:
        raise ValueError("No directus login details found: exiting")


    DATABASE = os.environ.get("DIRECTUS_DATABASE", "STAGING")
    lesson = Lesson(notebook_path, DATABASE)

    print(f"\nPushing '{lesson.name}' to '{DATABASE}':")

    # Zip file
    print("  * Zipping folder...")
    lesson.zip_path = Path(
        shutil.make_archive(
            lesson.path / f"{random.randint(0, 1_000_000_000)}_{lesson.name}",
            'zip',
            root_dir=lesson.path
        )
    )

    # Log in
    print("  * Logging in...")
    response = requests.post(
        f"{lesson.directus.url}/auth/login",
        json=({"email": os.environ["DIRECTUS_EMAIL"],
               "password": os.environ["DIRECTUS_PASSWORD"]}),
    )

    ACCESS_TOKEN = response.json()["data"]["access_token"]

    print("  * Finding translations ID...")
    # Get id of english translation
    response = requests.get(
        f"{lesson.directus.url}/items/lessons/{lesson.directus.id}?fields[]=translations.id,translations.languages_code",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    TRANSLATION_ID = 0
    for translation in response.json()["data"]["translations"]:
        if translation["languages_code"] == "en-US":
            TRANSLATION_ID = translation["id"]
            break
        raise ValueError("No en-US translation found!")

    print(f"  * Uploading `{lesson.zip_path.name}`...")
    # Update page
    # 1. Upload .zip
    with open(lesson.zip_path, "rb") as fileobj:
        response = requests.post(
            lesson.directus.url + f"/files",
            files={"file": (fileobj)},
            data={"filename": lesson.zip_path.stem},
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        )

    temp_file_id = response.json()["data"]["id"]
    if response.status_code != 200:
        raise Exception(f"Problem connecting to Directus (error code {response.status_code}.")


    print(f"  * Linking upload to lesson {lesson.directus.id}...")
    # 2. Link .zip to content
    response = requests.patch(
        lesson.directus.url + f"/items/lessons/{lesson.directus.id}",
        json={
            "translations": [
                {"id": TRANSLATION_ID, "temporal_file": temp_file_id}
            ]
        },
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    if response.status_code != 200:
        raise Exception(f"Problem connecting to Directus (error code {response.status_code}.")

    # Clean up zipped file afterwards
    print(f"  * Deleting `{lesson.zip_path.name}`...")
    os.remove(lesson.zip_path)

    print("  Complete!")


if __name__=="__main__":
    if os.environ.get("DIRECTUS_PASSWORD", None) is None:
        input_login_environment_variables()
    for notebook in sys.argv[1:]:
        push_content(notebook)
