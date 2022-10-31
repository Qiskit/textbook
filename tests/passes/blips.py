# This script checks that each quiz in NB_PATHS has a unique goal name, and that
# no notebook uses the internal provider
import os
from typing import List


NB_ROOT = './notebooks'

def check_file(filename: str, goal_names: List[str]) -> None:
    with open(filename, encoding='utf-8') as f:
        content: str = f.read()
    for line in content.split('\n'):
        if '(goal=\\"' in line:
            name = line.split('"')[2].strip('\\')
            if name in goal_names:
                raise ValueError(
                    f'Found multiple quizzes with goal name "{name}"'
                )
            else:
                goal_names.append(name)

    if 'ibm-q-internal' in content:
        raise ValueError(
            f"Found use of non-open provider ('ibm-q-internal') in '{filename}',"
            " please use 'ibm-q'."
        )


if __name__ == '__main__':
    goal_names: List[str] = []
    for root, dirs, files in os.walk(NB_ROOT):
        for name in files:
            if name.endswith('-checkpoint.ipynb'):
                continue
            if name.endswith('.ipynb'):
                check_file(os.path.join(root, name), goal_names)
