from metagpt.actions import Action, ActionOutput
from metagpt.schema import Document, Message
from metagpt.roles import Role
from metagpt.utils.common import fetch_data
from metagpt.utils.file_repository import save_document

class Trainer(Role):
    """
    Represents a Trainer role responsible for training the racehorses.

    Attributes:
        name (str): Name of the trainer.
        profile (str): Role profile, default is 'Trainer'.
        goal (str): Goal of the trainer.
        constraints (str): Constraints or limitations for the trainer.
    """

    name: str = "Mike"
    profile: str = "Trainer"
    goal: str = "to train racehorses to peak physical condition for races"
    constraints: str = "limited by the horse's physical capabilities and training facilities"
    todo_action: str = "develop and implement effective training routines"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([DevelopTrainingRoutine, MonitorHorsePerformance, FetchHorseData])
        self._watch([TrainingRoutine, HorsePerformance, HorseHealth])
        self.rc.react_mode = RoleReactMode.BY_ORDER
        self.todo_action = any_to_name(MonitorHorsePerformance)

    async def _develop_training_routine(self, horse_id) -> None:
        action = DevelopTrainingRoutine()
        output = await action.run(horse_id)
        await save_document(output.documents[0])

    async def _monitor_horse_performance(self, horse_id) -> None:
        action = MonitorHorsePerformance()
        output = await action.run(horse_id)
        await save_document(output.documents[0])

    async def _fetch_horse_data(self, horse_id) -> None:
        action = FetchHorseData()
        output = await action.run(horse_id)
        await save_document(output.documents[0])

    async def _act(self) -> Message:
        horse_id = self.context.get("horse_id")
        await self._develop_training_routine(horse_id)
        await self._monitor_horse_performance(horse_id)
        await self._fetch_horse_data(horse_id)

        return Message(
            content=f"Training routine and performance monitoring for horse {horse_id} completed.",
            role=self.profile,
            cause_by=self.todo_action,
            sent_from=self.profile,
            send_to=MESSAGE_ROUTE_TO_NONE,
        )

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory=True)
