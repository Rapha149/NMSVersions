import json
import os
import re
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ElementTree
from datetime import datetime

import pytz
import requests
from tabulate import tabulate


def main():
    namespaces = {'pom': 'http://maven.apache.org/POM/4.0.0'}

    version_file_path = 'nms-versions.json'
    readme_file_path = 'README.md'

    if os.path.exists(version_file_path):
        if not os.path.isfile(version_file_path):
            print('Not updating nms-versions.json because it is not a file', file=sys.stderr)
            exit(1)

        with open(version_file_path) as file:
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
            print(f'Skipping {version} (already in {version_file_path})')
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

    versions = {key: value for key, value in versions.items() if key in version_order}
    if new_versions:
        sorted_versions = dict(sorted(versions.items(), key=lambda x: version_order.index(x[0])))
        with open(version_file_path, 'w') as file:
            json.dump(sorted_versions, file, indent=4)

        version_list = []
        for bukkit_version, nms_version in sorted_versions.items():
            minecraft_version = bukkit_version.split('-')[0]
            version_list.append((minecraft_version, bukkit_version, nms_version))

        if os.path.isfile(readme_file_path):
            with open(readme_file_path) as file:
                readme = file.read()

            if re.search('<!-- ?versions_start ?-->(.|\n)*<!-- ?versions_end ?-->', readme):
                rows = []
                last_major = None
                for minecraft_version, bukkit_version, nms_version in version_list:
                    major = int(minecraft_version.split('.')[1])
                    if last_major is not None and major != last_major:
                        rows.append(())
                    last_major = major
                    rows.append((minecraft_version, nms_version, bukkit_version))

                table = tabulate(rows, headers=['Minecraft Version', 'NMS Version', 'Bukkit Version String'], tablefmt='pipe')
                readme = re.sub('<!-- ?versions_start ?-->(.|\n)*<!-- ?versions_end ?-->',
                                f'<!-- versions_start -->\n{table}\n<!-- versions_end -->', readme)

            if re.search('<!-- ?date_start ?-->.*<!-- ?date_end ?-->', readme):
                date = urllib.parse.quote(datetime.now(pytz.timezone('UTC')).strftime('%Y--%m--%d_%H:%M_%Z'), safe='')
                badge_date = f'![Last Update](https://img.shields.io/badge/Last_Update-{date}-blue)'
                readme = re.sub('<!-- ?date_start ?-->.*<!-- ?date_end ?-->',
                                f'<!-- date_start -->{badge_date}<!-- date_end -->', readme)

            if re.search('<!-- ?latest_version_start ?-->.*<!-- ?latest_version_end ?-->', readme):
                latest_version = urllib.parse.quote(version_order[-1].split('-')[0], safe='')
                badge_latest_version = f'![Latest Included Version](https://img.shields.io/badge/Latest_Included_Version-{latest_version}-slateblue)'
                readme = re.sub('<!-- ?latest_version_start ?-->.*<!-- ?latest_version_end ?-->',
                                f'<!-- latest_version_start -->{badge_latest_version}<!-- latest_version_end -->', readme)

            with open(readme_file_path, 'w') as file:
                file.write(readme)

        subprocess.call(['git', 'add', version_file_path, readme_file_path])
        subprocess.call(['git', 'commit', '-m', f'Add version(s): {", ".join(new_versions)}'])

        ntfy_url, ntfy_token = os.getenv('NTFY_URL'), os.getenv('NTFY_TOKEN')
        if ntfy_url:
            headers = {}
            if ntfy_token:
                headers['Authorization'] = ntfy_token
            for minecraft_version, bukkit_version, nms_version in version_list:
                if bukkit_version in new_versions:
                    requests.post(
                        ntfy_url,
                        data=f'NMS Version: {nms_version}',
                        headers={
                            **headers,
                            'Title': f'New Minecraft Version: {minecraft_version}'
                        }
                    )

    print(f'\nAdded {len(new_versions)} new version(s) to {version_file_path}')


def _get_xml(url: str) -> ElementTree.Element:
    response = requests.get(url)
    if int(response.status_code / 100) != 2:
        raise Exception(f'Failed to get {url}: {response.status_code}')
    return ElementTree.fromstring(response.content)


if __name__ == '__main__':
    main()
