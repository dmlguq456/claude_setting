"""Normalized cross-harness schema + shared helpers (zero-dep, stdlib only).

`Session` / `DispatchJob` are the harness-agnostic rows the render layer consumes.
Collectors fill them; no harness-specific logic lives here. Any field a harness
cannot provide stays `None` and renders as `—` (an explicit "not available",
never a blank — PRD §4 결손 칸 규칙).
"""
import re
from dataclasses import dataclass, field, asdict
from typing import Optional


# --- shared time helpers (ps etime parsing + human format) ---
def etime_to_min(et):
    """ps etime ([[DD-]HH:]MM:SS) → whole minutes (int)."""
    et = (et or "").strip()
    if not et:
        return 0
    days = 0
    if "-" in et:
        d, et = et.split("-", 1)
        try:
            days = int(d)
        except ValueError:
            days = 0
    try:
        nums = [int(p) for p in et.split(":")]
    except ValueError:
        return 0
    while len(nums) < 3:
        nums.insert(0, 0)
    hh, mm = nums[-3], nums[-2]
    return days * 1440 + hh * 60 + mm


def fmt_min(m):
    """minutes → '5h20m' / '20m'; None/invalid → '—'."""
    if m is None:
        return "—"
    try:
        m = int(m)
    except (TypeError, ValueError):
        return "—"
    if m < 0:
        return "—"
    return f"{m // 60}h{m % 60:02d}m" if m >= 60 else f"{m}m"


def dash(v, fmt=None):
    """Render helper: None/'' → '—', else fmt(v) or str(v)."""
    if v is None or v == "":
        return "—"
    return fmt(v) if fmt else str(v)


# 4-state herdr vocabulary (+ stale/dead) — single source for render coloring.
LIVENESS_STATES = ("working", "idle", "blocked", "done", "stale", "dead", "unknown")


def project_of(cwd):
    """Grouping key for the render v2 cwd-project groups — one group per parent repo.

    Rule precedence (documented, not accidental): `-wt` OUTRANKS `_worktrees`, and both
    passes are OUTERMOST-COMPONENT-FIRST (left→right). This is a TWO-PASS scan (all
    components checked for `-wt` before ANY component is checked for `_worktrees`) —
    a single interleaved pass would let an outer `_worktrees` component win over an
    inner `-wt` component, which is the wrong precedence (see the mixed 7th test case
    below). Edge cases verified — see plan Verification §1 / dev_logs/step_01_model.md:
      /x/agent_setting-wt/fleet-dashboard              -> agent_setting
      /x/.claude/worklog-board-wt/studio-c2            -> worklog-board
      /x/.claude-wt/definitions-manifest               -> .claude
      /x/Stream_Diar_Baselines_worktrees/m5b_ls_eend_engine -> Stream_Diar_Baselines
      /x/worklog-board.broken-20260629-151852          -> worklog-board
      ''                                                -> (unknown)
      /a/foo_worktrees/bar-wt/leaf                     -> bar   (outer `_worktrees` component
                                                                   loses to inner `-wt` component
                                                                   because of the two-pass order)

    Known accepted edge: basename-only merge means `/home/Uihyeop` and
    `/home/nas/user/Uihyeop` both project to `Uihyeop` (same human, different mount —
    treated as one group; acceptable, not a bug).

    Quirk (not a bug, a consequence of rule 1 being unable to distinguish a worktree
    PARENT from a leaf literally named `<x>-wt`): a non-worktree directory named
    e.g. `/x/my-cool-wt` (no children, not actually a worktree root) still truncates
    to `my-cool` — rule 1 has no way to tell the two apart from the path alone.
    """
    if not cwd:
        return "(unknown)"
    parts = [p for p in cwd.rstrip("/").split("/") if p]
    # pass 1 (outermost-first): `-wt` suffix — takes precedence over `_worktrees`.
    for comp in parts:
        if len(comp) > 3 and comp.endswith("-wt"):
            return comp[: -len("-wt")]
    # pass 2 (outermost-first): `_worktrees` suffix.
    for comp in parts:
        if len(comp) > len("_worktrees") and comp.endswith("_worktrees"):
            return comp[: -len("_worktrees")]
    # fallback: basename, with a trailing `.broken*` marker stripped.
    base = parts[-1] if parts else ""
    base = re.sub(r"\.broken.*$", "", base)
    return base or "(root)"


@dataclass
class Session:
    """One live harness session (backbone = one per matched process)."""
    harness: str                       # claude | codex | opencode
    pid: int
    cwd: str = ""
    orphan: bool = False               # /proc/<pid>/cwd had ' (deleted)' (worktree gone)
    app_server: bool = False           # codex app-server companion (procscan-detected — see collectors/procscan.py)
    elapsed_min: int = 0               # ps etime
    # --- enrichment (None = harness doesn't expose it → render '—') ---
    session_id: Optional[str] = None
    slug: Optional[str] = None
    model: Optional[str] = None
    effort: Optional[str] = None
    ctx_pct: Optional[int] = None      # context window used %
    rl_5h: Optional[int] = None        # claude five_hour / codex primary  used %
    rl_7d: Optional[int] = None        # claude seven_day / codex secondary used %
    cost: Optional[float] = None
    tokens: Optional[int] = None
    status: Optional[str] = None        # raw harness status (claude idle/shell/busy)
    mtime: Optional[float] = None       # newest transcript/db mtime (epoch sec) for liveness
    liveness: str = "unknown"

    def to_dict(self):
        return asdict(self)


@dataclass
class DispatchJob:
    """One headless dispatch job (autopilot-*/loops process, or jobs.log row)."""
    key: str                            # pipe key: autopilot-code / oncall / ...
    stage: Optional[str] = None         # plan | exec | test | done (live_stage)
    mode: Optional[str] = None          # --mode value
    qa: Optional[str] = None            # --qa value
    elapsed_min: Optional[int] = None
    slug: str = ""
    cwd: str = ""
    source: str = "proc"                # proc | jobs
    status: Optional[str] = None        # raw jobs.log status (open/running/...)
    liveness: str = "unknown"

    def to_dict(self):
        return asdict(self)
