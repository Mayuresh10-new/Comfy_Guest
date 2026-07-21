import subprocess

class PlannerRunner:

    def run(self):

        result = subprocess.run(
            [
                "./run.sh",
                "HSP",
                "ComfyGuest/domain_test.pddl",
                "ComfyGuest/current_problem.pddl"
            ],
            cwd="/Users/yusuf/AI_Planning/scripts",
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError("Planner failed.")

        return result.stdout
