import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

import requests


def main():
    namespaces = {'pom': 'http://maven.apache.org/POM/4.0.0'}

    file_path = 'nms-versions.json'
    if os.path.exists(file_path):
        if not os.path.isfile(file_path):
            print('Not updating nms-versions.json because it is not a file', file=sys.stderr)
            exit(1)

        with open(file_path) as file:
            versions = json.load(file)
    else:
        versions = {}

    version_order = []
    new_versions = []
    root_xml = _get_xml('https://repo.codemc.io/repository/nms/org/spigotmc/spigot/maven-metadata.xml')
    for version_element in root_xml.findall('versioning/versions/version'):
        version = version_element.text
        version_order.append(version)

        if version in versions:
            print(f'Skipping {version} (already in {file_path})')
            continue

        version_xml = _get_xml(f'https://repo.codemc.io/repository/nms/org/spigotmc/spigot/{version}/maven-metadata.xml')
        snapshot_xml = version_xml.find('versioning/snapshot')
        snapshot_version = snapshot_xml.find('timestamp').text + '-' + snapshot_xml.find('buildNumber').text

        pom_location = f'spigot-{version.replace("SNAPSHOT", snapshot_version)}.pom'
        pom_xml = _get_xml(f'https://repo.codemc.io/repository/nms/org/spigotmc/spigot/{version}/{pom_location}')
        nms_version = pom_xml.find('pom:properties/pom:minecraft_version', namespaces).text

        versions[version] = nms_version
        new_versions.append(version)
        print(f'Parsed {version} -> {nms_version}')

    if new_versions:
        with open(file_path, 'w') as file:
            sorted_versions = dict(sorted(versions.items(), key=lambda x: version_order.index(x[0]))),
            json.dump(sorted_versions, file, indent=4)

    print(f'\nAdded {len(new_versions)} new version(s) to {file_path}')

    subprocess.call(['git', 'add', file_path])
    subprocess.call(['git', 'commit', '-m', f'Add version(s): {", ".join(new_versions)}'])


def _get_xml(url: str) -> ET.Element:
    response = requests.get(url)
    if int(response.status_code / 100) != 2:
        raise Exception(f'Failed to get {url}: {response.status_code}')
    return ET.fromstring(response.content)


if __name__ == '__main__':
    main()
