# NMS Versions [![Update NMS Versions](https://github.com/Rapha149/NMSVersions/actions/workflows/update.yml/badge.svg)](https://github.com/Rapha149/NMSVersions/actions/workflows/update.yml)

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
            // NMS Version is not yet available in the json file, see the updates section
        }
    }
} catch (IOException e) {
    // Handle exception
}
```

## Updates

The file is updated every 4 hours.  
But the NMS versions are parsed from the NMS repository at [repo.codemc.io](https://repo.codemc.io/#browse/browse:nms:org%2Fspigotmc%2Fspigot) which means that that repository first has to update before the file can get updated.

## Versions

<!-- versions_start --><!-- versions_end -->