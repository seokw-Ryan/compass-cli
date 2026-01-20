"""First-run setup helpers.

Handles local vs API mode selection and basic user preferences. All settings
are stored locally in the Compass config file.
"""

import sys
from rich.prompt import Prompt
from compass.config import Config


def is_interactive() -> bool:
    """Return True if we can safely prompt the user."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def _is_llm_setup_valid(cfg: Config) -> bool:
    """Validate that required LLM config is present."""
    mode = cfg.get("llm.mode")
    provider = cfg.get("llm.provider")
    api_key = cfg.get("llm.api_key")
    local_model = cfg.get("llm.local_model")

    if mode == "api":
        return bool(provider) and bool(api_key)
    if mode == "local":
        return bool(provider) and bool(local_model)
    return False


def ensure_setup(cfg: Config) -> None:
    """Ensure required config values are set.

    If running non-interactively, defaults are applied without prompting.
    """
    can_prompt = is_interactive()

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

    if not cfg.is_set("user.name"):
        if can_prompt:
            name = Prompt.ask("What name should I greet you with?", default="friend")
            name = name.strip() or "friend"
        else:
            name = "friend"
        cfg.set("user.name", name)
        cfg.save()

    cfg.set("setup.ready", _is_llm_setup_valid(cfg))
    cfg.save()
