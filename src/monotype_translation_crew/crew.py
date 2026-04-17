import os
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, before_kickoff, crew, task
from crewai_tools import ScrapeWebsiteTool
from datetime import datetime

from .tools import (
    read_brand_guidelines,
    read_excel_for_translation,
    read_reviewed_translations,
    write_translations_to_excel,
    write_reviewed_translations_to_excel,
    read_brand_context_cache,
    save_brand_context_cache,
)


@CrewBase
class MonotypeTranslationCrew:
    """Monotype Translation Crew — translates UI strings from English into
    French, German, Brazilian Portuguese, Japanese, and Latin American Spanish."""

    agents: List[BaseAgent]
    tasks: List[Task]

    # ------------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------------

    @agent
    def brand_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["brand_analyst"],  # type: ignore[index]
            verbose=True,
            tools=[
                read_brand_context_cache,
                read_brand_guidelines,
                ScrapeWebsiteTool(website_url="https://www.myfonts.com/"),
                ScrapeWebsiteTool(website_url="https://www.myfonts.com/collections/"),
                save_brand_context_cache,
            ],
            allow_delegation=False,
        )

    @agent
    def translator(self) -> Agent:
        return Agent(
            config=self.agents_config["translator"],  # type: ignore[index]
            verbose=True,
            tools=[read_excel_for_translation],
            allow_delegation=False,
        )

    @agent
    def translation_reviewer(self) -> Agent:
        # No tools — works purely from context passed by prior tasks.
        # This prevents re-reading stale Excel state mid-crew.
        return Agent(
            config=self.agents_config["translation_reviewer"],  # type: ignore[index]
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def production_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["production_manager"],  # type: ignore[index]
            verbose=True,
            tools=[write_reviewed_translations_to_excel],
            allow_delegation=False,
        )

    # ------------------------------------------------------------------
    # Lifecycle hooks
    # ------------------------------------------------------------------

    @before_kickoff
    def setup(self, inputs=None):
        os.makedirs(os.path.join(os.getcwd(), "outputs"), exist_ok=True)
        return inputs

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    @task
    def brand_context_task(self) -> Task:
        return Task(
            config=self.tasks_config["brand_context_task"],  # type: ignore[index]
        )

    @task
    def translation_task(self) -> Task:
        return Task(
            config=self.tasks_config["translation_task"],  # type: ignore[index]
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_task"],  # type: ignore[index]
            output_file=os.path.join("outputs", "reviewed_translations.json"),
        )

    @task
    def production_task(self) -> Task:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = os.path.join("outputs", f"translation_report-{timestamp}.md")
        return Task(
            config=self.tasks_config["production_task"],  # type: ignore[index]
            output_file=report_path,
        )

    # ------------------------------------------------------------------
    # Crew
    # ------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
