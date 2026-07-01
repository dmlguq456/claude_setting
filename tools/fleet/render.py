"""Render layer — curses cwd-project-group TUI (live) + plain snapshot (--once). PRD §4 v2.

Both paths build the same flat segment-line list ([(text, color_key), ...] per line, None =
blank line) via `_build_lines` — the plain renderer joins the text (for piping / smoke tests,
no ANSI), the curses renderer paints each segment through a scrollable viewport. Missing cells
render as '—' (never blank). Layout: one group per project (cwd), each holding its sessions
followed by its dispatch jobs under a dim `dispatch:` sub-label. Responsive: narrow (<~70 cols)
drops low-priority fields; badge/slug/liveness never drop.

Module-global state invariants (single-process / single-thread only — no concurrent `_draw`):
  - `_OFFSET` (scroll offset) is READ in exactly ONE place: `_draw` (the viewport slice
    `lines[_OFFSET:_OFFSET+body_h]`). `_build_lines` must NEVER read `_OFFSET` — this is what
    guarantees the plain/`--once` path (which calls `_build_lines` directly) can never drop
    top lines.
  - Resize safety = re-clamp `_OFFSET` against the new `body_h` on every wake via
    `_clamp_offset`, NOT reset. Do NOT reset `_OFFSET` on KEY_RESIZE — that would destroy the
    user's scroll position on every resize.
  - `reset_scroll()` (public, called by fleet.py) sets `_OFFSET=0` — belt-and-suspenders for
    the single-process-per-launch model (a fresh process already starts at 0; only load-bearing
    if `run_live` were ever called twice in one process).
  - `_TOGGLE_ROWS` is reset at the TOP of `_draw`, before any early-return / short-circuit, so a
    stale toggle map never survives to the next click.
"""
import curses
import sys
import time

from .model import fmt_min, dash, project_of

_BADGE_TEXT = {"claude": "[Claude]", "codex": "[Codex]", "opencode": "[opencode]"}
_BADGE_KEY = {"claude": "badge_claude", "codex": "badge_codex", "opencode": "badge_opencode"}
_LIVE_RANK = {"working": 0, "idle": 1, "blocked": 2, "done": 3, "stale": 4, "dead": 5, "unknown": 6}
_JOB_LIVE_RANK = {"working": 0, "stale": 1, "dead": 2, "unknown": 3}
_EFFORT_KEY = {"low": "dim", "medium": "ok", "high": "warn", "xhigh": "blocked", "max": "dead"}
_NARROW_CUTOFF = 70
_LOOPS_KEYS = ("oncall", "note", "study", "drill")

_COLOR = {}   # color_key → curses attr (filled by _init_colors); empty ⇒ plain mode


# ---------- color ----------
def _init_colors():
    _COLOR.clear()
    try:
        curses.start_color()
        curses.use_default_colors()
        bg = -1
    except Exception:
        bg = curses.COLOR_BLACK
    spec = {
        "work": curses.COLOR_GREEN, "ok": curses.COLOR_GREEN, "done": curses.COLOR_CYAN,
        "warn": curses.COLOR_YELLOW, "blocked": curses.COLOR_YELLOW,
        "stale": curses.COLOR_RED, "dead": curses.COLOR_RED,
        "badge_claude": curses.COLOR_CYAN, "badge_codex": curses.COLOR_MAGENTA,
        "badge_opencode": curses.COLOR_GREEN,
        "head": curses.COLOR_CYAN,
        "pct_g": curses.COLOR_GREEN, "pct_y": curses.COLOR_YELLOW, "pct_r": curses.COLOR_RED,
    }
    n = 1
    for key, fg in spec.items():
        try:
            curses.init_pair(n, fg, bg)
            _COLOR[key] = curses.color_pair(n)
            n += 1
        except Exception:
            _COLOR[key] = 0
    # reverse-video badges: OR the color pair with A_REVERSE (falls back to plain A_REVERSE
    # if the pair failed to init above).
    for k in ("badge_claude", "badge_codex", "badge_opencode"):
        _COLOR[k] = _COLOR.get(k, 0) | curses.A_REVERSE
    _COLOR["idle"] = curses.A_DIM
    _COLOR["dim"] = curses.A_DIM
    _COLOR["unknown"] = curses.A_DIM


def _attr(key):
    return _COLOR.get(key, 0)


def _live_key(state):
    return {"working": "work", "idle": "idle", "blocked": "blocked", "done": "done",
            "stale": "stale", "dead": "dead"}.get(state, "unknown")


