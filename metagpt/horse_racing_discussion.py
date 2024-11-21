#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from pathlib import Path

import agentops
import typer

from metagpt.const import CONFIG_ROOT
from metagpt.utils.project_repo import ProjectRepo

app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)


def generate_repo(
    n_round=5,
    project_name="",
    inc=False,
    project_path="",
    reqa_file="",
    recover_path=None,
) -> ProjectRepo:
    """Run the Discussion logic. Can be called from CLI or other Python scripts."""
    from metagpt.config2 import config
    from metagpt.context import Context
    from metagpt.roles import (
        Trainer,
        PastPerformance
    )
    from metagpt.team import Team

    if config.agentops_api_key != "":
        agentops.init(config.agentops_api_key, tags=["horse_racing_discussion"])

    config.update_via_cli(project_path, project_name, inc, reqa_file)
    ctx = Context(config=config)

    if not recover_path:
        company = Team(context=ctx)
        company.hire(
            [
                Trainer(),
                PastPerformance(),
            ]
        )
    else:
        stg_path = Path(recover_path)
        if not stg_path.exists() or not str(stg_path).endswith("team"):
            raise FileNotFoundError(f"{recover_path} not exists or not endswith `team`")

        company = Team.deserialize(stg_path=stg_path, context=ctx)

    asyncio.run(company.run(n_round=n_round))

    if config.agentops_api_key != "":
        agentops.end_session("Success")

    return ctx.repo


@app.command("", help="Give an insight of the horse race.")
def startup(
    idea: str = typer.Argument(None, help="Your hypothesis of a horse race idea, such as 'Will Horse Lucky 7 able to win in the current race?'"),
    n_round: int = typer.Option(default=5, help="Number of rounds for the simulation."),
    project_name: str = typer.Option(default="", help="Unique project name, such as 'lucky_7_win'."),
    inc: bool = typer.Option(default=False, help="Incremental mode. Use it to coop with existing repo."),
    project_path: str = typer.Option(
        default="",
        help="Specify the directory path of the old version project to fulfill the incremental requirements.",
    ),
    reqa_file: str = typer.Option(
        default="", help="Specify the source file name for rewriting the quality assurance code."
    ),
    recover_path: str = typer.Option(default=None, help="recover the project from existing serialized storage"),
    init_config: bool = typer.Option(default=False, help="Initialize the configuration file for MetaGPT."),
):
    """Run a startup. Be a boss."""
    if init_config:
        copy_config_to()
        return

    if idea is None:
        typer.echo("Missing argument 'IDEA'. Run 'metagpt --help' for more information.")
        raise typer.Exit()

    return generate_repo(
        n_round,
        project_name,
        inc,
        project_path,
        reqa_file,
        recover_path,
    )


DEFAULT_CONFIG = """# Full Example: https://github.com/geekan/MetaGPT/blob/main/config/config2.example.yaml
# Reflected Code: https://github.com/geekan/MetaGPT/blob/main/metagpt/config2.py
# Config Docs: https://docs.deepwisdom.ai/main/en/guide/get_started/configuration.html
llm:
  api_type: "openai"  # or azure / ollama / groq etc.
  model: "gpt-4-turbo"  # or gpt-3.5-turbo
  base_url: "https://api.openai.com/v1"  # or forward url / other llm url
  api_key: "YOUR_API_KEY"
"""


def copy_config_to():
    """Initialize the configuration file for MetaGPT."""
    target_path = CONFIG_ROOT / "config2.yaml"

    # 创建目标目录（如果不存在）
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 如果目标文件已经存在，则重命名为 .bak
    if target_path.exists():
        backup_path = target_path.with_suffix(".bak")
        target_path.rename(backup_path)
        print(f"Existing configuration file backed up at {backup_path}")

    # 复制文件
    target_path.write_text(DEFAULT_CONFIG, encoding="utf-8")
    print(f"Configuration file initialized at {target_path}")


if __name__ == "__main__":
    app()
