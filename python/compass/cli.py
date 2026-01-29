"""Main CLI interface using Typer."""

from pathlib import Path
from typing import Any, Dict, Optional
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint

from compass import __version__
from compass.config import Config
from compass.vault import Vault, find_vault
from compass.paths import get_config_dir, get_vault_path, get_default_vault_path
from compass.mcp import LocalDataAccess
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


def _load_logo() -> str:
    """Load the Compass logo from the design folder if available."""
    logo_path = Path(__file__).resolve().parents[2] / "design" / "logo.txt"
    if logo_path.exists():
        return logo_path.read_text().rstrip()
    return (
        "  _____    ____    __  __   _____     __        _____    _____\n"
        " / ____|  / __ \\  |  \\/  | |  __ \\   /  \\      / ____|  / ____|\n"
        "| |      | |  | | | \\  / | | |__) | / /\\ \\    | (____   | (___\n"
        "| |      | |  | | | |\\/| | |  ___/ / /  \\ \\    \\____ \\  \\___   \\\n"
        "| |____  | |__| | | |  | | | |    / /    \\_\\   ____)  |  ____) |\n"
        " \\_____|  \\____/  |_|  |_| |_|   /_/      \\_\\ |______/  |_____/\n"
    )


def _get_quick_options(cfg: Config) -> list[str]:
    """Return quick options, ensuring they are stored locally."""
    options = cfg.get("quick.options", [])
    if not options:
        options = [
            "Daily review",
            "Summarize recent notes",
            "Plan my day",
        ]
    if not cfg.is_set("quick.options"):
        cfg.set("quick.options", options)
        cfg.save()
    return options


PROVIDERS = {
    "1": ("local", "ollama", "Local (Ollama)"),
    "2": ("api", "openai", "OpenAI"),
    "3": ("api", "anthropic", "Anthropic"),
    "4": ("api", "google", "Google"),
}


def _detect_hardware() -> Optional[Dict[str, Any]]:
    """Run jido hardware detection if available."""
    try:
        from jido.core.hardware import detect
        hardware, _env, _hints, _mid = detect.scan()
        return hardware
    except (ImportError, Exception):
        return None


def _display_hardware(hardware: Dict[str, Any]) -> None:
    """Format and print hardware info using Rich."""
    table = Table(title="Detected Hardware", show_header=False, border_style="cyan")
    table.add_column("Component", style="bold")
    table.add_column("Details")

    cpu = hardware.get("cpu", {})
    table.add_row("CPU", cpu.get("brand", "Unknown"))
    table.add_row("Cores", f"{cpu.get('physical_cores', '?')} physical / {cpu.get('logical_cores', '?')} logical")

    mem = hardware.get("memory", {})
    total = mem.get("total_gb", 0)
    table.add_row("RAM", f"{total:.1f} GB" if total else "Unknown")

    gpus = hardware.get("gpus", [])
    if gpus:
        for i, gpu in enumerate(gpus):
            name = gpu.get("name", "Unknown")
            vram = gpu.get("vram_total_mb", 0)
            label = f"GPU {i}" if len(gpus) > 1 else "GPU"
            detail = f"{name} ({vram} MB)" if vram else name
            table.add_row(label, detail)
    else:
        table.add_row("GPU", "None detected")

    console.print(table)
    console.print()


def _first_run_setup(cfg: Config) -> None:
    """First-run welcome screen: detect hardware and choose provider."""
    console.print("\n[bold cyan]Welcome to Compass![/bold cyan]")
    console.print("Let's configure your LLM provider.\n")

    hardware = _detect_hardware()
    if hardware:
        _display_hardware(hardware)
    else:
        console.print("[dim]Hardware detection unavailable (install jido for details)[/dim]\n")

    console.print("[bold]Choose your LLM provider:[/bold]")
    for num, (_mode, _prov, label) in PROVIDERS.items():
        console.print(f"  {num}. {label}")

    choice = Prompt.ask("\nSelection", choices=list(PROVIDERS.keys()), default="1")
    mode, provider, label = PROVIDERS[choice]

    cfg.set("llm.mode", mode)
    cfg.set("llm.provider", provider)

    if mode == "api":
        api_key = Prompt.ask(f"Enter your {label} API key", password=True)
        if api_key.strip():
            cfg.set("llm.api_key", api_key.strip())

    cfg.save()
    console.print(f"\n[green]\u2713[/green] Provider set to: {label}")


