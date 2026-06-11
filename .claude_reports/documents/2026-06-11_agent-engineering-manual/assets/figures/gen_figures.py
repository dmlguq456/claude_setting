#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
에이전트 엔지니어링 매뉴얼 — 신규 도식 F1~F7 생성 (figure-gen).

ground truth:
  F1 세대 타임라인  ← research/analysis_summary.md §1 (Gen0~3) + §4 timeline
  F2 패턴×세대 매트릭스 ← analysis_summary.md §2 실무 패턴 + §1 세대 파생
  F3 안전장치 4층    ← research/05_deployment.md §1 (L1 permission 93% / L2 classifier 17%FN / L3 sandbox 84% / L4 hook)
  F4 4트랙 파이프    ← ~/.claude/CLAUDE.md 워크플로우 맵 (research→spec→code 하드 순서)
  F5 팀 분업 매트릭스 ← ~/.claude/CONVENTIONS.md §2 model 매트릭스 + §1.1 QA 5단계
  F6 루프 4계층      ← ~/.claude/loops/README.md 계층 표 (L1초/L2분/L3일/L4주)
  F7 하루 일과 흐름   ← loops/README.md 현역 4종 cron 시간표

디자인 강제 (사용자 feedback):
  - many-to-many (F2·F5) = 매트릭스/히트맵 (노드-엣지 금지)
  - 파이프라인 (F1·F3·F4·F6·F7) = 단방향 레인 (좌→우 또는 상→하, 역방향·교차 금지)
  - 한글 라벨 = Noto Sans CJK KR
  - DPI 200, 가로 ~2000px
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np
import os

# ---- 한글 폰트 ----
KR_FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(KR_FONT)
_kr = fm.FontProperties(fname=KR_FONT)
plt.rcParams["font.family"] = _kr.get_name()
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
DPI = 200

# ---- palette (user_profile 01 역할색 차용, 도식용 톤다운) ----
C_PROMPT  = "#A5A5A5"   # gray  — gen0 배경
C_CONTEXT = "#4472C4"   # blue
C_HARNESS = "#548235"   # green (encoder green)
C_LOOP    = "#ED7D31"   # orange (decoder orange)
C_RED     = "#C00000"   # novelty red 강조
C_GOLD    = "#FFC000"   # zoom gold
C_INK     = "#222222"
C_FILL    = "#FFFFFF"
GEN_COLORS = [C_PROMPT, C_CONTEXT, C_HARNESS, C_LOOP]


def _save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", p)


# ======================================================================
# F1 — 세대 4단 누적 타임라인 (단방향 레인, 좌→우)
# ======================================================================
def f1():
    gens = [
        ("Gen 0\nprompt", "~2024", "단일 prompt phrasing", C_PROMPT),
        ("Gen 1\ncontext", "2025", "context rot · attention budget\ncompaction · just-in-time", C_CONTEXT),
        ("Gen 2\nharness", "2025–26", "Agent = Model + Harness\nTrivedy coined", C_HARNESS),
        ("Gen 3\nloop", "2026", "스스로를 prompt 에서 교체\nOsmani 명명", C_LOOP),
    ]
    fig, ax = plt.subplots(figsize=(11.0, 4.3))
    n = len(gens)
    x0, w, gap = 0.4, 2.05, 0.55
    ytop, h = 2.7, 1.5
    # 누적 layer 띠 (아래에 깔린 배경 — 각 세대가 이전 세대를 감싼다)
    for i in range(n):
        x = x0 + i * (w + gap)
        # 누적 표현: i 세대는 0..i 까지 layer 를 품는다 (얇은 stack)
        for j in range(i + 1):
            yb = 0.35 + j * 0.16
            ax.add_patch(Rectangle((x - 0.05, yb), w + 0.1, 0.13,
                                   facecolor=GEN_COLORS[j], edgecolor="none", alpha=0.55))
        ax.text(x + w / 2, 0.18, "누적 layer  loop⊃harness⊃context⊃prompt" if i == n - 1 else "",
                ha="center", va="center", fontsize=8.5, color=C_INK, style="italic")
        # 메인 카드
        box = FancyBboxPatch((x, ytop), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                             linewidth=2.0, edgecolor=gens[i][3], facecolor=C_FILL, zorder=3)
        ax.add_patch(box)
        ax.text(x + w / 2, ytop + h - 0.34, gens[i][0], ha="center", va="center",
                fontsize=13, fontweight="bold", color=gens[i][3], zorder=4)
        ax.text(x + w / 2, ytop + h - 0.92, gens[i][1], ha="center", va="center",
                fontsize=9.5, color=C_INK, zorder=4)
        ax.text(x + w / 2, ytop + 0.34, gens[i][2], ha="center", va="center",
                fontsize=8.3, color="#444444", zorder=4)
        # 단방향 화살표 (좌→우, 미해결분 흡수)
        if i < n - 1:
            xa = x + w
            arr = FancyArrowPatch((xa + 0.02, ytop + h / 2), (xa + gap - 0.02, ytop + h / 2),
                                  arrowstyle="-|>", mutation_scale=18, linewidth=2.0,
                                  color=C_INK, zorder=5)
            ax.add_patch(arr)
            ax.text(xa + gap / 2, ytop + h / 2 + 0.28, "미해결분\n흡수", ha="center", va="center",
                    fontsize=6.8, color="#666666", zorder=5)
    ax.text(x0, 4.78, "F1 · 원칙의 세대사 — 각 세대는 이전 세대 위에 누적되는 layer",
            ha="left", va="center", fontsize=11, fontweight="bold", color=C_INK)
    ax.set_xlim(0, x0 + n * (w + gap))
    ax.set_ylim(0, 5.05)
    ax.axis("off")
    _save(fig, "f1_generations_timeline.png")