def _pct_key(v):
    if v is None:
        return "dim"
    return "pct_r" if v >= 80 else ("pct_y" if v >= 50 else "pct_g")


# ---------- row builders (return a single segment-line: [(text, color_key), ...]) ----------
def _session_row(s, narrow):
    """Single segment-line per session (PRD §4 v2 — the wide 3-line panel is retired).

    Format: `  [Badge] <slug>  ✨<model> ·<effort>  🧠<ctx%>  5h<r>/7d<r>  ⏳<elapsed>  <liveness>`
    app_server codex appends a dim `⚙app-server` marker right after the badge. Dim rule (§6/§7):
    stale/dead/app_server sessions render telemetry segments dim (last-observed, not live) —
    badge/slug/liveness always keep normal coloring.
    """
    badge = _BADGE_TEXT.get(s.harness, "[?]")
    bkey = _BADGE_KEY.get(s.harness, "head")
    slug = s.slug or (s.cwd.rsplit("/", 1)[-1] if s.cwd else "?")
    live = s.liveness
    lkey = _live_key(live)
    dim_telemetry = live in ("stale", "dead") or s.app_server
    tkey = "dim" if dim_telemetry else None

    segs = [("  ", None), (badge, bkey)]
    if s.app_server:
        segs.append((" ⚙app-server", "dim"))
    segs.append((" " + slug, None))

    model = dash(s.model)
    ctx = dash(s.ctx_pct, lambda v: "%d%%" % v)
    r5 = dash(s.rl_5h, lambda v: "%d%%" % v)
    r7 = dash(s.rl_7d, lambda v: "%d%%" % v)
    el = fmt_min(s.elapsed_min)
    cost = dash(s.cost, lambda v: "$%.2f" % v)

    # narrow drop priority: (1) cost/rl first, (2) then effort, (3) then model.
    # badge/slug/liveness never drop.
    show_cost_rl = not narrow
    show_effort = True
    show_model = True

    if show_model:
        segs.append(("  ✨" + model, tkey if dim_telemetry else "dim"))
        if s.effort and show_effort:
            segs.append((" ·" + s.effort, "dim" if dim_telemetry else _EFFORT_KEY.get(s.effort, "dim")))
    segs.append(("  🧠" + ctx, "dim" if dim_telemetry else _pct_key(s.ctx_pct)))
    if show_cost_rl:
        segs.append(("  5h" + r5 + "/7d" + r7, tkey if dim_telemetry else "dim"))
        segs.append(("  " + cost, "dim"))
    segs.append(("  ⏳" + el, "dim"))
    segs.append(("  " + live, lkey))
    if s.orphan:
        segs.append(("  ⚠worktree-gone", "dead"))
    return segs


def _dispatch_row(j):
    """Single segment-line per dispatch job, placed under the group's dim `dispatch:` label.

    Format: `    ▸<key>▸<stage> (<mode>·<qa>)  ⏳<elapsed>  <liveness>  <slug>`
    """
    key = j.key or "?"
    stage = ("▸" + j.stage) if j.stage else ""
    opts = []
    if j.mode:
        opts.append(j.mode)
    if j.qa:
        opts.append(j.qa)
    optstr = (" (" + "·".join(opts) + ")") if opts else ""
    el = fmt_min(j.elapsed_min)
    lkey = _live_key(j.liveness)
    segs = [("    ▸", "dim"), (key, "head"), (stage, "done")]
    if optstr:
        segs.append((optstr, "dim"))
    segs.append(("  ⏳" + el, "dim"))
    segs.append(("  " + j.liveness, lkey))
    segs.append(("  " + (j.slug or ""), None))
    return segs


# ---------- grouping assembler ----------
def _group_key_session(s):
    return project_of(s.cwd)


def _group_key_job(j):
    # loops jobs (empty cwd, key in the loops vocabulary) always group under "loops" —
    # project_of('') would return '(unknown)', which is wrong for a recognized loop job.
    if not j.cwd and j.key in _LOOPS_KEYS:
        return "loops"
    return project_of(j.cwd)


def _group_sort_key(name, g):
    members_live = [s.liveness for s in g["sessions"]] + [j.liveness for j in g["jobs"]]
    if "working" in members_live:
        activity_rank = 0
    elif "idle" in members_live:
        activity_rank = 1
    else:
        activity_rank = 2
    mtimes = [s.mtime for s in g["sessions"] if s.mtime is not None]
    recency = max(mtimes) if mtimes else None
    # None mtime sorts as oldest (i.e. last) — use a very negative sentinel for the desc sort.
    recency_sort = recency if recency is not None else -1.0
    return (activity_rank, -recency_sort, name)


