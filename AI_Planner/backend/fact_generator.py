def generate_predicates(room, device, env):

    predicates = []

    if room.temperature == 'high':
        predicates.append(f'(temperature-high room{room.number})')
    elif room.temperature == 'comfy':
        predicates.append(f'(temperature-comfy room{room.number})')
    else:
        predicates.append(f'(temperature-low room{room.number})')

    if env.temperature == 'high':
        predicates.append(f'(out-temperature-high env{room.number})')
    elif env.temperature == 'comfy':
        predicates.append(f'(out-temperature-comfy env{room.number})')
    else:
        predicates.append(f'(out-temperature-low env{room.number})')

    if room.lux == 'high':
        predicates.append(f'(high-lux room{room.number})')
    elif room.lux == 'comfy':
        predicates.append(f'(comfy-lux room{room.number})')
    else:
        predicates.append(f'(low-lux room{room.number})')

    if room.daytime:
        predicates.append(f'(day-time room{room.number})')

    if room.air_quality == 'good':
        predicates.append(f'(air_quality-good room{room.number})')
    else:
        predicates.append(f'(air_quality-poor room{room.number})')

    if room.humidity == 'high':
        predicates.append(f'(high-humidity room{room.number})')
    else:
        predicates.append(f'(low-humidity room{room.number})')

    if device.lights == 1:
        predicates.append(f'(lights-on lights{device.number} room{room.number})')
    else:
        predicates.append(f'(lights-off lights{device.number} room{room.number})')

    if device.blinds == 1:
        predicates.append(f'(blinds-open blinds{device.number} room{room.number})')
    else:
        predicates.append(f'(blinds-close blinds{device.number} room{room.number})')

    if device.windows == 1:
        predicates.append(f'(windows-open windows{device.number} room{room.number})')
    else:
        predicates.append(f'(windows-close windows{device.number} room{room.number})')

    if device.ac == 1:
        predicates.append(f'(cooling-on ac{device.number} room{room.number})')
    else:
        predicates.append(f'(cooling-off ac{device.number} room{room.number})')

    if device.heater == 1:
        predicates.append(f'(heating-on heater{device.number} room{room.number})')
    else:
        predicates.append(f'(heating-off heater{device.number} room{room.number})')

    if device.air_purifier == 1:
        predicates.append(f"(air_purifier-on air_purifier{device.number} room{room.number})")
    else:
        predicates.append(f"(air_purifier-off air_purifier{device.number} room{room.number})")

    if device.ventilator == 1:
        predicates.append(f"(ventilation-on ventilator{device.number} room{room.number})")
    else:
        predicates.append(f"(ventilation-off ventilator{device.number} room{room.number})")

    return predicates

def generate_static_predicates(room, device):

    statice_predicates = []

    statice_predicates.append(f"(in-room lights{device.number} room{room.number})")
    statice_predicates.append(f"(in-room blinds{device.number} room{room.number})")
    statice_predicates.append(f"(in-room windows{device.number} room{room.number})")
    statice_predicates.append(f"(in-room ac{device.number} room{room.number})")
    statice_predicates.append(f"(in-room heater{device.number} room{room.number})")
    statice_predicates.append(f"(in-room air_purifier{device.number} room{room.number})")
    statice_predicates.append(f"(in-room ventilator{device.number} room{room.number})")

    return statice_predicates
