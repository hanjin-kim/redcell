"""redcell CLI.

Commands:
  redcell init [--output config.yaml] [--scenario scenario.yaml]
      Scaffold a starter config + scenario stub. Edit and run.
  redcell doctor
      Pre-flight checks: LLM credentials, connectivity, dependencies.
  redcell run <config.yaml> [-o brief.md] [--cache-dir .redcell_cache]
      Generate the adversarial scenario brief.
"""
from __future__ import annotations

import sys
from pathlib import Path

import typer

from .config import RunConfig, load_llm_settings
from .pipeline import run_and_render

app = typer.Typer(
    help="redcell — adversarial strategy scenario generator.",
    no_args_is_help=True,
)


@app.callback()
def _main():
    """Keep `run`/`init`/`doctor` as explicit subcommands (Typer collapses
    single-command apps otherwise)."""


# ---------------------------------------------------------------------
# Starter templates for `init`
# ---------------------------------------------------------------------

_CONFIG_TEMPLATE = """# redcell run config.
# Edit the fields below, then run:
#   redcell run {config_name}

industry: <industry_name>             # e.g., kbeauty_premium_skincare
our_company: <Our Company>            # the company whose strategy is being stress-tested
competitors:                          # 1-3 main rivals
  - <Competitor A>
  - <Competitor B>

strategy: |
  <Describe your strategy in 3-6 lines. Concrete actions + 12-24 month KPIs.>
  Example:
    프리미엄-아시아 듀얼 트랙: 고가 anti-aging SKU 집중 + 일본 직영 채널 50개
    신설 + 동남아 멀티브랜드 확장. R&D 매출 비중 7%→12% 증가.
    24개월 KPI: EBIT 마진 12→15%, 일본 매출 비중 8→18%.

worried_risk: |
  <One risk you're worried about. Concrete trigger + when + who.>
  Example:
    Shiseido가 2026 Q1부터 mass-premium 30% 가격 인하 실집행.

n_scenarios: 5     # 3-8 recommended. each scenario is one LLM-orchestrated sim
max_turns: 5       # multi-turn propagation depth
scenario_path: {scenario_name}
"""

_SCENARIO_TEMPLATE = """# Scenario context — industry parameters + competitor seats.
# Reference: see github.com/.../redcell/scenarios/kbeauty_aurie.yaml for a
# full example. The minimum stub below lets the engine bootstrap a rulebook
# from the industry name; for higher fidelity, add competitor strategies,
# event deck overrides, etc.

industry: <industry_name>

sides:
  - id: side_a       # our side — must be side_a
    company:
      id: <our_company_id>
      name: <Our Company>
  - id: side_b
    company:
      id: <competitor_a_id>
      name: <Competitor A>
  - id: side_c
    company:
      id: <competitor_b_id>
      name: <Competitor B>

# (Optional) initial cash and shares. Defaults below if omitted.
init_shares:
  side_a: 0.30
  side_b: 0.40
  side_c: 0.30

init_cash:
  side_a: 0.55
  side_b: 0.65
  side_c: 0.55
"""


@app.command()
def init(
    output: str = typer.Option(
        "redcell_config.yaml", "--output", "-o",
        help="Path to write the starter config.",
    ),
    scenario: str = typer.Option(
        "scenario.yaml", "--scenario", "-s",
        help="Path to write the starter scenario stub.",
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing files.",
    ),
):
    """Scaffold a starter config + scenario stub."""
    cfg_path = Path(output)
    scn_path = Path(scenario)

    if not force:
        for p in (cfg_path, scn_path):
            if p.exists():
                typer.secho(f"❌ {p} already exists. Use --force to overwrite.",
                            fg=typer.colors.RED, err=True)
                raise typer.Exit(code=1)

    cfg_path.write_text(
        _CONFIG_TEMPLATE.format(
            config_name=cfg_path.name, scenario_name=str(scn_path),
        ),
        encoding="utf-8",
    )
    scn_path.write_text(_SCENARIO_TEMPLATE, encoding="utf-8")

    typer.secho(f"✅ scaffolded:", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"  - config:   {cfg_path}")
    typer.echo(f"  - scenario: {scn_path}")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(f"  1. Edit {cfg_path} (industry, company, strategy, worry).")
    typer.echo(f"  2. Edit {scn_path} (industry, sides).")
    typer.echo("  3. Set LLM env vars (see `redcell doctor`).")
    typer.echo(f"  4. Run: redcell run {cfg_path}")