def _sort_group_sessions(ss):
    return sorted(ss, key=lambda s: (_LIVE_RANK.get(s.liveness, 9), -(s.elapsed_min or 0)))


def _sort_group_jobs(js):
    return sorted(js, key=lambda j: (_JOB_LIVE_RANK.get(j.liveness, 9), -(j.elapsed_min or 0)))


_SHOW_ALL = False   # --all: reveal stale/dead/app_server sessions (folded by default per group)


def set_show_all(v):
    global _SHOW_ALL
    _SHOW_ALL = bool(v)


def _build_lines(sessions, jobs, section, narrow, malformed):
    """Return a flat list of segment-lines for the whole screen (None = blank line).

    Same contract consumed by BOTH `render_once` (plain, full output) and `_draw` (viewport
    slices this same list) — `_OFFSET` must never be read here (see module docstring).
    """
    groups = {}
    for s in sessions:
        gk = _group_key_session(s)
        groups.setdefault(gk, {"sessions": [], "jobs": []})["sessions"].append(s)
    for j in jobs:
        gk = _group_key_job(j)
        groups.setdefault(gk, {"sessions": [], "jobs": []})["jobs"].append(j)

    show_sessions = section in ("fleet", "both")
    show_jobs = section in ("dispatch", "both")

    order = sorted(groups.keys(), key=lambda name: _group_sort_key(name, groups[name]))

    lines = []
    first = True
    for name in order:
        g = groups[name]
        group_sessions = g["sessions"] if show_sessions else []
        group_jobs = g["jobs"] if show_jobs else []
        if not group_sessions and not group_jobs:
            continue    # empty-group suppression per --section: no dangling header

        if not first:
            lines.append(None)
        first = False

        shown = (group_sessions if _SHOW_ALL else
                 [s for s in group_sessions
                  if not (s.liveness in ("stale", "dead") or s.app_server)])
        hidden = len(group_sessions) - len(shown)

        by_harness = {}
        for s in group_sessions:
            by_harness[s.harness] = by_harness.get(s.harness, 0) + 1
        lc = {}
        for s in group_sessions:
            lc[s.liveness] = lc.get(s.liveness, 0) + 1
        counts_str = " ".join("%s%d" % (k[0], lc[k])
                               for k in ("working", "idle", "stale", "dead") if lc.get(k))
        head = "━━ 📁 %s  (%d sessions%s)" % (
            name, len(group_sessions),
            ("  " + counts_str) if counts_str else "",
        )
        lines.append([(head, "head")])

        for s in _sort_group_sessions(shown):
            lines.append(_session_row(s, narrow))
        if group_sessions and hidden:
            lines.append([("  +%d stale/companion hidden" % hidden, "dim")])
        if show_sessions and not group_sessions and group_jobs:
            pass  # session-less group with only dispatch — nothing to say here, jobs follow

        if group_jobs:
            lines.append([("  dispatch:", "dim")])
            for j in _sort_group_jobs(group_jobs):
                lines.append(_dispatch_row(j))

    if not order:
        lines.append([("  (no active sessions or dispatch jobs)", "dim")])

    if malformed:
        lines.append(None)
        lines.append([("  +%d malformed jobs.log rows skipped" % malformed, "dim")])

    return lines


# ---------- plain (--once) ----------
def _plain(segs):
    return "" if segs is None else "".join(t for t, _ in segs)


def render_once(collect_all, hfilter, section):
    sessions, jobs = collect_all(harness_filter=hfilter)
    malformed = _malformed()
    lines = _build_lines(sessions, jobs, section, narrow=False, malformed=malformed)
    out = "\n".join(_plain(l) for l in lines)
    sys.stdout.write(out + "\n")
    return 0


def _malformed():
    try:
        from .collectors import dispatch
        return getattr(dispatch.collect, "last_malformed", 0)
    except Exception:
        return 0


# ---------- curses (live) ----------
def _addline(stdscr, row, segs, w):
    if segs is None:
        return
    col = 0
    for text, color in segs:
        if col >= w - 1:
            break
        piece = text[: (w - 1 - col)]
        try:
            stdscr.addstr(row, col, piece, _attr(color))
        except curses.error:
            pass
        col += len(piece)


