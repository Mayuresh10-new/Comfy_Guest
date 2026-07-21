import json
from backend.models import RoomState


class StateParser:

    def parse(self, payload):

        data = json.loads(payload)

        temperature = data["temperature"]
        humidity = data["humidity"]

        if temperature < 20:
            comfort = "cold"
        elif temperature > 25:
            comfort = "hot"
        else:
            comfort = "comfortable"

        if data["occupied"]:
            occupancy = "occupied"
        else:
            occupancy = "vacant"

        return RoomState(
            temperature=temperature,
            humidity=humidity,

            motion=data["motion"],
            occupied=data["occupied"],

            light=data["light"],

            manual_mode=data["manual_mode"],
            manual_relay=data["manual_relay"],

            comfort_state=comfort,
            occupancy_state=occupancy
        )