@app.command()
def doctor():
    """Run pre-flight checks: LLM creds, connectivity, optional deps."""
    ok = True

    typer.secho("== LLM settings ==", bold=True)
    settings = load_llm_settings()
    typer.echo(f"  model:    {settings.model or '(unset)'}")
    typer.echo(f"  base_url: {settings.base_url or '(default openai)'}")
    key_present = bool(settings.api_key)
    typer.echo(f"  api_key:  {'set' if key_present else '(unset)'}")
    if not key_present:
        typer.secho(
            "  ❌ No API key. Set SF_QWEN_API_KEY (or OPENAI_API_KEY) "
            "in env or .env.", fg=typer.colors.RED,
        )
        ok = False

    typer.secho("\n== Provider detection ==", bold=True)
    try:
        from .llm import detect_provider
        provider = detect_provider(settings.base_url, settings.model)
        typer.echo(f"  detected: {provider.name}")
        if provider.name == "openai_compatible":
            typer.secho(
                "  ⚠ Using conservative passthrough — provider not "
                "recognized. Qwen-specific kwargs disabled.",
                fg=typer.colors.YELLOW,
            )
    except Exception as e:
        typer.secho(f"  ❌ detection failed: {e}", fg=typer.colors.RED)
        ok = False

    typer.secho("\n== Connectivity ==", bold=True)
    if not key_present:
        typer.secho("  ⏭  skipped (no api_key)", fg=typer.colors.YELLOW)
    else:
        try:
            from .llm import LLMAdapter
            llm = LLMAdapter(
                model=settings.model, api_key=settings.api_key,
                base_url=settings.base_url,
            )
            # Use generous budget + thinking off explicitly so the ping
            # doesn't trip Qwen's reasoning preamble (which would eat a
            # tiny token budget and emit no content).
            out = llm.complete(
                system="Reply with exactly the word: ok", user="ping",
                temperature=0.0, max_tokens=64,
                enable_thinking=False,
            )
            typer.secho(f"  ✅ response: {out.strip()[:30]}",
                        fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"  ❌ call failed: {type(e).__name__}: {e}",
                        fg=typer.colors.RED)
            ok = False

    typer.secho("\n== Optional deps ==", bold=True)
    try:
        import json_repair  # noqa: F401
        typer.echo("  ✅ json_repair (robust JSON parse fallback)")
    except ImportError:
        typer.secho(
            "  ⚠ json_repair not installed (pip install json-repair). "
            "Without it, malformed LLM JSON will fail-fast instead of "
            "being recovered.", fg=typer.colors.YELLOW,
        )

    typer.echo("")
    if ok:
        typer.secho("All checks passed.", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho("Some checks failed — see above.",
                    fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)


@app.command()
def run(
    config: str = typer.Argument(..., help="Path to run config YAML."),
    output: str = typer.Option("red_team_brief.md", "--output", "-o",
                               help="Output markdown path."),
    cache_dir: str = typer.Option(".redcell_cache", "--cache-dir",
                                  help="Simulation cache directory."),
    quiet: bool = typer.Option(False, "--quiet", "-q",
                               help="Suppress per-scenario progress."),
):
    """Generate an adversarial scenario brief from a run config."""
    cfg_path = Path(config)
    if not cfg_path.exists():
        typer.secho(f"❌ config not found: {config}",
                    fg=typer.colors.RED, err=True)
        typer.echo("Run `redcell init` to scaffold a starter config.")
        raise typer.Exit(code=1)

    try:
        cfg = RunConfig.from_yaml(config)
    except Exception as e:
        typer.secho(f"❌ failed to parse config {config}:\n  {e}",
                    fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    scn_path = Path(cfg.scenario_path)
    if not scn_path.exists():
        typer.secho(
            f"❌ scenario_path not found: {cfg.scenario_path}\n"
            f"  (resolved from config field. Check the path is correct "
            f"relative to your current directory.)",
            fg=typer.colors.RED, err=True,
        )
        raise typer.Exit(code=1)

    settings = load_llm_settings()
    if not settings.api_key:
        typer.secho(
            "❌ No LLM API key. Set SF_QWEN_API_KEY (or OPENAI_API_KEY) "
            "in env or in a .env file in the project root.\n"
            "  Run `redcell doctor` to verify your setup.",
            fg=typer.colors.RED, err=True,
        )
        raise typer.Exit(code=1)

    log = (lambda *a, **k: None) if quiet else typer.echo

    try:
        run_and_render(cfg, output=output, cache_dir=cache_dir, log=log)
    except Exception as e:
        typer.secho(f"\n❌ Run failed: {type(e).__name__}: {e}",
                    fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2)


if __name__ == "__main__":
    app()