_OFFSET = 0                 # scroll offset — READ only in _draw (see module docstring)
_TOGGLE_ROWS = {}            # screen_y -> True, reset at the top of every _draw (mouse click map)


def _clamp_offset(off, total, body_h):
    return max(0, min(off, max(0, total - body_h)))


def reset_scroll():
    global _OFFSET
    _OFFSET = 0


def _draw(stdscr, sessions, jobs, section, malformed):
    global _OFFSET, _TOGGLE_ROWS
    _TOGGLE_ROWS = {}    # reset before any early-return so a stale map never survives a click
    h, w = stdscr.getmaxyx()
    stdscr.erase()
    narrow = w < _NARROW_CUTOFF
    lines = _build_lines(sessions, jobs, section, narrow, malformed)
    body_h = max(1, h - 1)   # reserve 1 footer row
    _OFFSET = _clamp_offset(_OFFSET, len(lines), body_h)

    visible = lines[_OFFSET: _OFFSET + body_h]
    row = 0
    for segs in visible:
        _addline(stdscr, row, segs, w)
        if segs is not None and len(segs) == 1 and "hidden" in segs[0][0]:
            _TOGGLE_ROWS[row] = True
        row += 1

    above = _OFFSET
    below = max(0, len(lines) - body_h - _OFFSET)
    parts = []
    if above:
        parts.append("↑%d" % above)
    if below:
        parts.append("↓%d" % below)
    hint = "q quit · r refresh · a all · ↑↓/jk PgUp/Dn g/G · click +N"
    footer = ("  " + " ".join(parts) + ("  " if parts else "") + hint)
    try:
        stdscr.addstr(h - 1, 0, footer[: w - 1], _attr("dim"))
    except curses.error:
        pass
    stdscr.noutrefresh()
    curses.doupdate()


def _loop(stdscr, collect_all, hfilter, section, interval):
    global _OFFSET
    curses.curs_set(0)
    _init_colors()
    try:
        curses.mousemask(curses.BUTTON1_CLICKED)
    except Exception:
        pass
    stdscr.timeout(200)                     # getch blocks ≤200ms → responsive keys
    sessions, jobs = collect_all(harness_filter=hfilter)
    malformed = _malformed()
    last = time.time()
    _draw(stdscr, sessions, jobs, section, malformed)
    while True:
        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q")):
            return 0
        h, w = stdscr.getmaxyx()
        body_h = max(1, h - 1)
        if ch in (curses.KEY_UP, ord("k")):
            _OFFSET -= 1
        elif ch in (curses.KEY_DOWN, ord("j")):
            _OFFSET += 1
        elif ch == curses.KEY_PPAGE:
            _OFFSET -= body_h
        elif ch == curses.KEY_NPAGE:
            _OFFSET += body_h
        elif ch in (curses.KEY_HOME, ord("g")):
            _OFFSET = 0
        elif ch in (curses.KEY_END, ord("G")):
            _OFFSET = 1 << 30    # clamp in _draw resolves this to maxoff
        elif ch in (ord("a"), ord("A")):
            set_show_all(not _SHOW_ALL)
        elif ch == curses.KEY_MOUSE:
            try:
                _, mx, my, _mz, _bstate = curses.getmouse()
            except Exception:
                my = None
            if my is not None and my in _TOGGLE_ROWS:
                set_show_all(not _SHOW_ALL)
        # KEY_RESIZE: no special handling needed — _draw's clamp re-clamps against the new
        # body_h below; do NOT reset _OFFSET here (would destroy scroll position).

        force = ch in (ord("r"), ord("R"))
        now = time.time()
        if force or (now - last) >= interval:
            sessions, jobs = collect_all(harness_filter=hfilter)
            malformed = _malformed()
            last = now
        # redraw every wake (covers KEY_RESIZE and tick) — _draw clamps _OFFSET internally.
        _draw(stdscr, sessions, jobs, section, malformed)


def run_live(collect_all, hfilter, section, interval):
    if not sys.stdout.isatty():
        sys.stderr.write("fleet: stdout is not a TTY — use --once (snapshot) or --json.\n")
        return 1
    try:
        return curses.wrapper(_loop, collect_all, hfilter, section, interval)
    except KeyboardInterrupt:
        return 0
    except Exception as e:  # pragma: no cover
        sys.stderr.write("fleet: curses failed: %s\n" % e)
        return 1
