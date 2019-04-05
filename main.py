import json

import xdtool

with open("config.json", "r") as config_file:
    configuration = json.load(config_file)

for application in configuration["applications"]:
    window_id = xdtool.search(application["name"])

    if not window_id:
        continue

    coordinates_config = application.get("coordinates", {})
    size_config = application.get("size", {})

    coordinates = xdtool.Coordinates(
        x=coordinates_config.get("x", 0), y=coordinates_config.get("y", 0)
    )
    size = xdtool.Size(
        width=size_config.get("width", "100%"), height=size_config.get("height", "100%")
    )

    xdtool.position(window_id=window_id, coordinates=coordinates, size=size)
    xdtool.to_desktop(window_id=window_id, desktop=application.get("desktop", 0))

desktop = configuration.get("desktop", 0)
xdtool.set_desktop(desktop=desktop)
