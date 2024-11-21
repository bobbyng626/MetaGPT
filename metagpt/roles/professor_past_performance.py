class PastPerformance(Role):
    """
    Represents the analysis of a horse's past performance.

    Attributes:
        name (str): Name of the past performance role.
        profile (str): Role profile, default is 'Past Performance'.
        goal (str): Goal of the past performance analysis.
        constraints (str): Constraints or limitations for the analysis.
    """

    name: str = "Performance Analysis"
    profile: str = "Past Performance"
    goal: str = "to provide insights based on previous races"
    constraints: str = "accuracy of historical data and relevance to current conditions"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([ReviewRaceHistory, ComparePerformanceMetrics])
        self._watch([RaceResults, PerformanceMetrics])
        self.rc.react_mode = RoleReactMode.BY_ORDER

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory=True)
