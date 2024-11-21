class RunningPositions(Role):
    """
    Represents the analysis of running positions during a race.

    Attributes:
        name (str): Name of the analysis role.
        profile (str): Role profile, default is 'Running Positions'.
        goal (str): Goal of the running positions analysis.
        constraints (str): Constraints or limitations for the analysis.
    """

    name: str = "Position Analysis"
    profile: str = "Running Positions"
    goal: str = "to analyze horses' positions throughout the race"
    constraints: str = "dependent on race conditions and competitors"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([AnalyzeStartingPosition, TrackPositionChanges])
        self._watch([StartingPositions, PositionChanges])
        self.rc.react_mode = RoleReactMode.BY_ORDER

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory=True)
