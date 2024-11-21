from metagpt.actions import Action, ActionOutput
from metagpt.schema import Document
from metagpt.utils.common import fetch_data

class DevelopTrainingRoutine(Action):
    """
    Develop a training routine for racehorses based on their health, past performance, and race schedules.

    Attributes:
        name (str): Name of the action.
    """

    async def run(self, horse_id, *args, **kwargs) -> ActionOutput:
        horse_details = await fetch_data(f"https://api.racing.com/horse/{horse_id}")
        health_data = horse_details['health']
        performance_data = horse_details['performance']
        training_routine = self._create_training_routine(health_data, performance_data)
        routine_doc = Document(title="Training Routine", content=training_routine)
        return ActionOutput(documents=[routine_doc])

    def _create_training_routine(self, health_data, performance_data):
        routine = {
            "warmup": "15 mins trot",
            "exercise": "30 mins gallop",
            "cooldown": "10 mins walk",
            "health_notes": health_data,
            "performance_notes": performance_data
        }
        return routine
