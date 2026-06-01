#!/usr/bin/env python3
# PreToolUse gate — spec-backed 프로젝트에서 .claude_reports/ 밖 소스 파일의
# Edit/Write 를, spec-first 파이프(WORKFLOW §7)를 안 거친 채로 하려 하면 'ask' 로 가로챈다.
# 목적: CLAUDE.md §9 / WORKFLOW §7 의 "ad-hoc 직접 Edit 금지"를 reminder(soft)에서
#       실제 gate(hard)로 승격. 새 세션에서 즉시-Edit 하는 경로 자체를 막는다.
#
# 등록: ~/.claude/settings.json hooks.PreToolUse, matcher "Edit|Write|MultiEdit|NotebookEdit".
# fail-open: 어떤 예외든 통과(allow) — gate 가 사용자의 편집 능력을 brick 하지 않게.
#
# 통과(ask 안 함) 조건:
#   - cwd(및 상위)에 spec-backed 프로젝트 없음 → 일반 작업, 무관
#   - 타겟이 .claude_reports/ 내부 → 파이프 산출물 자체(plan/log/spec) 작성은 정상
#   - 오늘자 active plan 폴더(plans/*/<today>_*) 존재 → 이미 파이프 사이클 중
# 그 외(spec-backed + 소스 밖 + 파이프 미경유) → permissionDecision: ask + 사유.
import json, sys, os, glob, datetime


def allow():
    # 출력 없이 종료 = 기존 권한 흐름 그대로(허용). gate 가 끼어들지 않음.
    sys.exit(0)


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))
    sys.exit(0)


def find_spec_root(start):
    """cwd 에서 위로 올라가며 .claude_reports/spec/*/pipeline_state.yaml 보유 dir 탐색.
    서브디렉토리에서 세션을 열어도 프로젝트 루트를 찾도록(cwd 스코핑 취약점 보정)."""
    d = os.path.abspath(start)
    home = os.path.expanduser("~")
    for _ in range(40):  # 무한 루프 backstop
        if glob.glob(os.path.join(d, ".claude_reports", "spec", "*", "pipeline_state.yaml")):
            return d
        parent = os.path.dirname(d)
        if parent == d or d == home:  # 파일시스템 루트 / 홈 경계에서 멈춤
            return None
        d = parent
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        allow()

    tool = data.get("tool_name", "")
    if tool not in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        allow()

    cwd = data.get("cwd") or os.getcwd()
    ti = data.get("tool_input", {}) or {}
    fpath = ti.get("file_path") or ti.get("notebook_path") or ""

    root = find_spec_root(cwd)
    if not root:
        allow()  # spec-backed 아님 → 무관

    reports = os.path.join(root, ".claude_reports")
    abspath = fpath if os.path.isabs(fpath) else os.path.join(cwd, fpath)
    abspath = os.path.normpath(abspath)
    # 타겟이 .claude_reports/ 내부면 통과(파이프 산출물 작성은 정상 흐름)
    if abspath == reports or abspath.startswith(reports + os.sep):
        allow()

    # 오늘자 active plan 폴더가 있으면 이미 파이프 사이클 중 → 통과
    today = datetime.date.today().strftime("%Y-%m-%d")
    if glob.glob(os.path.join(reports, "plans", "*", today + "_*")):
        allow()

    proj = os.path.basename(os.path.dirname(
        glob.glob(os.path.join(reports, "spec", "*", "pipeline_state.yaml"))[0]))
    ask(
        f"⚠️ spec-backed 프로젝트 '{proj}' 의 .claude_reports/ 밖 소스 수정입니다.\n"
        f"WORKFLOW §7 (spec-first) 미경유 — ad-hoc 직접 Edit 은 금지. 순서: "
        f"(0) 기존 산출물 파악 → (1) spec-drift 체크: spec-significant 면 autopilot-spec update "
        f"(prd 갱신+versioning) → (2) autopilot-code --qa quick 경유(plans/{proj}/ 에 기록).\n"
        f"→ 순수 typo·1줄 포맷이면 승인. 기능·구조 변경이면 거부하고 파이프로 전환하세요."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        allow()  # fail-open
