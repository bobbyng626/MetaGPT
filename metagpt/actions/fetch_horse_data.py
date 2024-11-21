from metagpt.actions import Action, ActionOutput
from metagpt.schema import Document
from metagpt.utils.common import fetch_data

class FetchHorseData(Action):
    """
    Fetch detailed data about the horse including current health status and upcoming races.

    Attributes:
        name (str): Name of the action.
    """

    async def run(self, horse_id, *args, **kwargs) -> ActionOutput:
        horse_data = await fetch_data(f"https://api.racing.com/horse/{horse_id}/details")
        health_data = horse_data['health']
        upcoming_races = horse_data['upcoming_races']
        horse_info = {
            "health": health_data,
            "upcoming_races": upcoming_races
        }
        horse_doc = Document(title="Horse Data", content=horse_info)
        return ActionOutput(documents=[horse_doc])
