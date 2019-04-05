import subprocess
from collections import namedtuple
from typing import Optional

Coordinates = namedtuple("coordinates", ("x", "y"))
Size = namedtuple("size", ("width", "height"))


def _execute(arguments: str) -> Optional[str]:
    command = "xdotool " + arguments

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    result = output.decode("utf-8")
    return result


def search(name: str, single_result=True) -> Optional[str]:
    command = f"search --onlyvisible --name {name}"
    result = _execute(command)

    if not result:
        return None

    ids = [id for id in result.split("\n") if len(id)]

    if single_result:
        return ids[-1]

    result = str(int(result)) if result else None

    return result


def _is_percentage(value) -> bool:
    return value.endswith("%") if isinstance(value, str) else False


def _convert_percentage(value: str) -> float:
    percentage = value[:-1]
    result = int(percentage) / 100

    return result


def _coord_to_position(coordinates: Coordinates) -> Coordinates:
    x = coordinates.x
    y = coordinates.y

    if _is_percentage(coordinates.x):
        x = display_size().width * _convert_percentage(coordinates.x)

    if _is_percentage(coordinates.y):
        y = display_size().height * _convert_percentage(coordinates.y)

    result = Coordinates(x=x, y=y)

    return result


def display_size() -> Size:
    command = "getdisplaygeometry"

    dimensions = _execute(command).split()
    result = Size(width=int(dimensions[0]), height=int(dimensions[1]))

    return result


def move(name: str = None, window_id: str = None, coordinates: Coordinates = None):
    if name:
        window_id = search(name=name)

    if not window_id or not coordinates:
        raise ValueError

    coordinates = _coord_to_position(coordinates=coordinates)

    command = f"windowmove {window_id} {coordinates.x} {coordinates.y}"
    result = _execute(command)

    return result


def resize(name: str = None, window_id: str = None, size: Size = None):
    if name:
        window_id = search(name=name)

    if not window_id or not size:
        raise ValueError

    command = f"windowsize {window_id} {size.width} {size.height}"
    result = _execute(command)

    return result


def position(
        name: str = None,
        window_id: str = None,
        coordinates: Coordinates = None,
        size: Size = None,
):
    if name:
        window_id = search(name=name)

    if not window_id or not coordinates or not size:
        raise ValueError

    move(window_id=window_id, coordinates=coordinates)
    resize(window_id=window_id, size=size)


def to_desktop(name: str = None, window_id: str = None, desktop: int = 0):
    if name:
        window_id = search(name=name)

    if not window_id:
        raise ValueError

    command = f"set_desktop_for_window {window_id} {desktop}"
    result = _execute(command)

    return result


def execute(parameters=None):
    command = f"exec {parameters} &"
    result = _execute(command)

    return result


def set_desktop(desktop=0):
    command = f"set_desktop {desktop}"
    result = _execute(command)

    return result
