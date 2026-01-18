"""CLI interface for RekaKata."""
import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from src.core.prompt_engine import PromptEngine
from config.logging_config import log


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    RekaKata - AI-powered UGC Prompt Generator.

    Generate optimized prompts for text-to-video AI tools like RunwayML, Pika, and Kling.
    """
    pass


@cli.command()
@click.argument("idea", type=str, required=True)
@click.option(
    "--output", "-o", type=click.Path(), help="Save output to file"
)
@click.option(
    "--format", "-f", type=click.Choice(["md", "json"]), default="md", help="Output format"
)
@click.option(
    "--platforms", "-p", type=str, help="Target platforms (comma-separated: tiktok,instagram,youtube)"
)
def generate(idea: str, output: str, format: str, platforms: str):
    """
    Generate a prompt for text-to-video generation.

    IDEA: Your content idea or description
    """
    try:
        # Parse platforms if provided
        platform_list = None
        if platforms:
            platform_list = [p.strip() for p in platforms.split(",")]

        # Show processing animation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Generating prompt...", total=None)

            # Generate prompt
            engine = PromptEngine()
            result = engine.generate_prompt(idea, platforms=platform_list)

            progress.remove_task(task)

        if not result["success"]:
            console.print(
                Panel(
                    f"[red]✗ Error: {result.get('error', 'Unknown error')}[/red]",
                    title="[bold red]Failed[/bold red]",
                    border_style="red",
                )
            )
            sys.exit(1)

        # Display success
        console.print(
            Panel(
                "[green]✓ Prompt generated successfully![/green]",
                title="[bold green]Success[/bold green]",
                border_style="green",
            )
        )

        # Display structured info
        console.print(f"\n[bold]Language:[/bold] {result['language'].upper()}")
        console.print(f"[bold]Entities:[/bold] {len(result['entities'])} detected")

        # Display markdown output
        if format == "md":
            md_content = result["markdown_output"]
            console.print("\n")
            console.print(Panel(Markdown(md_content), title="[bold]Generated Prompt[/bold]", border_style="cyan"))

            # Save to file if specified
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(md_content)
                console.print(f"\n[green]✓ Saved to:[/green] {output}")
            else:
                # Auto-save with timestamp
                filepath = engine.export_last_generated(format="md")
                if filepath:
                    console.print(f"\n[green]✓ Saved to:[/green] {filepath}")

        elif format == "json":
            import json

            json_content = result["structured_result"]
            json_str = json.dumps(json_content, indent=2, ensure_ascii=False)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(json_str)
                console.print(f"\n[green]✓ Saved JSON to:[/green] {output}")
            else:
                # Auto-save with timestamp
                filepath = engine.export_last_generated(format="json")
                if filepath:
                    console.print(f"\n[green]✓ Saved JSON to:[/green] {filepath}")

    except KeyboardInterrupt:
        console.print("\n[yellow]✓ Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(
            Panel(
                f"[red]✗ Unexpected error: {str(e)}[/red]",
                title="[bold red]Error[/bold red]",
                border_style="red",
            )
        )
        log.error(f"CLI error: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
def export():
    """Export the last generated prompt to file."""
    try:
        engine = PromptEngine()

        # Try to export
        filepath = engine.export_last_generated(format="md")

        if not filepath:
            console.print(
                Panel(
                    "[yellow]No previously generated prompt to export.[/yellow]\n\n"
                    "Use 'generate' command first to create a prompt.",
                    title="[bold yellow]No Data[/bold yellow]",
                    border_style="yellow",
                )
            )
            sys.exit(1)

        console.print(
            Panel(
                f"[green]✓ Exported to:[/green] {filepath}",
                title="[bold green]Export Success[/bold green]",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(
            Panel(
                f"[red]✗ Export failed: {str(e)}[/red]",
                title="[bold red]Error[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)


@cli.command()
@click.option(
    "--platform", "-p", type=click.Choice(["tiktok", "instagram", "youtube"]), help="Show platform-specific info"
)
def info(platform):
    """Show information about supported platforms."""
    from src.core.platform_optimizer import PlatformOptimizer

    optimizer = PlatformOptimizer()

    if platform:
        specs = optimizer.PLATFORM_SPECS.get(platform)
        if specs:
            console.print(
                Panel(
                    f"""
[bold]Platform:[/bold] {platform.capitalize()}
[bold]Aspect Ratio:[/bold] {specs['aspect_ratio']}
[bold]Max Duration:[/bold] {specs['max_duration']}
[bold]Resolution:[/bold] {specs['resolution']}
[bold]Characteristics:[/bold] {specs['characteristics']}
[bold]Optimal Length:[/bold] {specs['optimal_length']}
""",
                    title=f"[bold cyan]{platform.capitalize()}[/bold cyan]",
                    border_style="cyan",
                )
            )
        else:
            console.print(
                Panel(
                    f"[red]Unknown platform: {platform}[/red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red",
                )
            )
            sys.exit(1)
    else:
        # Show all platforms
        for plt, specs in optimizer.PLATFORM_SPECS.items():
            console.print(
                Panel(
                    f"""
[bold]Aspect Ratio:[/bold] {specs['aspect_ratio']}
[bold]Max Duration:[/bold] {specs['max_duration']}
[bold]Resolution:[/bold] {specs['resolution']}
[bold]Characteristics:[/bold] {specs['characteristics']}
""",
                    title=f"[bold cyan]{plt.capitalize()}[/bold cyan]",
                    border_style="cyan",
                )
            )


@cli.command()
def version():
    """Show version information."""
    console.print(
        Panel(
            "[bold]RekaKata v1.0.0[/bold]\n\n"
            "[cyan]AI-powered UGC Prompt Generator[/cyan]\n\n"
            "Generate optimized prompts for:\n"
            "• RunwayML\n"
            "• Pika Labs\n"
            "• Kling\n\n"
            "Supports TikTok, Instagram Reels, and YouTube Shorts",
            title="[bold yellow]RekaKata[/bold yellow]",
            border_style="yellow",
        )
    )


def main():
    """Main entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()
