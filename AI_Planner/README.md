# ComfyGuest – AI Planning Module

ComfyGuest is an AI-powered planning system designed for a Smart Hotel Welcome System. This repository contains the intelligent decision-making component responsible for generating action plans that prepare a hotel room according to guest preferences and real-time environmental conditions.

The planner combines **Artificial Intelligence Planning** with **IoT sensor data** to determine the most appropriate sequence of actions for devices such as lights, blinds, HVAC, ventilation, and air purification systems. Instead of relying on fixed if-else rules, ComfyGuest reasons about the current state of the room and automatically generates a plan that achieves the desired comfort and sustainability goals.

## Features

- AI Planning using **PDDL (Planning Domain Definition Language)**
- Dynamic world-state generation from IoT sensor data
- Goal selection based on room conditions and operational modes
- Automatic plan generation using the **HSP Planner (PDDL4J)**
- Plan parsing and execution interface
- Modular Python backend for easy integration with IoT platforms
- Extensible domain model supporting additional smart devices and planning goals

## Workflow

1. Receive sensor data from the IoT system.
2. Convert sensor readings into PDDL facts.
3. Select the appropriate planning goal.
4. Generate an optimal action plan using the HSP planner.
5. Parse the generated plan.
6. Send actions to the execution layer for device control.

## Technologies

- Python
- PDDL
- PDDL4J
- HSP Planner
- MQTT
- IoT Sensors

## Repository Structure

```text
backend/
├── actionExecutor.py
├── fact_generator.py
├── goalManager.py
├── plannerInterface.py
├── planParser.py
└── stateParser.py

models/
└── models.py

pddl/
├── domain.pddl
└── problem.pddl

scripts/
└── run.sh
```

## Objective

The goal of ComfyGuest is to demonstrate how **Classical AI Planning** can be integrated with **IoT systems** to create an intelligent, context-aware hotel automation solution. By reasoning about the current room state and guest requirements, the planner generates efficient action sequences that enhance guest comfort while supporting sustainable and energy-efficient operation.
