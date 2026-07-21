from fact_generator import generate_predicates, generate_static_predicates
from goalManager import get_goal

problem_template = "/Users/yusuf/AI_Planning/domains/ComfyGuest/template.pddl"
output_path = "/Users/yusuf/AI_Planning/domains/ComfyGuest/current_problem.pddl"

with open(problem_template, "r") as file:
    template = file.read()

def generate_static_init(room, device):
    predicates = generate_static_predicates(room, device)
    init_text = "\n".join(predicates)
    return init_text

def generate_init(room, device, env):
    predicates = generate_predicates(room, device, env)
    init_text = "\n".join(predicates)
    return init_text

def generate_goal(room, device, env):
    goals = get_goal(room, device, env)
    goal_text = "\n".join(goals)
    return goal_text

def generate_problem(room, device, env):
    static_init_text = generate_static_init(room, device)
    init_text = generate_init(room, device, env)
    goal_text = generate_goal(room, device, env)
    problem = f"""(define (problem room{room.number})

    (:domain ComfyGuest)

    (:objects
    env{room.number} - env
    room{room.number} - room
    lights{room.number} - lights
    blinds{room.number} - blinds
    windows{room.number} - windows
    ac{room.number} - cooling_unit
    heater{room.number} - heating_unit
    air_purifier{room.number} - air_purifier
    ventilator{room.number} - ventilation_unit)
    
    (:init
    {static_init_text}
    {init_text})
    
    (:goal
    (and
    {goal_text}))
    )
    """

    with open(output_path, "w") as file:

        file.write(problem)
        print("Problem generated")

    return problem
