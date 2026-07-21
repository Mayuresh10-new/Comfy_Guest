(define (domain ComfyGuest)

  (:requirements :strips :typing :negative-preconditions :disjunctive-preconditions)

  (:types room guest device env - object
    hvac blinds air_purifier lights windows - device
    heating_unit cooling_unit ventilation_unit - hvac
  )

  (:predicates
    (inIdleMode ?room - room)
    (out-temperature-high ?env - env)
    (out-temperature-comfy ?env - env)
    (out-temperature-low ?env - env) 
    (high-lux ?room - room)
    (comfy-lux ?room - room)
    (low-lux ?room - room)
    (lights-on ?lights - lights ?room - room)
    (lights-off ?lights - lights ?room - room)
    (temperature-high ?room - room)
    (temperature-low ?room - room)
    (temperature-comfy ?room - room)
    (cooling-on ?ac - cooling_unit ?room - room)
    (cooling-off ?ac - cooling_unit ?room - room)
    (heating-on ?heater - heating_unit ?room - room)
    (heating-off ?heater - heating_unit ?room - room)
    (blinds-open ?blinds - blinds ?room - room)
    (blinds-close ?blinds - blinds ?room - room)
    (windows-open ?windows - windows ?room - room)
    (windows-close ?windows - windows ?room - room)
    (day-time ?room - room)
    (air_quality-good ?room - room)
    (air_quality-poor ?room - room)
    (air_purifier-on ?air_purifier - air_purifier ?room - room)
    (air_purifier-off ?air_purifier - air_purifier ?room - room)
    (high-humidity ?room - room)
    (low-humidity ?room - room)
    (ventilation-on ?ventilator - ventilation_unit ?room - room)
    (ventilation-off ?ventilator - ventilation_unit ?room - room)
    (in-room ?obj - device ?room - room)
  )

  (:action turn-on-lights-blindsClosed
    :parameters (?room - room ?lights - lights ?blinds - blinds)
    :precondition (and
      (in-room ?lights ?room)
      (in-room ?blinds ?room) 
      (low-lux ?room)
      (lights-off ?lights ?room)
      (blinds-close ?blinds ?room)
      )
    :effect (and 
    (lights-on ?lights ?room) 
    (comfy-lux ?room) 
    (not (lights-off ?lights ?room))
    (not (low-lux ?room))
    (not (high-lux ?room))
    )
  )

  (:action turn-on-lights-blindsOpenDay
    :parameters (?room - room ?lights - lights ?blinds - blinds)
    :precondition (and
      (in-room ?lights ?room)
      (in-room ?blinds ?room) 
      (lights-off ?lights ?room)
      (blinds-open ?blinds ?room)
      (day-time ?room)
      (not (lights-on ?lights ?room))
      (not (blinds-close ?blinds ?room))
      )
    :effect (and 
    (lights-on ?lights ?room) 
    (high-lux ?room) 
    (not (lights-off ?lights ?room))
    (not (low-lux ?room))
    (not (comfy-lux ?room)))
  )

  (:action turn-on-lights-blindsOpenNight
    :parameters (?room - room ?lights - lights ?blinds - blinds)
    :precondition (and 
      (in-room ?lights ?room)
      (in-room ?blinds ?room)
      (lights-off ?lights ?room)
      (blinds-open ?blinds ?room)
      (not (day-time ?room))
      (not (lights-on ?lights ?room))
      (not (blinds-close ?blinds ?room))
    )
    :effect (and 
    (lights-on ?lights ?room) 
    (comfy-lux ?room)
    (not (low-lux ?room))
    (not (high-lux ?room)))
  )


  (:action turn-off-lights-blindsClosed
    :parameters (?room - room ?lights - lights ?blinds - blinds)
    :precondition (and 
    (in-room ?lights ?room)
    (in-room ?blinds ?room)
    (lights-on ?lights ?room)
    (blinds-close ?blinds ?room)
    )
    :effect (and 
    (lights-off ?lights ?room) 
    (low-lux ?room) 
    )
  )

  (:action turn-off-lights-blindsOpenDay
    :parameters (?room - room ?lights - lights ?blinds - blinds)
    :precondition (and 
    (in-room ?lights ?room)
    (in-room ?blinds ?room)
    (day-time ?room)
    (lights-on ?lights ?room)
    (blinds-open ?blinds ?room))
    :effect (and 
    (lights-off ?lights ?room) 
    (comfy-lux ?room) 
    (not (lights-on ?lights ?room))
    (not (low-lux ?room))
    (not (high-lux ?room)))
  )

  (:action turn-off-lights-blindsOpenNight
    :parameters (?room - room ?lights - lights ?blinds - blinds)
    :precondition (and 
    (in-room ?lights ?room)
    (in-room ?blinds ?room)
    (not (day-time ?room))
    (lights-on ?lights ?room)
    (not (lights-off ?lights ?room))
    (blinds-open ?blinds ?room)
    (not (blinds-close ?blinds ?room))
    )
    :effect (and 
    (lights-off ?lights ?room) 
    (low-lux ?room) 
    (not (lights-on ?lights ?room))
    (not (comfy-lux ?room))
    (not (high-lux ?room)))
  )


  (:action close-blinds-lightsOff
    :parameters (?room - room ?blinds - blinds ?lights - lights)
    :precondition (and 
    (in-room ?lights ?room)
    (in-room ?blinds ?room)
    (blinds-open ?blinds ?room)
    (lights-off ?lights ?room) 
    (not (blinds-close ?blinds ?room))
    (not (lights-on ?lights ?room))
    )
    :effect (and 
      (blinds-close ?blinds ?room)
    )
  )

  (:action close-blinds-lightsOn
    :parameters (?room - room ?blinds - blinds ?lights - lights)
    :precondition (and (in-room ?blinds ?room)
     (blinds-open ?blinds ?room) 
     (lights-on ?lights ?room))
    :effect (and 
      (blinds-close ?blinds ?room)
      (comfy-lux ?room)
      (not (blinds-open ?blinds ?room))
      (not (low-lux ?room))
      (not (high-lux ?room))
      )
  )

  (:action open-blinds-lightsOnNight
    :parameters (?room - room ?blinds - blinds)
    :precondition (and 
    (blinds-close ?blinds ?room) 
    (in-room ?blinds ?room)
    (not (day-time ?room)))
    :effect (and 
      (blinds-open ?blinds ?room)
      (comfy-lux ?room)
      (not (blinds-close ?blinds ?room))
      (not (high-lux ?room))
      )
  )

  (:action open-blinds-lightsOffDay
    :parameters (?room - room ?blinds - blinds ?lights - lights)
    :precondition (and 
      (in-room ?blinds ?room)
      (in-room ?lights ?room)
      (day-time ?room)
      (blinds-close ?blinds ?room)
      (not (blinds-open ?blinds ?room))
      (lights-off ?lights ?room)
    )
    :effect (and 
      (blinds-open ?blinds ?room)
      (high-lux ?room)
    )
  )

  (:action open-blinds-lightsOnDay
    :parameters (?room - room ?blinds - blinds ?lights - lights)
    :precondition (and 
      (in-room ?blinds ?room)
      (in-room ?lights ?room)
      (day-time ?room)
      (blinds-close ?blinds ?room)
      (not (blinds-open ?blinds ?room))
      (lights-on ?lights ?room)
      (not (lights-off ?lights ?room))
    )
    :effect (and 
      (blinds-open ?blinds ?room)
    )
  )

  (:action open-windowsHighEnvTemp
    :parameters (?room - room ?windows - windows ?ac - cooling_unit ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?windows ?room)
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      ; (windows-close ?windows ?room)
      (not (windows-open ?windows ?room))
      (cooling-off ?ac ?room)
      (heating-off ?heater ?room)
      (out-temperature-high ?env)
    )
    :effect (and 
      (windows-open ?windows ?room)
      (temperature-high ?room)
    )
  )

  (:action open-windowsComfyEnvTemp
    :parameters (?room - room ?windows - windows ?ac - cooling_unit ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?windows ?room)
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (windows-close ?windows ?room)
      (not (windows-open ?windows ?room))
      (cooling-off ?ac ?room)
      (heating-off ?heater ?room)
      (out-temperature-comfy ?env)
    )
    :effect (and 
      (windows-open ?windows ?room)
      (temperature-high ?room)
    )
  )

  (:action open-windowsLowEnvTemp
    :parameters (?room - room ?windows - windows ?ac - cooling_unit ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?windows ?room)
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (windows-close ?windows ?room)
      (not (windows-open ?windows ?room))
      (cooling-off ?ac ?room)
      (heating-off ?heater ?room)
      (out-temperature-low ?env)
    )
    :effect (and 
      (windows-open ?windows ?room)
      (temperature-low ?room)
    )
  )

  (:action close-windows
    :parameters (?room - room ?windows - windows)
    :precondition (and 
      (in-room ?windows ?room)
      (windows-open ?windows ?room)
      (not (windows-close ?windows ?room))
    )
    :effect (and 
      (windows-close ?windows ?room)
    )
  )

  (:action turn-on-cooling
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?windows - windows)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (or (temperature-high ?room) (temperature-comfy ?room))
      ; (not (cooling-on ?ac ?room))
      ; (heating-off ?heater ?room)
      (windows-close ?windows ?room)
    )
    :effect (and 
    (cooling-on ?ac ?room) 
    (temperature-comfy ?room) 
    (not (cooling-off ?ac ?room)) 
    (heating-off ?heater ?room)
  )
  )
  (:action continue-cooling
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?windows - windows)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (temperature-comfy ?room)
      (cooling-on ?ac ?room)
      (not (cooling-off ?ac ?room))
      (heating-off ?heater ?room)
      (windows-close ?windows ?room)
    )
    :effect (and 
      (temperature-low ?room)
      (not (cooling-off ?ac ?room))
      (heating-off ?heater ?room)
      (not (temperature-high ?room))
      (not (temperature-comfy ?room))
    )
  )

  (:action turn-off-cooling
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (cooling-on ?ac ?room)
      (not (cooling-off ?ac ?room))
    )
    :effect (and 
      (cooling-off ?ac ?room)
      (not (cooling-on ?ac ?room))
    )
  )

  (:action turn-off-coolingHighEnvTemp
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (cooling-on ?ac ?room)
      (not (cooling-off ?ac ?room))
      (out-temperature-high ?env)
    )
    :effect (and 
      (cooling-off ?ac ?room)
      (temperature-high ?room)
    )
  )

  (:action turn-off-coolingComfyEnvTemp
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (cooling-on ?ac ?room)
      (not (cooling-off ?ac ?room))
      (out-temperature-comfy ?env)
    )
    :effect (and 
      (cooling-off ?ac ?room)
      (temperature-high ?room)
    )
  )

  (:action turn-off-coolingLowEnvTemp
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (cooling-on ?ac ?room)
      (not (cooling-off ?ac ?room))
      (out-temperature-low ?env)
    )
    :effect (and 
      (cooling-off ?ac ?room)
      (temperature-comfy ?room)
    )
  )

  (:action turn-on-heating
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?windows - windows)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (or (temperature-low ?room) (temperature-comfy ?room))
      (not (heating-on ?heater ?room))
      (windows-close ?windows ?room)
      (cooling-off ?ac ?room)
    )
    :effect (and 
      (temperature-comfy ?room)
      (heating-on ?heater ?room)
      (not (heating-off ?heater ?room))
      (cooling-off ?ac ?room)
      (not (cooling-on ?ac ?room))
      (not (temperature-low ?room))
      (not (temperature-high ?room))
    )
  )

  (:action continue-heating
    :parameters (?room - room ?ac - cooling_unit ?heater - heating_unit ?windows - windows)
    :precondition (and 
      (in-room ?ac ?room)
      (in-room ?heater ?room)
      (temperature-comfy ?room)
      (heating-on ?heater ?room)
      (windows-close ?windows ?room)
    )
    :effect (and 
      (temperature-high ?room)
      (heating-on ?heater ?room)
      (not (heating-off ?heater ?room))
      (cooling-off ?ac ?room)
      ; (not (temperature-comfy ?room))
      ; (not (temperature-low ?room))
    )
  )

  (:action turn-off-heating
    :parameters (?room - room ?heater - heating_unit ?env - env)
    :precondition (and 
      (in-room ?heater ?room)
      (heating-on ?heater ?room)
      (not (heating-off ?heater ?room))
    )
    :effect (and
      (heating-off ?heater ?room)
      (not (heating-on ?heater ?room))
    )
  )

  (:action turn-off-heatingHighEnvTemp
    :parameters (?room - room ?heater - heating_unit ?env - env ?windows - windows)
    :precondition (and 
      (in-room ?heater ?room)
      (heating-on ?heater ?room)
      (out-temperature-high ?env)
      (not (heating-off ?heater ?room))
      (windows-open ?windows ?room)
    )
    :effect (and
      (heating-off ?heater ?room)
      (temperature-high ?room)
      (not (heating-on ?heater ?room))
    )
  )

  (:action turn-off-heatingComfyEnvTemp
    :parameters (?room - room ?heater - heating_unit ?env - env ?windows - windows)
    :precondition (and 
      (in-room ?heater ?room)
      (heating-on ?heater ?room)
      (out-temperature-comfy ?env)
      (windows-open ?windows ?room)
      (not (heating-off ?heater ?room))
    )
    :effect (and
      (heating-off ?heater ?room)
      (temperature-comfy ?room)
      (not (heating-on ?heater ?room))
    )
  )

  (:action turn-off-heatingLowEnvTemp
    :parameters (?room - room ?heater - heating_unit ?env - env ?windows - windows)
    :precondition (and 
      (in-room ?heater ?room)
      (heating-on ?heater ?room)
      (out-temperature-low ?env)
      (windows-open ?windows ?room)
      (not (heating-off ?heater ?room))
    )
    :effect (and
      (heating-off ?heater ?room)
      (temperature-comfy ?room)
      (not (heating-on ?heater ?room))
    )
  )

  (:action turn-on-airPurifier
      :parameters (?room - room ?air_purifier - air_purifier)
      :precondition (and
        (air_quality-poor ?room)
        ; (air_purifier-off ?air_purifier ?room)
        (in-room ?air_purifier ?room)
      )
      :effect (and 
      (air_purifier-on ?air_purifier ?room) 
      (not (air_purifier-off ?air_purifier ?room))
      (air_quality-good ?room) 
      (not (air_quality-poor ?room)))
  )
  
  (:action turn-off-airPurifier
      :parameters (?room - room ?air_purifier - air_purifier)
      :precondition (and
        (in-room ?air_purifier ?room)
        (not (air_purifier-off ?air_purifier ?room))
        ; (air_purifier-on ?air_purifier ?room)
        (air_quality-good ?room)
       )
      :effect (and 
      (not (air_purifier-on ?air_purifier ?room)) 
      (air_purifier-off ?air_purifier ?room)
      (air_quality-poor ?room)
      (not (air_quality-good ?room))
      )
  )

  (:action turn-on-ventilation
    :parameters (?room - room ?ventilator - ventilation_unit)
    :precondition (and 
      (in-room ?ventilator ?room)
      (high-humidity ?room)
      ; (not (ventilation-on ?ventilator ?room))
      ; (ventilation-off ?ventilator ?room)
    )
    :effect (and 
      (ventilation-on ?ventilator ?room)
      (not (ventilation-off ?ventilator ?room)) 
      (low-humidity ?room)
      (not (high-humidity ?room))
    )
  )  

  (:action turn-off-ventilation
      :parameters (?room - room ?ventilator - ventilation_unit)
      :precondition (and 
        (in-room ?ventilator ?room)
        (low-humidity ?room)
        ; (ventilation-on ?ventilator ?room)
        ; (not (ventilation-off ?ventilator ?room))
      )
      :effect (and 
        (ventilation-off ?ventilator ?room)
        (not (ventilation-on ?ventilator ?room)) 
        (high-humidity ?room)
        (not (low-humidity ?room))
      )
    )

    (:action toIdleMode
      :parameters (?room - room ?lights - lights ?blinds - blinds ?windows - windows ?ac - cooling_unit ?heater - heating_unit ?ventilator - ventilation_unit ?air_purifier - air_purifier)
      :precondition (and 
        (in-room ?lights ?room)
        (in-room ?blinds ?room)
        (in-room ?windows ?room)
        (in-room ?ac ?room)
        (in-room ?heater ?room)
        (in-room ?ventilator ?room)
        (in-room ?air_purifier ?room)
        (not (inIdleMode ?room))
      )
      :effect (and 
      (inIdleMode ?room)
      )
    )
)