# ======================================================================
# F2 — 패턴 11종 × 세대 매트릭스 (heatmap, many-to-many)
# ======================================================================
def f2():
    patterns = [
        "P1 plan-then-execute", "P2 spec-driven", "P3 maker-verifier",
        "P4 서브에이전트", "P5 파이프라인 세분화", "P6 golden set",
        "P7 오답노트 승격", "P8 상태·산출물 소통", "P9 worktree",
        "P10 headless·cron", "P11 컨텍스트 절약",
    ]
    gens = ["prompt\n(Gen0)", "context\n(Gen1)", "harness\n(Gen2)", "loop\n(Gen3)"]
    # 2 = 주 파생 세대, 1 = 연관(걸침), 0 = 무관
    # ground truth: analysis_summary §1 세대 + §2 패턴 출처 세대
    M = np.array([
        [1, 0, 2, 1],  # P1 plan — harness 정초(building effective agents) 주, loop 로 확장
        [0, 1, 2, 1],  # P2 spec — harness 주, context/loop 걸침
        [0, 1, 2, 2],  # P3 maker-verifier — 여러 갈래 수렴 (harness+loop)
        [0, 1, 2, 1],  # P4 서브에이전트 — harness(orchestrator-worker) 주
        [0, 0, 2, 1],  # P5 파이프라인 — harness(prompt chaining) 주
        [0, 0, 1, 2],  # P6 golden set — loop/eval 주
        [0, 1, 1, 2],  # P7 오답노트 — loop(failure-driven) 주, context delta 걸침
        [0, 2, 2, 1],  # P8 상태·산출물 — context+harness 외재화 주
        [0, 0, 1, 2],  # P9 worktree — loop 병렬 주
        [0, 0, 1, 2],  # P10 headless·cron — loop 주
        [0, 2, 1, 0],  # P11 컨텍스트 절약 — context 주
    ])
    fig, ax = plt.subplots(figsize=(7.4, 7.0))
    cmap = matplotlib.colors.ListedColormap(["#F2F2F2", "#BFD3B0", C_HARNESS])
    ax.imshow(M, cmap=cmap, aspect="auto", vmin=0, vmax=2)
    # 셀 표식
    sym = {0: "", 1: "○", 2: "●"}
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            col = "white" if v == 2 else ("#3a5a28" if v == 1 else "#cccccc")
            ax.text(j, i, sym[v], ha="center", va="center", fontsize=14, color=col)
    ax.set_xticks(range(len(gens)))
    ax.set_xticklabels(gens, fontsize=9.5)
    ax.set_yticks(range(len(patterns)))
    ax.set_yticklabels(patterns, fontsize=9.5)
    ax.set_xticks(np.arange(-0.5, len(gens), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(patterns), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2.2)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("F2 · 패턴 11종이 어느 세대에서 파생했나\n●=주 파생 세대  ○=연관(걸침)  — maker-verifier(P3)는 harness·loop 두 갈래 수렴",
                 fontsize=10.5, fontweight="bold", pad=12, loc="left")
    _save(fig, "f2_pattern_generation_matrix.png")


# ======================================================================
# 단방향 세로 레인 헬퍼 (상→하)
# ======================================================================
def _vlane(ax, layers, x_center, w, top, dh, gap, title_color=C_INK):
    """layers: list of (title, sub, color, side_note)"""
    y = top
    boxes = []
    for (title, sub, color, note) in layers:
        box = FancyBboxPatch((x_center - w / 2, y - dh), w, dh,
                             boxstyle="round,pad=0.02,rounding_size=0.10",
                             linewidth=2.0, edgecolor=color, facecolor=C_FILL, zorder=3)
        ax.add_patch(box)
        ax.text(x_center, y - dh * 0.36, title, ha="center", va="center",
                fontsize=11.5, fontweight="bold", color=color, zorder=4)
        if sub:
            ax.text(x_center, y - dh * 0.74, sub, ha="center", va="center",
                    fontsize=8.4, color="#444444", zorder=4)
        if note:
            ax.text(x_center + w / 2 + 0.18, y - dh / 2, note, ha="left", va="center",
                    fontsize=8.0, color=C_RED, zorder=4)
        boxes.append((y, y - dh))
        y -= (dh + gap)
    # 단방향 하향 화살표
    for i in range(len(layers) - 1):
        ya = boxes[i][1]
        arr = FancyArrowPatch((x_center, ya - 0.02), (x_center, ya - gap + 0.02),
                              arrowstyle="-|>", mutation_scale=16, linewidth=2.0,
                              color=C_INK, zorder=5)
        ax.add_patch(arr)
    return y


# ======================================================================
# F3 — 자율 실행 안전장치 4층 (단방향 레인, 상→하)
# ======================================================================
def f3():
    layers = [
        ("L1 · Permission prompt", "per-action 승인", C_PROMPT, "93% 승인\n→ 마찰만"),
        ("L2 · Auto mode classifier", "intent-alignment 판정", C_CONTEXT, "17% FN\n(false-negative)"),
        ("L3 · Sandboxing", "filesystem + network\nhard boundary", C_HARNESS, "84% prompt\n감소"),
        ("L4 · Hook gate", "deterministic 강제\n(advisory 아님)", C_GOLD, "통과 전\nturn 차단"),
    ]
    fig, ax = plt.subplots(figsize=(8.2, 7.0))
    x = 3.0
    yend = _vlane(ax, layers, x_center=x, w=3.6, top=6.4, dh=1.05, gap=0.55)
    # 자율성 축 (왼쪽 화살표 — soft→hard)
    arr = FancyArrowPatch((0.55, 6.2), (0.55, yend + 0.35),
                          arrowstyle="-|>", mutation_scale=16, linewidth=2.2, color="#888888")
    ax.add_patch(arr)
    ax.text(0.3, (6.2 + yend) / 2, "자율성 ↑\nsoft → hard boundary", ha="center", va="center",
            rotation=90, fontsize=9, color="#666666")
    # 최종 도착
    ax.text(x, yend + 0.05, "→  자율 실행", ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=C_INK)
    ax.set_title("F3 · 자율 실행 안전장치 4층 — 자율성 ↑ 일수록 hard boundary 로 무게 이동\n(out: research/05_deployment.md §1)",
                 fontsize=10.5, fontweight="bold", loc="left", pad=10)
    ax.set_xlim(0, 6.0)
    ax.set_ylim(yend - 0.3, 7.0)
    ax.axis("off")
    _save(fig, "f3_safety_layers.png")


# ======================================================================
# F4 — 4트랙 파이프 구조도 (단방향 레인, 좌→우 4 레인 + 공통 하드 게이트)
# ======================================================================
def f4():
    # NOTE: '↻'(반복) 글리프가 Noto Sans CJK 에 없어 □ 깨짐 → "(반복)" ASCII 라벨로 폴백
    tracks = [
        ("문서", ["research /\nanalyze-project", "autopilot-draft", "autopilot-refine\n(반복)", "autopilot-apply"], C_CONTEXT),
        ("연구·실험", ["research", "autopilot-spec\n(반복)", "autopilot-code\n(반복)", "autopilot-lab\n(반복)"], C_HARNESS),
        ("앱", ["autopilot-spec\n(반복)", "autopilot-design", "autopilot-code\n(반복)", "autopilot-ship\n(반복)"], C_LOOP),
        ("라이브러리·CLI", ["analyze-project", "autopilot-spec\n(반복)", "autopilot-code\n(반복)", "—"], C_GOLD),
    ]
    fig, ax = plt.subplots(figsize=(12.0, 6.4))
    n_tracks = len(tracks)
    n_stage = 4
    x0, sw, sgap = 1.9, 2.25, 0.45
    ytop, rh, rgap = 5.6, 1.05, 0.40
    for ti, (tname, stages, col) in enumerate(tracks):
        y = ytop - ti * (rh + rgap)
        ax.text(x0 - 0.25, y - rh / 2, tname, ha="right", va="center",
                fontsize=11, fontweight="bold", color=col)
        for si, st in enumerate(stages):
            x = x0 + si * (sw + sgap)
            empty = (st == "—")
            box = FancyBboxPatch((x, y - rh), sw, rh,
                                 boxstyle="round,pad=0.02,rounding_size=0.08",
                                 linewidth=1.8, edgecolor=("#cccccc" if empty else col),
                                 facecolor=("#FAFAFA" if empty else C_FILL), zorder=3)
            ax.add_patch(box)
            ax.text(x + sw / 2, y - rh / 2, st, ha="center", va="center",
                    fontsize=8.6, color=("#bbbbbb" if empty else C_INK), zorder=4)
            if si < n_stage - 1 and not empty and stages[si + 1] != "—":
                arr = FancyArrowPatch((x + sw + 0.02, y - rh / 2), (x + sw + sgap - 0.02, y - rh / 2),
                                      arrowstyle="-|>", mutation_scale=13, linewidth=1.6,
                                      color="#555555", zorder=5)
                ax.add_patch(arr)
    # 공통 하드 순서 게이트 띠 (상단)
    ax.text(x0, 6.25, "F4 · autopilot 4트랙 파이프 — research → spec → code 하드 순서 게이트 (앞 산출물 없이 다음 단계 진입 금지)",
            ha="left", va="center", fontsize=11, fontweight="bold", color=C_INK)
    ax.text(x0, 5.95, "하드 게이트:  research / analyze (산출물)  ▶  spec (spec/)  ▶  code (plans/)   — hooks/artifact-guard.sh 가 생성 순서 강제",
            ha="left", va="center", fontsize=8.6, color=C_RED, style="italic")
    ybot = ytop - (n_tracks - 1) * (rh + rgap) - rh
    ax.set_xlim(0, x0 + n_stage * (sw + sgap))
    ax.set_ylim(ybot - 0.2, 6.45)
    ax.axis("off")
    _save(fig, "f4_four_track_pipeline.png")


# ======================================================================
# F5 — 팀 분업 매트릭스 (heatmap, 팀 × 역할)
# ======================================================================
def f5():
    teams = ["기획팀", "개발팀", "품질관리팀", "연구팀", "편집팀", "디자인팀", "자료팀", "codex-review"]
    roles = ["maker\n(생성)", "verifier\n(검증)", "fact-check", "보조\n(자료·시각)"]
    # 2 = 주 역할, 1 = 부 역할, 0 = 없음
    # ground truth: CONVENTIONS §2 model 매트릭스 + §1.1 QA reviewer 구성
    M = np.array([
        [2, 0, 0, 0],  # 기획팀 — maker (plan)
        [2, 0, 0, 0],  # 개발팀 — maker (code)
        [0, 2, 1, 0],  # 품질관리팀 — verifier (review/test/security)
        [1, 2, 2, 1],  # 연구팀 — claim-verify(verifier)+fact-check, research maker 보조
        [1, 1, 2, 0],  # 편집팀 — 다듬기(maker)+fact·표기 검증
        [1, 1, 0, 2],  # 디자인팀 — UI maker + 시각 보조
        [0, 0, 1, 2],  # 자료팀 — 자료·figure 보조 + 수치 검증
        [0, 2, 0, 0],  # codex-review — 외부 adversarial verifier
    ])
    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    cmap = matplotlib.colors.ListedColormap(["#F2F2F2", "#F6D9B0", C_LOOP])
    ax.imshow(M, cmap=cmap, aspect="auto", vmin=0, vmax=2)
    sym = {0: "", 1: "○", 2: "●"}
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            col = "white" if v == 2 else ("#9a5a1f" if v == 1 else "#cccccc")
            ax.text(j, i, sym[v], ha="center", va="center", fontsize=14, color=col)
    ax.set_xticks(range(len(roles)))
    ax.set_xticklabels(roles, fontsize=9.3)
    ax.set_yticks(range(len(teams)))
    ax.set_yticklabels(teams, fontsize=10)
    ax.set_xticks(np.arange(-0.5, len(roles), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(teams), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2.2)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("F5 · 팀 × 역할 매트릭스 — maker / verifier 분리\n●=주 역할  ○=부 역할  (out: CONVENTIONS.md §2 · §1.1)",
                 fontsize=10.5, fontweight="bold", pad=12, loc="left")
    _save(fig, "f5_team_matrix.png")


# ======================================================================
# F6 — 루프 4계층 (단방향 레인, 상→하, 초→분→일→주)
# ======================================================================
def f6():
    layers = [
        ("L1 · 에이전트 루프", "초 · LLM→도구→반복 (벤더 영역)\nClaude Code 자체 — 소비만", C_PROMPT, ""),
        ("L2 · 과제 루프", "분 · 한 작업 안 생성↔검증\n(maker/verifier · QA 라운드)", C_CONTEXT, ""),
        ("L3 · 작업 루프", "일 · 세션 밖 발견·분사·기록\n당직(oncall) · 일지(note)", C_HARNESS, "cron+\nheadless"),
        ("L4 · 메타 루프", "주 · 시스템 자체 시험·개선\n모의훈련(drill) · 연수(study)", C_LOOP, ""),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 7.0))
    x = 3.2
    yend = _vlane(ax, layers, x_center=x, w=4.4, top=6.4, dh=1.05, gap=0.55)
    # 주기 축 (왼쪽)
    arr = FancyArrowPatch((0.55, 6.2), (0.55, yend + 0.55),
                          arrowstyle="-|>", mutation_scale=16, linewidth=2.2, color="#888888")
    ax.add_patch(arr)
    ax.text(0.3, (6.2 + yend) / 2, "주기  초 → 분 → 일 → 주", ha="center", va="center",
            rotation=90, fontsize=9, color="#666666")
    ax.set_title("F6 · 루프 4계층 — 같은 모양(행동→검증→조정)이 네 박자로 돈다\n(out: ~/.claude/loops/README.md 계층 표)",
                 fontsize=10.5, fontweight="bold", loc="left", pad=10)
    ax.set_xlim(0, 6.2)
    ax.set_ylim(yend - 0.2, 7.0)
    ax.axis("off")
    _save(fig, "f6_loop_layers.png")


# ======================================================================
# F7 — 하루 일과 흐름 (단방향 레인, 좌→우 timeline)
# ======================================================================
def f7():
    steps = [
        ("일지\n(note)", "cron 05:03", "전날 산출물\nL2 노트화", C_CONTEXT),
        ("당직\n(oncall)", "cron 05:37", "야간 순찰\n이상 발견·보고", C_HARNESS),
        ("아침 처리", "사용자 발화", "당직 보고\ntriage·실행", C_GOLD),
        ("작업 디스패치", "낮", "autopilot 파이프\nworktree 분사", C_INK),
        ("모의훈련\n(drill)", "지침 수정 후", "fixture 시험\n채점·FAIL 수정", C_RED),
        ("연수\n(study)", "일요일 06:17", "외부 동향 ×\n세팅 → 제안서", C_LOOP),
    ]
    fig, ax = plt.subplots(figsize=(13.0, 3.9))
    n = len(steps)
    x0, w, gap = 0.4, 1.85, 0.55
    ytop, h = 1.6, 1.55
    for i, (title, when, what, col) in enumerate(steps):
        x = x0 + i * (w + gap)
        box = FancyBboxPatch((x, ytop), w, h, boxstyle="round,pad=0.02,rounding_size=0.10",
                             linewidth=2.0, edgecolor=col, facecolor=C_FILL, zorder=3)
        ax.add_patch(box)
        ax.text(x + w / 2, ytop + h - 0.32, title, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color=col, zorder=4)
        ax.text(x + w / 2, ytop + h - 0.82, when, ha="center", va="center",
                fontsize=8.2, color="#666666", zorder=4)
        ax.text(x + w / 2, ytop + 0.32, what, ha="center", va="center",
                fontsize=8.0, color="#444444", zorder=4)
        if i < n - 1:
            xa = x + w
            arr = FancyArrowPatch((xa + 0.02, ytop + h / 2), (xa + gap - 0.02, ytop + h / 2),
                                  arrowstyle="-|>", mutation_scale=15, linewidth=1.9,
                                  color="#555555", zorder=5)
            ax.add_patch(arr)
    ax.text(x0, 3.55, "F7 · 하루 일과 흐름 — 새벽 cron → 아침 처리 → 작업 → 지침 수정 후 모의훈련 → 일요일 연수",
            ha="left", va="center", fontsize=11, fontweight="bold", color=C_INK)
    ax.text(x0, 3.25, "새벽 시간표: 05:03 일지 → 05:37 당직 (충돌 방지 간격)", ha="left", va="center",
            fontsize=8.6, color="#666666", style="italic")
    ax.set_xlim(0, x0 + n * (w + gap))
    ax.set_ylim(0.9, 3.75)
    ax.axis("off")
    _save(fig, "f7_daily_flow.png")


if __name__ == "__main__":
    f1(); f2(); f3(); f4(); f5(); f6(); f7()
    print("done")