def _handle_settings(cfg: Config) -> None:
    """Implement the /settings slash command."""
    while True:
        mode = cfg.get("llm.mode", "not set")
        provider = cfg.get("llm.provider", "not set")
        api_key = cfg.get("llm.api_key")
        masked = f"{api_key[:4]}{'*' * (len(api_key) - 4)}" if api_key else "not set"

        console.print("\n[bold cyan]Settings[/bold cyan]")
        console.print(f"  Mode:     {mode}")
        console.print(f"  Provider: {provider}")
        console.print(f"  API Key:  {masked}")
        console.print()
        console.print("  1. Change provider")
        console.print("  2. Set API key")
        console.print("  3. Re-run hardware detection")
        console.print("  4. Back")

        action = Prompt.ask("\nSelection", choices=["1", "2", "3", "4"], default="4")

        if action == "1":
            console.print("\n[bold]Choose provider:[/bold]")
            for num, (_m, _p, label) in PROVIDERS.items():
                console.print(f"  {num}. {label}")
            pick = Prompt.ask("Selection", choices=list(PROVIDERS.keys()), default="1")
            m, p, label = PROVIDERS[pick]
            cfg.set("llm.mode", m)
            cfg.set("llm.provider", p)
            cfg.save()
            console.print(f"[green]\u2713[/green] Provider set to: {label}")

        elif action == "2":
            key = Prompt.ask("Enter API key", password=True)
            if key.strip():
                cfg.set("llm.api_key", key.strip())
                cfg.save()
                console.print("[green]\u2713[/green] API key saved")

        elif action == "3":
            hardware = _detect_hardware()
            if hardware:
                _display_hardware(hardware)
            else:
                console.print("[dim]Hardware detection unavailable[/dim]")

        else:
            break


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

    if not cfg.is_set("vault.default_path"):
        cfg.set("vault.default_path", str(get_default_vault_path()))
        cfg.save()

    if ctx.invoked_subcommand is None:
        compass_art = _load_logo()
        console.print(compass_art, style="cyan")
        console.print()
        chat(vault=None, resume=None)
        return


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

    cfg = Config()

    if not cfg.is_set("llm.mode"):
        _first_run_setup(cfg)

    quick_options = _get_quick_options(cfg)
    if not isinstance(vault, (Path, type(None))):
        vault = None
    vault_path = vault or get_vault_path()
    if vault_path is None:
        default_path = cfg.get("vault.default_path")
        vault_path = Path(default_path) if default_path else None
    local_data = LocalDataAccess.from_config(vault_path)

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

            stripped = user_input.strip()
            if stripped.isdigit():
                index = int(stripped)
                if 1 <= index <= len(quick_options):
                    user_input = quick_options[index - 1]

            # Handle slash commands
            if user_input.startswith("/"):
                raw_cmd = user_input[1:].strip()
                cmd, _, rest = raw_cmd.partition(" ")
                cmd = cmd.lower()
                rest = rest.strip()
                if cmd == "exit" or cmd == "quit":
                    console.print("[dim]Goodbye![/dim]")
                    session_mgr.save(session)
                    break
                elif cmd == "help":
                    console.print("\n[bold]Available commands:[/bold]")
                    console.print("  /help     - Show this help")
                    console.print("  /settings - Configure LLM provider and API keys")
                    console.print("  /exit     - Exit chat")
                    console.print("  /local status - Show local vault path")
                    console.print("  /local list [dir] - List files in vault")
                    console.print("  /local read <path> - Read a file from vault")
                    continue
                elif cmd == "settings":
                    _handle_settings(cfg)
                    continue
                elif cmd in ("local", "mcp"):
                    subcmd, _, subrest = rest.partition(" ")
                    subcmd = subcmd.lower() if subcmd else "status"
                    subrest = subrest.strip()
                    if subcmd == "status":
                        console.print(local_data.status())
                    elif subcmd == "list":
                        files = local_data.list_files(subrest)
                        if not files:
                            console.print("[dim]No files found.[/dim]")
                        else:
                            for entry in files[:50]:
                                console.print(entry)
                            if len(files) > 50:
                                console.print(f"[dim]...and {len(files) - 50} more[/dim]")
                    elif subcmd == "read":
                        if not subrest:
                            console.print("[yellow]Usage:[/yellow] /local read <path>")
                        else:
                            try:
                                content = local_data.read_text(subrest)
                                console.print(content)
                            except FileNotFoundError:
                                console.print(f"[yellow]Not found:[/yellow] {subrest}")
                    else:
                        console.print(f"[yellow]Unknown /local command:[/yellow] {subcmd}")
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
