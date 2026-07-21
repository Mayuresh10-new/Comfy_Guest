def get_mode(room, device, env):

    if room.checked_in == 0 or room.occupied == 0:
        return "idle"

    if room.manual_mode == 1:
        return "manual"

    if (
        room.checked_in == 1
    ):
        return "prepare"

    if room.occupied == 1:
        return "comfort"

    return "idle"


def get_goal(room, device, env):

    mode = get_mode(room, device, env)
    print(f"Planning mode: {mode}")

    room_id = f"room{room.number}"
    goals = []

    if mode == "manual":
        return []

    if mode == "idle":
        return [f"(inIdleMode {room_id})"]

    if mode == "prepare":

        if room.temperature != "comfy":
            goals.append(f"(temperature-comfy {room_id})")

        if room.lux != "comfy":
            goals.append(f"(comfy-lux {room_id})")

    elif mode == "comfort":

        if room.daytime == 1:

            if room.temperature != "comfy":
                goals.append(f"(temperature-comfy {room_id})")

        else:

            if room.temperature != "low":
                goals.append(f"(temperature-low {room_id})")

    if room.occupied:
        goals.append(f"(comfy-lux {room_id})")
    else:
        goals.append(f"(low-lux {room_id})")

    if room.occupied and room.lux == "high":
        goals.remove(f"(comfy-lux {room_id})")
        goals.append(f"(low-lux {room_id})")

    # if room.lux == "high":
    #     goals.append(f"(low-lux {room_id})")
    # else:
    #     goals.append(f"(comfy-lux {room_id})")

    if room.humidity == "high":
        goals.append(f"(low-humidity {room_id})")
    else:
        goals.append(f"(high-humidity {room_id})")

    if room.air_quality != "good":
        goals.append(f"(air_quality-good {room_id})")

    return goals