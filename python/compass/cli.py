"""Main CLI interface using Typer."""

from pathlib import Path
from typing import Optional
import sys
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich import print as rprint

from compass import __version__
from compass.config import Config
from compass.vault import Vault, find_vault
from compass.paths import get_config_dir, get_vault_path
from compass.sessions import Session, SessionManager
from compass.logging import RunLogger

app = typer.Typer(
    name="compass",
    help="Personal knowledge management with RAG",
    add_completion=False,
    invoke_without_command=True,
)
console = Console()
logger = RunLogger()


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        rprint(f"Compass CLI v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
):
    """Compass CLI - Personal knowledge management with RAG."""
    if ctx.resilient_parsing:
        return

    cfg = Config()
    can_prompt = sys.stdin.isatty() and sys.stdout.isatty()
    if not cfg.is_set("llm.mode"):
        if can_prompt:
            choice = Prompt.ask(
                "Choose LLM mode (local keeps data on your machine)",
                choices=["local", "api"],
                default="local",
            )
        else:
            choice = "local"
        cfg.set("llm.mode", choice)
        if choice == "local" and not cfg.is_set("llm.provider"):
            cfg.set("llm.provider", "ollama")
        cfg.save()
        if can_prompt:
            console.print(f"[green]✓[/green] LLM mode set to: {choice}")

    if not cfg.is_set("user.name"):
        if can_prompt:
            name = Prompt.ask("What name should I greet you with?", default="friend")
            name = name.strip() or "friend"
        else:
            name = "friend"
        cfg.set("user.name", name)
        cfg.save()

    if ctx.invoked_subcommand is None:
        name = cfg.get("user.name", "friend")
        compass_art = r"""
          /\
     ____/  \____
    /    \  /    \
   /  /\  \/  /\  \
   \  \/  /\  \/  /
    \____/  \____/
          \/
        """
        console.print(compass_art, style="cyan")
        console.print(f"[bold]Welcome back, {name}![/bold]")
        console.print()
        console.print(ctx.get_help())
        raise typer.Exit()


@app.command()
def init(
    vault: Path = typer.Option(
        None,
        "--vault",
        help="Path to initialize vault",
    ),
):
    """Initialize a new vault."""
    if vault is None:
        vault = Path.cwd()

    vault = vault.resolve()
    vault_obj = Vault(vault)

    try:
        vault_obj.init()
        console.print(f"[green]✓[/green] Initialized vault at: {vault}")
        console.print(f"  - Config: {vault_obj.config_file}")
        console.print(f"  - Commands: {vault_obj.commands_dir}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def config(
    action: str = typer.Argument(..., help="Action: show, set, get"),
    key: Optional[str] = typer.Argument(None, help="Config key (dot notation)"),
    value: Optional[str] = typer.Argument(None, help="Config value"),
):
    """Manage configuration."""
    cfg = Config()

    if action == "show":
        import toml

        console.print("[bold]Current configuration:[/bold]")
        console.print(toml.dumps(cfg.get_all()))

    elif action == "get":
        if key is None:
            console.print("[red]Error:[/red] Key required for 'get' action")
            raise typer.Exit(1)
        result = cfg.get(key)
        if result is not None:
            console.print(f"{key} = {result}")
        else:
            console.print(f"[yellow]Warning:[/yellow] Key '{key}' not found")

    elif action == "set":
        if key is None or value is None:
            console.print("[red]Error:[/red] Key and value required for 'set' action")
            raise typer.Exit(1)
        cfg.set(key, value)
        cfg.save()
        console.print(f"[green]✓[/green] Set {key} = {value}")

    else:
        console.print(f"[red]Error:[/red] Unknown action '{action}'")
        console.print("Valid actions: show, set, get")
        raise typer.Exit(1)


@app.command()
def ingest(
    path: Path = typer.Argument(..., help="Path to ingest (file or directory)"),
    vault: Optional[Path] = typer.Option(None, "--vault", help="Vault path"),
):
    """Ingest documents into the knowledge base."""
    if not path.exists():
        console.print(f"[red]Error:[/red] Path does not exist: {path}")
        raise typer.Exit(1)

    # Count files (placeholder)
    if path.is_file():
        file_count = 1
    else:
        file_count = sum(1 for _ in path.rglob("*") if _.is_file())

    console.print(f"[green]✓[/green] Ingested {file_count} file(s) from {path}")
    console.print("[dim]Note: Full ingestion pipeline not yet implemented[/dim]")
    logger.log_command("ingest", {"path": str(path), "file_count": file_count})


@app.command()
def chat(
    vault: Optional[Path] = typer.Option(None, "--vault", help="Vault path"),
    resume: Optional[str] = typer.Option(None, "--resume", help="Resume session ID"),
):
    """Start an interactive chat session."""
    console.print("[bold cyan]Compass Chat[/bold cyan]")
    console.print("Type /help for commands, /exit to quit\n")

    session_mgr = SessionManager()
    if resume:
        session = session_mgr.load(resume)
        if session:
            console.print(f"[green]Resumed session:[/green] {session.id}")
        else:
            console.print(f"[yellow]Session not found, starting new session[/yellow]")
            session = Session()
    else:
        session = Session()
        console.print(f"[dim]Session ID: {session.id}[/dim]")

    while True:
        try:
            user_input = Prompt.ask("\n[bold blue]You[/bold blue]")

            if not user_input.strip():
                continue

            # Handle slash commands
            if user_input.startswith("/"):
                cmd = user_input[1:].lower()
                if cmd == "exit" or cmd == "quit":
                    console.print("[dim]Goodbye![/dim]")
                    session_mgr.save(session)
                    break
                elif cmd == "help":
                    console.print("\n[bold]Available commands:[/bold]")
                    console.print("  /help  - Show this help")
                    console.print("  /exit  - Exit chat")
                    continue
                else:
                    console.print(f"[yellow]Unknown command:[/yellow] /{cmd}")
                    continue

            # Echo user input (placeholder for actual LLM)
            session.add_message("user", user_input)
            response = f"[Placeholder response to: {user_input[:50]}...]"
            session.add_message("assistant", response)

            console.print(f"\n[bold green]Compass[/bold green]: {response}")

        except KeyboardInterrupt:
            console.print("\n[dim]Use /exit to quit[/dim]")
        except EOFError:
            break

    logger.log_completion("chat", 0)


@app.command()
def exec(
    prompt: str = typer.Argument(..., help="Prompt to execute"),
    vault: Optional[Path] = typer.Option(None, "--vault", help="Vault path"),
):
    """Execute a one-off prompt."""
    console.print(f"[bold]Prompt:[/bold] {prompt}")
    console.print(f"\n[bold green]Compass:[/bold green] [Placeholder response]")
    console.print("[dim]LLM integration not yet implemented[/dim]")
    logger.log_command("exec", {"prompt": prompt})


if __name__ == "__main__":
    app()
