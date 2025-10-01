# NMS Versions [![Update Task](https://img.shields.io/github/actions/workflow/status/Rapha149/NMSVersions/update.yml?logo=github&label=Update%20Task)](https://github.com/Rapha149/NMSVersions/actions/workflows/update.yml) <!-- date_start -->![Last Update](https://img.shields.io/badge/Last_Update-2025--10--01_01%3A13_UTC-blue)<!-- date_end --> <!-- latest_version_start -->![Latest Included Version](https://img.shields.io/badge/Latest_Included_Version-1.21.9-slateblue)<!-- latest_version_end -->

This repository contains an automatically updated JSON file which links the Bukkit versions (e.g. `1.20.6-R0.1-SNAPSHOT`) to the corresponding NMS version (e.g. `1_20_R4`).  
This is useful for Spigot plugins which use NMS and have a Wrapper class for each different version, because as of Paper 1.20.5 the craftbukkit packages no longer contain the NMS version and you can't parse the NMS version from that package like before.

## Usage

The raw file is available here: [nms-versions.json](https://raw.githubusercontent.com/Rapha149/NMSVersions/main/nms-versions.json)

An example of parsing the NMS version would be the following:
```java
try {
    HttpURLConnection conn = (HttpURLConnection) new URL("https://raw.githubusercontent.com/Rapha149/NMSVersions/main/nms-versions.json").openConnection();
    conn.setRequestMethod("GET");
    conn.connect();

    try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
        JSONObject json = new JSONObject(br.lines().collect(Collectors.joining()));
        if (json.has(Bukkit.getBukkitVersion())) {
            String nmsVersion = json.getString(Bukkit.getBukkitVersion());
        } else {
            // Version is not yet available in the json file, see the updates section
        }
    }
} catch (IOException e) {
    // Handle exception
}
```

## Updates

The file is updated every 12 hours.  
However, the NMS versions are parsed from the NMS repository at [repo.codemc.io](https://repo.codemc.io/#browse/browse:nms:org%2Fspigotmc%2Fspigot) which means that that repository first has to update before the file can get updated.

## Versions

<!-- versions_start -->
| Minecraft Version   | NMS Version   | Bukkit Version String   |
|:--------------------|:--------------|:------------------------|
| 1.21.9              | 1_21_R6       | 1.21.9-R0.1-SNAPSHOT    |
| 1.21.8              | 1_21_R5       | 1.21.8-R0.1-SNAPSHOT    |
| 1.21.7              | 1_21_R5       | 1.21.7-R0.1-SNAPSHOT    |
| 1.21.6              | 1_21_R5       | 1.21.6-R0.1-SNAPSHOT    |
| 1.21.5              | 1_21_R4       | 1.21.5-R0.1-SNAPSHOT    |
| 1.21.4              | 1_21_R3       | 1.21.4-R0.1-SNAPSHOT    |
| 1.21.3              | 1_21_R2       | 1.21.3-R0.1-SNAPSHOT    |
| 1.21.1              | 1_21_R1       | 1.21.1-R0.1-SNAPSHOT    |
|                     |               |                         |
| 1.20.6              | 1_20_R4       | 1.20.6-R0.1-SNAPSHOT    |
| 1.20.5              | 1_20_R4       | 1.20.5-R0.1-SNAPSHOT    |
| 1.20.4              | 1_20_R3       | 1.20.4-R0.1-SNAPSHOT    |
| 1.20.3              | 1_20_R3       | 1.20.3-R0.1-SNAPSHOT    |
| 1.20.2              | 1_20_R2       | 1.20.2-R0.1-SNAPSHOT    |
| 1.20.1              | 1_20_R1       | 1.20.1-R0.1-SNAPSHOT    |
| 1.20                | 1_20_R1       | 1.20-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.19.4              | 1_19_R3       | 1.19.4-R0.1-SNAPSHOT    |
| 1.19.3              | 1_19_R2       | 1.19.3-R0.1-SNAPSHOT    |
| 1.19.2              | 1_19_R1       | 1.19.2-R0.1-SNAPSHOT    |
| 1.19.1              | 1_19_R1       | 1.19.1-R0.1-SNAPSHOT    |
| 1.19                | 1_19_R1       | 1.19-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.18.2              | 1_18_R2       | 1.18.2-R0.1-SNAPSHOT    |
| 1.18.1              | 1_18_R1       | 1.18.1-R0.1-SNAPSHOT    |
| 1.18                | 1_18_R1       | 1.18-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.17.1              | 1_17_R1       | 1.17.1-R0.1-SNAPSHOT    |
| 1.17                | 1_17_R1       | 1.17-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.16.5              | 1_16_R3       | 1.16.5-R0.1-SNAPSHOT    |
| 1.16.4              | 1_16_R3       | 1.16.4-R0.1-SNAPSHOT    |
| 1.16.3              | 1_16_R2       | 1.16.3-R0.1-SNAPSHOT    |
| 1.16.2              | 1_16_R2       | 1.16.2-R0.1-SNAPSHOT    |
| 1.16.1              | 1_16_R1       | 1.16.1-R0.1-SNAPSHOT    |
|                     |               |                         |
| 1.15.2              | 1_15_R1       | 1.15.2-R0.1-SNAPSHOT    |
| 1.15.1              | 1_15_R1       | 1.15.1-R0.1-SNAPSHOT    |
| 1.15                | 1_15_R1       | 1.15-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.14.4              | 1_14_R1       | 1.14.4-R0.1-SNAPSHOT    |
| 1.14.3              | 1_14_R1       | 1.14.3-R0.1-SNAPSHOT    |
| 1.14.2              | 1_14_R1       | 1.14.2-R0.1-SNAPSHOT    |
| 1.14                | 1_14_R1       | 1.14-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.13.2              | 1_13_R2       | 1.13.2-R0.1-SNAPSHOT    |
| 1.13.1              | 1_13_R2       | 1.13.1-R0.1-SNAPSHOT    |
| 1.13                | 1_13_R1       | 1.13-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.12.2              | 1_12_R1       | 1.12.2-R0.1-SNAPSHOT    |
| 1.12.1              | 1_12_R1       | 1.12.1-R0.1-SNAPSHOT    |
| 1.12                | 1_12_R1       | 1.12-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.11.2              | 1_11_R1       | 1.11.2-R0.1-SNAPSHOT    |
| 1.11                | 1_11_R1       | 1.11-R0.1-SNAPSHOT      |
|                     |               |                         |
| 1.10.2              | 1_10_R1       | 1.10.2-R0.1-SNAPSHOT    |
|                     |               |                         |
| 1.9.4               | 1_9_R2        | 1.9.4-R0.1-SNAPSHOT     |
| 1.9.2               | 1_9_R1        | 1.9.2-R0.1-SNAPSHOT     |
| 1.9                 | 1_9_R1        | 1.9-R0.1-SNAPSHOT       |
|                     |               |                         |
| 1.8.8               | 1_8_R3        | 1.8.8-R0.1-SNAPSHOT     |
| 1.8.3               | 1_8_R2        | 1.8.3-R0.1-SNAPSHOT     |
| 1.8                 | 1_8_R1        | 1.8-R0.1-SNAPSHOT       |
<!-- versions_end -->
