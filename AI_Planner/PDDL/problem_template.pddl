(define (problem template) 

  (:domain ComfyGuest)
  (:objects
    env101 - env
    room101 - room

    lights101 - lights
    blinds101 - blinds
    windows101 - windows

    ac101 - cooling_unit
    heater101 - heating_unit

    air_purifier101 - air_purifier
    ventilator101 - ventilation_unit
  )

  (:init
      (in-room lights101 room101)
      (in-room blinds101 room101)
      (in-room ac101 room101)
      (in-room heater101 room101)
      (in-room air_purifier101 room101)
      (in-room ventilator101 room101)

      (lights-off lights101 room101)
      (blinds-close blinds101 room101)
      (day-time room101)

      (temperature-high room101)
      (air_quality-poor room101)
      (ventilation-on ventilator101 room101)
      (low-humidity room101)
  )

  (:goal (and
      (high-humidity room101)
      (temperature-low room101)
      (air_quality-good room101)
      (high-lux room101)
  ))
)
