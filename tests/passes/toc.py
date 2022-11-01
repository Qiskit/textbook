# Tests notebooks/toc.yaml is valid

import yaml
from pathlib import Path

TOC_PATH = 'notebooks/toc.yaml'

with open(TOC_PATH) as f:
    toc = yaml.safe_load(f)

def check_exists(path):
    path = Path(path)
    if not path.exists():
        raise AssertionError(
                f"No file: {path}\n\n"
                f"{TOC_PATH} refers to a file ({path}) that does not exist. "
                 "Please add the missing file, or remove the reference.")

def check_resource(resource):
    for key in resource.keys():
        if not key in ['title', 'description', 'link', 'author']:
            raise AssertionError(
                    f"'{key}' not in resource:\n{resource}.\n\n"
                    "Please edit this resouce in {TOC_PATH} to include a value "
                    f"for '{key}'.")

def check_page(page):
    check_exists('./notebooks'+ page['url'] + '.ipynb')
    check_exists('./notebooks'+ page['previewImgUrl'])

def check_course(course):
    assert course['type'] in ['chapter', 'course', 'summer-school']
    overview = course['overviewInfo']
    check_exists('./notebooks' + overview['thumbnailUrl'])
    _, _ = overview['description']['short'], overview['description']['long']
    for key in overview.keys():
        assert key in ['description',
                       'thumbnailUrl',
                       'prerequisites',
                       'externalRecommendedReadings',
                       'externalRecommendedReadingsPreamble']
    for page in course['sections']:
        check_page(page)
    if 'externalRecommendedReadings' in overview:
        for resource in overview['externalRecommendedReadings']:
            check_resource(resource)
    if 'prerequisites' in overview:
        for resource in overview['prerequisites']:
            check_resource(resource)

for course in toc:
    check_course(course)
