import re

class PlanParser:

    ACTION_MAP = {
        "turn-on-lights-blindsclosed": "turn-on-lights",
        "turn-on-lights-blindsopenday": "turn-on-lights",
        "turn-on-lights-blindsopennight": "turn-on-lights",
        "turn-off-lights-blindsclosed": "turn-off-lights",
        "turn-off-lights-blindsopenday": "turn-off-lights",
        "turn-off-lights-blindsopennight": "turn-off-lights",
        "close-blinds-lightsoff": "close-blinds",
        "close-blinds-lightson": "close-blinds",
        "open-blinds-lightsonnight": "open-blinds",
        "open-blinds-lightsoffday": "open-blinds",
        "open-blinds-lightsonday": "open-blinds",
        "open-windowshighenvtemp": "open-windows",
        "open-windowscomfyenvtemp": "open-windows",
        "open-windowslowenvtemp": "open-windows",
        "close-windows": "close-windows",
        "turn-off-coolinghighenvtemp": "turn-off-cooling",
        "turn-off-coolingcomfyenvtemp": "turn-off-cooling",
        "turn-off-coolinglowenvtemp": "turn-off-cooling",
        "turn-off-heatinghighenvtemp": "turn-off-heating",
        "turn-off-heatingcomfyenvtemp": "turn-off-heating",
        "turn-off-heatinglowenvtemp": "turn-off-heating",
    }

    def parse(self, planner_output):

        plan = []

        for line in planner_output.splitlines():

            line = line.strip()

            if re.match(r'^\d+:', line):
                match = re.search(r'\((.*?)\)', line)
                if match:
                    plan.append(match.group(1).strip())

        return plan

    def extract_actions(self, plan):

        actions = []
        params = []

        if len(plan) == 0:
            plan = ["No Plan Found!"]
        else:
            for action in plan:
                action = action.split()
                if action[0] in self.ACTION_MAP:
                    action[0] = self.ACTION_MAP[action[0]]
                actions.append(action[0])
                params.append(action[1])

            for index in range(0, len(actions)):
                action = f'''{actions[index]} in {params[index]}'''
                plan[index] = action

        return plan

    def printPlan(self, plan):

        for action in plan:
            print(action)

