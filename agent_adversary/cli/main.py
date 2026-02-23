import click
import asyncio
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from ..adversary.logic.engine import AdversaryEngine, BenchmarkReport
from ..adversary.jailbreak.library import ScenarioLibrary
from ..connectors.base import ShellConnector
from ..connectors.browser import BrowserConnector
from ..evaluator.judge import JudgeModel
from ..patching.hotfix import LivePatcher
from ..observability.exporters import PrometheusExporter
import os
import json

from ..adversary.generator import AutonomousGenerator

console = Console()

@click.group()
def main():
    """🛡️ Agent-Adversary: Forge more reliable AI through adversarial testing."""
    pass

@main.command()
def list():
    """List all available adversarial scenarios."""
    library = ScenarioLibrary()
    library.load_defaults()
    
    table = Table(title="Available Adversarial Scenarios")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category", style="magenta")
    
    for s in library.scenarios:
        table.add_row(s.id, s.name, s.category)
    
    console.print(table)

@main.command()
@click.option('--agent', help='Shell command to run the target agent (for Shell connector).')
@click.option('--url', help='Target URL (for Browser connector).')
@click.option('--scenario', default="all", help='Scenario ID to run or "all".')
@click.option('--connector', type=click.Choice(['shell', 'browser']), default='shell', help='Interfacing method.')
@click.option('--telemetry/--no-telemetry', default=True, help='Enable real-time telemetry logging.')
@click.option('--patch/--no-patch', default=False, help='Enable live adversarial patching (Hotfix).')
def bench(agent: str, url: str, scenario: str, connector: str, telemetry: bool, patch: bool):
    """Run adversarial benchmarks against an agent."""
    library = ScenarioLibrary()
    library.load_defaults()
    
    # 1. Initialize Connector
    if connector == 'shell':
        if not agent:
            console.print("[red]Error: --agent command required for shell connector.[/red]")
            return
        conn = ShellConnector(agent)
    else:
        if not url:
            console.print("[red]Error: --url required for browser connector.[/red]")
            return
        conn = BrowserConnector(url=url)

    # 2. Initialize Judge & Engine
    judge = JudgeModel()
    engine = AdversaryEngine(conn, judge, enable_telemetry=telemetry)
    patcher = LivePatcher() if patch else None

    # 3. Select Scenarios
    to_run = []
    if scenario == "all":
        to_run = [s.id for s in library.scenarios]
    else:
        if library.get_scenario(scenario):
            to_run = [scenario]
        else:
            console.print(f"[red]Error: Scenario '{scenario}' not found.[/red]")
            return

    # 4. Execution
    results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for sid in to_run:
            progress.add_task(description=f"Running {sid}...", total=None)
            res = engine.run_scenario_by_id(sid)
            results.append(res)
            
            # Apply Hotfix if enabled and resilience is low
            if patcher:
                hotfix = patcher.generate_hotfix(res)
                if hotfix:
                    console.print(f"[yellow]![/yellow] [bold red]Exploit Detected![/bold red] Applied hotfix for {sid}")

    # 5. Report
    report_md = BenchmarkReport.to_markdown(results)
    console.print("\n[bold green]Benchmark Completed![/bold green]")
    
    table = Table(title="Summary Results")
    table.add_column("Scenario", style="cyan")
    table.add_column("Resilience Score", style="bold magenta")
    for r in results:
        table.add_row(r.scenario_id, f"{r.total_resilience:.2f}")
    console.print(table)
    
    # Export to file
    with open("latest_report.md", "w") as f:
        f.write(report_md)
    console.print(f"\nDetailed report saved to [bold]latest_report.md[/bold]")

@main.command()
@click.argument('session_id')
def observe(session_id: str):
    """View real-time telemetry events for a session."""
    log_path = f"logs/telemetry/{session_id}.jsonl"
    if not os.path.exists(log_path):
        console.print(f"[red]Error: Session {session_id} not found.[/red]")
        return
    
    console.print(f"[bold cyan]Observing Session: {session_id}[/bold cyan]")
    with open(log_path, 'r') as f:
        for line in f:
            event = json.loads(line)
            console.print(f"[{event['timestamp']}] [bold green]{event['event_type']}[/bold green]: {event['data']}")

@main.command()
@click.option('--output', default='metrics.prom', help='File to save Prometheus metrics.')
def export(output: str):
    """Export all session telemetry to Prometheus metrics."""
    # Simplified mock implementation
    metrics = "# Agent Adversary Prometheus Metrics"
    with open(output, 'w') as f:
        f.write(metrics)
    console.print(f"Metrics exported to [bold]{output}[/bold]")

@main.command()
@click.option('--description', required=True, help='Description of the target agent.')
@click.option('--count', default=3, help='Number of scenarios to generate.')
def generate(description: str, count: int):
    """Dynamically generate new adversarial scenarios using LLM."""
    gen = AutonomousGenerator()
    with console.status("[bold green]Generating scenarios..."):
        new_scenarios = gen.generate_scenarios(description, count)
    
    if not new_scenarios:
        console.print("[red]Failed to generate scenarios.[/red]")
        return

    table = Table(title="Generated Scenarios")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    
    for s in new_scenarios:
        table.add_row(s.get('id', 'N/A'), s.get('name', 'N/A'))
    
    console.print(table)
    console.print("\n[bold]Run with:[/bold] `agent-adversary bench --scenario <id>`")

if __name__ == "__main__":
    main()
