from metagpt.actions import Action, ActionOutput
from metagpt.schema import Document
from metagpt.utils.common import fetch_data

class MonitorHorsePerformance(Action):
    """
    Monitor the performance of racehorses by fetching and analyzing their recent race data and training feedback.

    Attributes:
        name (str): Name of the action.
    """

    async def run(self, horse_id, *args, **kwargs) -> ActionOutput:
        recent_races = await fetch_data(f"https://api.racing.com/horse/{horse_id}/recent_races")
        training_feedback = await fetch_data(f"https://api.racing.com/horse/{horse_id}/training_feedback")
        performance_analysis = self._analyze_performance(recent_races, training_feedback)
        performance_doc = Document(title="Performance Analysis", content=performance_analysis)
        return ActionOutput(documents=[performance_doc])

    def _analyze_performance(self, recent_races, training_feedback):
        analysis = {
            "recent_races": recent_races,
            "training_feedback": training_feedback,
            "improvement_suggestions": "Increase endurance training"
        }
        return analysis
