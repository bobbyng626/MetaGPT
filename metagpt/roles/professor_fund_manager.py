#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : product_manager.py
@Modified By: mashenquan, 2023/11/27. Add `PrepareDocuments` action according to Section 2.2.3.5.1 of RFC 135.
"""


from metagpt.actions import UserRequirement, WritePRD
from metagpt.actions.prepare_documents import PrepareDocuments
from metagpt.roles.role import Role, RoleReactMode
from metagpt.utils.common import any_to_name
class FundManager(Role):
    """
    Represents a Fund Manager role responsible for placing bets on horse races.

    Attributes:
        name (str): Name of the Fund Manager.
        profile (str): Role profile, default is 'Fund Manager'.
        goal (str): Goal of the Fund Manager.
        constraints (str): Constraints or limitations for the Fund Manager.
    """

    name: str = "Sarah"
    profile: str = "Fund Manager"
    goal: str = "to place informed bets on horse races to maximize winnings"
    constraints: str = "limited by knowledge, budget, and betting regulations"
    todo_action: str = "research horses, trainers, and jockeys before placing bets"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_actions([ResearchHorses, AnalyzeOdds])
        self._watch([HorsePerformance, BettingOdds])
        self.rc.react_mode = RoleReactMode.BY_ORDER
        self.todo_action = any_to_name(AnalyzeOdds)

    async def _observe(self, ignore_memory=False) -> int:
        return await super()._observe(ignore_memory=True)
