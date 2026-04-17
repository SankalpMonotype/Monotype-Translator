#!/usr/bin/env python
"""
Monotype Translation Crew — entry point.

Usage:
    translate [excel_path]

    excel_path defaults to "inputs/translations Input.xlsx".
    Override with env vars: EXCEL_PATH, KNOWLEDGE_DIR.

Examples:
    translate
    translate "inputs/translations Input.xlsx"
    EXCEL_PATH="inputs/translations Input.xlsx" translate
"""

import os
import sys
import warnings

from monotype_translation_crew.crew import MonotypeTranslationCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run() -> None:
    """Run the Monotype translation crew."""
    excel_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.environ.get("EXCEL_PATH", os.path.join("inputs", "translations Input.xlsx"))
    )
    knowledge_dir = os.environ.get("KNOWLEDGE_DIR", "knowledge")

    if not os.path.exists(excel_path):
        print(
            f"ERROR: Excel file not found: {excel_path}\n"
            "Place your translation Excel file at that path or pass the path as an argument:\n"
            '    translate "inputs/translations Input.xlsx"',
            file=sys.stderr,
        )
        sys.exit(1)

    inputs = {
        "excel_path": excel_path,
        "knowledge_dir": knowledge_dir,
    }

    try:
        MonotypeTranslationCrew().crew().kickoff(inputs=inputs)
    except Exception as exc:
        raise RuntimeError(f"Crew execution failed: {exc}") from exc


def train() -> None:
    """Train the crew for a given number of iterations."""
    if len(sys.argv) < 3:
        print("Usage: train <n_iterations> <output_filename>", file=sys.stderr)
        sys.exit(1)
    inputs = {
        "excel_path": os.environ.get("EXCEL_PATH", os.path.join("inputs", "translations Input.xlsx")),
        "knowledge_dir": os.environ.get("KNOWLEDGE_DIR", "knowledge"),
    }
    try:
        MonotypeTranslationCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )
    except Exception as exc:
        raise RuntimeError(f"Training failed: {exc}") from exc


def replay() -> None:
    """Replay the crew from a specific task ID."""
    try:
        MonotypeTranslationCrew().crew().replay(task_id=sys.argv[1])
    except Exception as exc:
        raise RuntimeError(f"Replay failed: {exc}") from exc


def serve() -> None:
    """Start the web server.

    Run from the project root:
        uv run serve             # default: http://localhost:8000
        PORT=9000 uv run serve   # custom port
    """
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Monotype Translation Crew web UI at http://localhost:{port}")
    uvicorn.run(
        "monotype_translation_crew.api:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
