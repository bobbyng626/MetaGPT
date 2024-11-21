class JockeyTrainerRelationship(Role):
    """
    Represents the relationship between a Jockey and a Trainer, crucial for race outcomes.

    Attributes:
        jockey_name (str): Name of the jockey.
        trainer_name (str): Name of the trainer.
        profile (str): Role profile, default is 'Jockey-Trainer Relationship'.
        goal (str): Goal of the relationship.
        constraints (str): Constraints or limitations for the relationship.
    """

    jockey_name: str = "David"
    trainer_name: str = "Mike"
    profile: str = "Jockey-Trainer Relationship"
    goal: str = "to develop a strategic and effective race plan"
    constraints: str = "communication and strategy alignment"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([CoordinateStrategy, CommunicateEffectively])
        self._watch([RaceStrategy, TrainingFeedback])
        self.rc.react_mode = RoleReactMode.BY_ORDER

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory=True)
