class Horse(Role):
    """
    Represents a Horse role in a race, focusing on its analysis for betting purposes.

    Attributes:
        name (str): Name of the horse.
        profile (str): Role profile, default is 'Horse'.
        goal (str): Goal of the horse.
        constraints (str): Constraints or limitations for the horse.
    """

    name: str = "Thunderbolt"
    profile: str = "Racehorse"
    goal: str = "to perform exceptionally in races"
    constraints: str = "limited by physical health and training"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([AnalyzePerformance, CheckHealth])
        self._watch([PastPerformance, CurrentHealth])
        self.rc.react_mode = RoleReactMode.BY_ORDER

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory=True)
