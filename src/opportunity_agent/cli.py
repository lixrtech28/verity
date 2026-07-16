from __future__ import annotations

import json
from pathlib import Path

import typer

from .agent import EvidenceAgent
from .models import AgentInput, AgentReport
from .providers import ProviderError, get_provider

app = typer.Typer(no_args_is_help=True, help="Evidence-disciplined opportunity intelligence agent")


@app.command()
def run(
    input_file: Path = typer.Argument(..., exists=True, readable=True),
    output_file: Path = typer.Option(Path("output/report.json"), "--output", "-o"),
    provider: str = typer.Option("mock", help="mock, openai, anthropic, or ollama"),
    model: str | None = typer.Option(None, help="Provider-specific model name"),
) -> None:
    """Generate a report from a human-curated JSON research packet."""
    try:
        payload = json.loads(input_file.read_text(encoding="utf-8"))
        agent_input = AgentInput.model_validate(payload)
        report = EvidenceAgent(get_provider(provider, model)).run(agent_input)
        report.save_json(output_file)
    except (ValueError, json.JSONDecodeError, ProviderError) as exc:
        typer.echo(f"ERROR: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Saved evidence report to {output_file}")
    typer.echo("Human approval is required before any outreach is sent.")


@app.command()
def approve(
    report_file: Path = typer.Argument(..., exists=True, readable=True),
    reviewer: str = typer.Option(..., prompt=True),
) -> None:
    """Record human approval. This does not send any message."""
    report = AgentReport.model_validate_json(report_file.read_text(encoding="utf-8"))
    report.approved_by = reviewer
    report.human_approval_required = False
    report_file.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    typer.echo(f"Approval recorded by {reviewer}. No external action was performed.")


if __name__ == "__main__":
    app()
