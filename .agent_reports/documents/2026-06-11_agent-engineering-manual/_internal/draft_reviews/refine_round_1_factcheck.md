# Fact-Check — refine round 1 (v2 변경 절 한정)

검토 기준일: 2026-06-11
검토 범위: frontmatter changelog v2 명시 8건 (§1.5 / §3.2 / §3.5/3.7/3.9 / §2.4·§3.6 oncall 항목 / §1.0 Karpathy / §1.3 Rust / §1.2/§1.4-T4 — 마지막은 memo 제거만이라 표에서 생략)

| Section | Claim | Source | Match | Severity |
|---|---|---|---|---|
| §1.5 | "Claude Code users approve **93%** of permission prompts" — L1 수치 | `anthropic-claude-code-auto-mode` card verbatim: "Claude Code users approve 93% of permission prompts" | ✅ | — |
| §1.5 | auto-mode classifier **17% false-negative** — L2 수치 | `anthropic-claude-code-auto-mode` card verbatim: "real overeager action에 대해 17% false-negative rate" | ✅ | — |
| §1.5 | "sandboxing safely reduces permission prompts by **84%**" — L3 수치 | `anthropic-claude-code-sandboxing` card verbatim: "sandboxing safely reduces permission prompts by 84%" | ✅ | — |
| §1.5 | 4층 구성 L1 permission → L2 classifier → L3 sandbox → L4 hook 이 `05_deployment.md §1` 과 일치하는가 | `05_deployment.md §1` 표: L1 Permission / L2 Auto mode classifier / L3 Sandboxing / L4 Hook gate — 동일 4층, 동일 순서, 동일 정량 귀속 | ✅ | — |
| §1.5 | L4 hook 귀속 카드가 draft에서 `[anthropic-claude-code-auto-mode]`·`[anthropic-claude-code-sandboxing]` 양쪽인데, `05_deployment §1` 표에서 L4는 `[anthropic-claude-code-best-practices]` 귀속 | draft §1.5 본문에서 L4 hook을 명시 인용하지 않고 "hook gate(deterministic 강제)"로만 서술 — 카드 귀속 차이는 draft가 L4를 명시 card 없이 표기했기 때문. 05_deployment 표와 비교 시 L4 카드(`[anthropic-claude-code-best-practices]`)가 §1.5 본문에 빠져 있음 | 🟡 | low — 누락이지 오류 아님; §1.5 본문에 L4 카드 귀속이 없어 추적 불완전 |
| §1.0 | "Osmani 가 인용한 한 줄('One analysis quipped:')" 표현으로 Karpathy 직접 귀속 완화 | `osmani-context-engineering` card Generation Mapping 섹션: "One analysis quipped: Prompt engineering walked so context engineering could run." — section title이 "Karpathy/quip"으로 표기; body에서 출처를 한 분석으로만 돌림. draft의 "카드는 Karpathy 풍 quip 으로 표기하나 원문은 출처를 한 분석으로만 돌려" 서술이 카드 내 section title vs body 불일치를 정확히 포착 | ✅ | — |
| §1.3 | C compiler가 "**Rust 기반**" | `anthropic-c-compiler-parallel-claudes` card Core Claims 1: "100,000줄 **Rust 기반** C compiler를 구축" verbatim 일치 | ✅ | — |
| §2.4 / §3.6 | "당직(oncall) **항목 8**(디스패치 job 현황)" | `~/.claude/loops/oncall.md` 점검 항목 번호 직접 확인: 항목 8 = "디스패치 job 현황 (`~/.claude/.dispatch/jobs.log`)" — 정확히 일치 | ✅ | — |
| §3.2 | 발화 예시 표 4트랙이 `CLAUDE.md §0(B)` 워크플로우 맵과 부합하는가 | CLAUDE.md 워크플로우 맵: 📄 문서(autopilot-draft) / 🔬 연구·실험(autopilot-research→spec→code→lab) / 💻 앱(autopilot-spec→design→code→ship) / 📦 라이브러리(autopilot-spec→code). Draft 표: "논문 정리" → autopilot-research(연구) / "문서 써줘" → autopilot-draft(문서) / "X 기능" → autopilot-spec→code(앱/라이브러리) / "실험 돌려줘" → autopilot-lab(연구·실험). 네 트랙 모두 맵과 정합 | ✅ | — |
| §3.2 | `analyze-project` → "즉시 invoke" (컨펌 없이) | `CLAUDE.md §0(B)` 발화 분류: "작은 (`audit`/`post-it`/`analyze-project`) → 즉시 invoke" verbatim 일치 | ✅ | — |
| §3.5 | 기대 산출물 경로: `.agent_reports/plans/{date}_{slug}/` | `CLAUDE.md §0(0b)` 버전 자리 표: `plans/<date>_<slug>/` — 일치. 실물 경로 포맷 동일 | ✅ | — |
| §3.7 | 기대 산출물 경로: `~/.claude/loops/drill/cases/` | `~/.claude/loops/drill/cases/` 실물 확인: g0~g5 케이스 디렉토리 실재 ✅ | ✅ | — |
| §3.9 | 기대 산출물 경로: `notes/study/<date>.md` | `~/.claude/loops/README.md` 연수 행: `notes/study/<date>.md` — 정의 일치. 단 `/home/nas/user/Uihyeop/notes/study/` 디렉토리가 현재 미존재(연수 미실행) — 경로 정의는 맞으나 실물 없음 | 🟡 | low — 루프 미실행 상태로 경로 자체는 README 기준 정확; "기대 산출물" 표현이 미래형이므로 허용 범위 |

## 종합

- 오류(❌): 0건
- 주의(🟡): 2건
  1. §1.5 L4 hook 카드 귀속 누락 — 05_deployment §1은 `[anthropic-claude-code-best-practices]`를 명시하나 draft §1.5 본문에 빠짐. 수정 필요성 낮음(문맥상 L4 설명은 충분).
  2. §3.9 `notes/study/` 디렉토리 미존재 — 연수 루프 미실행으로 인한 것이며 경로 정의 자체는 올바름.
- 전체 pass: 수치(93%/17%/84%) 3종, 4층 구조, Karpathy 귀속 완화 표현, Rust 명시, oncall 항목 8 번호, 4트랙 발화 매핑, 즉시 invoke 분류, 산출물 경로 3종 모두 원천과 일치.
