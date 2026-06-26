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
    read_docx_for_translation,
    write_translations_to_docx,
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
            max_iter=8,
            max_execution_time=720,
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
            max_iter=5,
            max_execution_time=600,
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
            max_iter=3,
            max_execution_time=300,
            allow_delegation=False,
        )

    @agent
    def production_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["production_manager"],  # type: ignore[index]
            verbose=True,
            max_iter=3,
            max_execution_time=300,
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
        config = self.tasks_config["translation_task"]  # type: ignore[index]
        override = getattr(self, "_translation_desc_override", None)
        if override:
            config = dict(config)
            config["description"] = override
        return Task(config=config)

    @task
    def review_task(self) -> Task:
        config = self.tasks_config["review_task"]  # type: ignore[index]
        override = getattr(self, "_review_desc_override", None)
        if override:
            config = dict(config)
            config["description"] = override
        return Task(
            config=config,
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


# ---------------------------------------------------------------------------
# Docx Translation Crew — translates Word documents into selected languages
# ---------------------------------------------------------------------------

class DocxTranslationCrew:
    """Translates Word documents (.docx) into one or more target languages.

    Intentionally does NOT use @CrewBase — loads config files via Path(__file__)
    so discovery never depends on the working directory.
    """

    def __init__(self):
        import yaml
        from pathlib import Path
        _cfg = Path(__file__).parent / "config"
        self._agents_cfg = yaml.safe_load((_cfg / "agents.yaml").read_text())
        self._tasks_cfg  = yaml.safe_load((_cfg / "docx_tasks.yaml").read_text())
        os.makedirs(os.path.join(os.getcwd(), "outputs"), exist_ok=True)

    # ------------------------------------------------------------------
    # Agent factories — single definition, reused across all crew modes
    # ------------------------------------------------------------------

    def _make_brand_analyst(self) -> Agent:
        return Agent(
            config=self._agents_cfg["brand_analyst"],
            verbose=True,
            max_iter=8,
            max_execution_time=720,
            tools=[
                read_brand_context_cache,
                read_brand_guidelines,
                ScrapeWebsiteTool(website_url="https://www.myfonts.com/"),
                ScrapeWebsiteTool(website_url="https://www.myfonts.com/collections/"),
                save_brand_context_cache,
            ],
            allow_delegation=False,
        )

    def _make_prod_manager(self) -> Agent:
        return Agent(
            config=self._agents_cfg["production_manager"],
            verbose=True,
            max_iter=3,
            max_execution_time=300,
            tools=[write_translations_to_docx],
            allow_delegation=False,
        )

    def crew(self) -> Crew:
        brand_analyst = self._make_brand_analyst()
        translator = Agent(
            config=self._agents_cfg["translator"],
            verbose=True,
            max_iter=5,
            max_execution_time=600,
            tools=[read_docx_for_translation],
            allow_delegation=False,
        )
        reviewer = Agent(
            config=self._agents_cfg["translation_reviewer"],
            verbose=True,
            max_iter=3,
            max_execution_time=300,
            allow_delegation=False,
        )
        prod_manager = self._make_prod_manager()

        brand_task = Task(
            description=self._tasks_cfg["brand_context_task"]["description"],
            expected_output=self._tasks_cfg["brand_context_task"]["expected_output"],
            agent=brand_analyst,
        )
        trans_task = Task(
            description=self._tasks_cfg["docx_translation_task"]["description"],
            expected_output=self._tasks_cfg["docx_translation_task"]["expected_output"],
            agent=translator,
            context=[brand_task],
        )
        review_task = Task(
            description=self._tasks_cfg["docx_review_task"]["description"],
            expected_output=self._tasks_cfg["docx_review_task"]["expected_output"],
            agent=reviewer,
            context=[brand_task, trans_task],
            output_file=os.path.join("outputs", "reviewed_docx_translations.json"),
        )
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        prod_task = Task(
            description=self._tasks_cfg["docx_production_task"]["description"],
            expected_output=self._tasks_cfg["docx_production_task"]["expected_output"],
            agent=prod_manager,
            context=[review_task],
            output_file=os.path.join("outputs", f"docx_report-{timestamp}.md"),
        )

        return Crew(
            agents=[brand_analyst, translator, reviewer, prod_manager],
            tasks=[brand_task, trans_task, review_task, prod_task],
            process=Process.sequential,
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Batch-mode helpers (called by api._run_docx_job_batched)
    # ------------------------------------------------------------------

    def _run_brand_context_only(self, knowledge_dir: str):
        """Run just the brand_analyst task so the brand context cache is populated."""
        brand_analyst = self._make_brand_analyst()
        brand_task = Task(
            description=self._tasks_cfg["brand_context_task"]["description"],
            expected_output=self._tasks_cfg["brand_context_task"]["expected_output"],
            agent=brand_analyst,
        )
        return Crew(
            agents=[brand_analyst],
            tasks=[brand_task],
            process=Process.sequential,
            verbose=True,
        ).kickoff(inputs={"knowledge_dir": knowledge_dir})

    def _run_production_only(self, docx_path: str):
        """Run just the production_manager task to write docx files from the merged JSON."""
        prod_manager = self._make_prod_manager()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        prod_task = Task(
            description=self._tasks_cfg["docx_production_task"]["description"],
            expected_output=self._tasks_cfg["docx_production_task"]["expected_output"],
            agent=prod_manager,
            output_file=os.path.join("outputs", f"docx_report-{timestamp}.md"),
        )
        return Crew(
            agents=[prod_manager],
            tasks=[prod_task],
            process=Process.sequential,
            verbose=True,
        ).kickoff(inputs={"docx_path": docx_path})
