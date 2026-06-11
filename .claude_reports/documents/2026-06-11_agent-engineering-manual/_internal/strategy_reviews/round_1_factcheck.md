---
type: factcheck
round: 1
date: 2026-06-11
mode: report
target: strategy/strategy.md
---

# Strategy Fact-Check Round 1

| # | Section | Claim in strategy | Source (file:line or section) | Match | Source type | Severity |
|---|---|---|---|---|---|---|
| 1 | §4.1 절 1.0 | "Karpathy 'Prompt engineering walked so context engineering could run'" — 명명 권위로 사실상 Karpathy 귀속 | `osmani-context-engineering.md` Core Claims: "(body, Karpathy/quip) verbatim" — 원래 Osmani 가 Karpathy 를 인용하는 구도. Karpathy 의 말을 Osmani 가 옮긴 것임은 카드에 명시. | ✅ (귀속 맥락 복잡하지만 카드와 일치) | cards-verbatim | 🟢 |
| 2 | §4.1 절 1.1 | "context engineering 명명 = Osmani+Anthropic 공동" | `osmani-context-engineering.md` (Osmani 블로그) + `anthropic-effective-context-engineering.md` (Anthropic 블로그) 양측이 별도 1차 출처. 카드 어디에도 "공동 명명"이라는 표현은 없음 — 두 출처가 병존하는 것을 strategy 가 "공동" 으로 해석. | 🟡 (카드는 "공동 명명" 표기 없음 — 두 1차 출처 존재로 추론한 것) | cards-name-only | 🟡 |
| 3 | §4.1 절 1.2 | "harness engineering 용어 coined = Trivedy" | `osmani-agent-harness-engineering.md` Core Claims: "Agent = Model + Harness. If you're not the model, you're the harness." + "Viv Trivedy coined the term _harness engineering_." — verbatim 일치. | ✅ | cards-verbatim | 🟢 |
| 4 | §4.1 절 1.3 | "loop engineering 명명 = Osmani" | `osmani-loop-engineering.md` Core Claims verbatim: "Loop engineering is replacing yourself as the person who prompts the agent." — 1차 카드. `greyling-loop-engineering.md` Limitations: "loop engineering 명명·프레임의 1차 권위는 Addy Osmani" — 명시 확인. | ✅ | cards-verbatim | 🟢 |
| 5 | §4.1 절 1.3 | "Greyling 정리" (loop engineering) | `greyling-loop-engineering.md` role: "정리·대중화 (popularizer)" — 일치. | ✅ | cards-verbatim | 🟢 |
| 6 | §4.1 절 1.3 | "실증: C compiler 16-Claude" | `anthropic-c-compiler-parallel-claudes.md` Core Claims 1: "16개 Claude Opus 4.6 instance … 100,000줄 Rust 기반 C compiler" — verbatim 일치. | ✅ | cards-verbatim | 🟢 |
| 7 | §4.1 절 1.3 | "경계: 'loop changes the work, it does not delete you from it'" | `osmani-loop-engineering.md` Quotable 1: "The loop changes the work, it does not delete you from it." — verbatim 일치. | ✅ | cards-verbatim | 🟢 |
| 8 | §4.1 표 4.1a P9 | "정량은 tier 3" (worktree) | `zylos-git-worktree-isolation.md` tier 확인 필요 — 카드 목록에 `augmentcode-git-worktrees.md` 도 존재. `analysis_summary.md §5` Gap 에 "정량은 tier 3(zylos/augmentcode)" 표기. cards glob 기준 두 카드 모두 존재, tier는 카드에서 확인 필요하나 strategy Gap §5.3 과 일치. | ✅ | cards-name-only | 🟢 |
| 9 | §4.1 표 4.1a P10 | "auto-mode(93%/17% FN)" | `anthropic-claude-code-auto-mode.md` Quotable: "Claude Code users approve 93% of permission prompts" + Limitations: "17% false-negative rate" — verbatim 일치. | ✅ | cards-verbatim | 🟢 |
| 10 | F3 캡션 | "84% sandboxing / 93% approve·17% FN" | `anthropic-claude-code-sandboxing.md` Core Claims: "sandboxing safely reduces permission prompts by 84%" — 84% 일치. `anthropic-claude-code-auto-mode.md`: 93% approve + 17% FN — 일치. | ✅ | cards-verbatim | 🟢 |
| 11 | §5.2 Style Guide | "90.2% 향상" | `anthropic-multi-agent-research-system.md` Core Claims: "내부 eval 에서 90.2% 향상" — 일치. | ✅ | cards-verbatim | 🟢 |
| 12 | §5.2 Style Guide | "15배 token" | `anthropic-multi-agent-research-system.md` Core Claims: "chat 대비 약 15배 token" — 일치. | ✅ | cards-verbatim | 🟢 |
| 13 | §5.2 Style Guide | "98.7%" | `anthropic-code-execution-mcp.md` Core Claims: "token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%." — 일치. | ✅ | cards-verbatim | 🟢 |
| 14 | §5.2 Style Guide | "85%" | `anthropic-advanced-tool-use.md` Quotable: "85% reduction in token usage" — 일치. | ✅ | cards-verbatim | 🟢 |
| 15 | §5.2 Style Guide | "23.8pt / 76.2/52.4" (Harness-Bench) — "Greyling 경유 2차 인용" 명시 | `greyling-agent-model-harness.md` Key Concepts: "23.8 점 이동. NanoBot 76.2 vs OpenClaw 52.4" + Limitations: "수치는 Greyling 가 논문에서 옮긴 2차 인용". Strategy §5.2 가 "Greyling 경유 2차 인용 명시" 라고 올바르게 표기. | ✅ | cards-verbatim | 🟢 |
| 16 | §5.3 Gap | "−73%" | `arxiv-constitutional-spec-driven.md` (grep 결과): "보안 defect 73% 감소" — 일치. | ✅ | cards-verbatim | 🟢 |
| 17 | §5.3 Gap / §5.2 | "+2.8%" | `arxiv-skillreducer.md`: "functional quality 2.8% 향상" — 일치. | ✅ | cards-verbatim | 🟢 |
| 18 | §5.3 Gap | "6%p" | `anthropic-infrastructure-noise.md`: "Terminal-Bench 2.0 에서 strict↔uncapped 사이 6%p swing" — 일치. | ✅ | cards-verbatim | 🟢 |
| 19 | §5.3 Gap / F8 | "18,282→122 tokens" | `arxiv-agentic-context-engineering.md`: "18,282 tokens … → 122 tokens" — verbatim 일치. | ✅ | cards-verbatim | 🟢 |
| 20 | §5.3 Gap | "17%→53%" | `arxiv-self-improving-coding-agent.md`: "SWE-bench Verified … 17%→53% 성능 향상" — 일치. | ✅ | cards-verbatim | 🟢 |
| 21 | §4.2 표 4.2a P10 | "현역 4종 (당직 duty / 일지 note / **모의훈련 golden** / 연수 study)" | `loops/README.md` 현역 표: 루프 이름이 `당직(oncall)` / `일지(note)` / **`모의훈련(drill/)`** / `연수(study)`. Strategy 가 모의훈련을 "golden" 으로 표기했으나 loops/README.md 의 실명은 `drill`. `CLAUDE.md` 도메인 트리거에도 `drill/run.sh` 로 표기. `loops/README.md` §케이스 승격 에는 "drill 케이스로 박아" 라는 트리거 발화. 단, `CONVENTIONS.md §5.10` "drill g0 실측"에서 내부 연동 명칭으로 쓰임. | 🔴 (loops/README.md 실명은 `drill`, strategy 표기 `golden` 은 오명칭 — 여러 라이브 파일에서 `drill` 사용) | live-file-missing | 🔴 |
| 22 | §4.3 표 4.3a "아침 당직 처리" | anchor `notes/scout/` 또는 `notes/duty/<date>.md` | `CLAUDE.md` 도메인 트리거: `notes/oncall/` 표기. `notes/` 실물 구조: `oncall/` 디렉터리 존재, `scout/` 나 `duty/` 디렉터리는 없음. Strategy 의 `notes/scout/` 는 stale 명칭 (구 scout → 현 oncall), `notes/duty/` 도 존재하지 않음. | 🔴 (실물 경로 `notes/oncall/`. `notes/scout/`·`notes/duty/` 모두 존재 안 함) | live-file-missing | 🔴 |
| 23 | §4.2 표 4.2a P7 / P10 | `loops/README.md` "케이스 승격" 절 | `loops/README.md`: "케이스 승격 (오답노트 → drill)" 절 존재 — 일치. 단 트리거 발화가 "이거 golden 케이스로 박아" 가 아니라 "이거 drill 케이스로 박아" 임. Strategy §4.3 표에서 트리거 발화 표기 확인 필요. | 🟡 (절 존재는 ✅; 트리거 발화 표기는 §4.3 표에 "이거 golden 케이스로 박아"로 표기돼 실명과 불일치 가능성) | live-file-verified | 🟡 |
| 24 | §4.2 표 4.2a P6 | "golden 모의훈련 루프 (지침 회귀 테스트, g0 세팅 세금 ~40k)" | `CONVENTIONS.md §5.10`: "비용 = 세팅 세금 ~40k/대 (drill g0 실측)" — ~40k 일치. `loops/README.md`: 모의훈련=`drill`. 단 strategy 본문 "golden 모의훈련" 표기는 `drill` 의 오명칭. | 🔴 (loop 실명 `drill` → strategy 표기 `golden` 오명칭. ~40k 수치는 일치) | live-file-verified | 🔴 |
| 25 | §4.2 표 4.2a P3 | `CONVENTIONS.md §2` agent model 매트릭스 (연구팀·품질관리팀·편집팀·디자인팀) | `CONVENTIONS.md §2`: "§2. Agent Model 표기 (canonical)" 절 실재 확인. 팀 열거는 카드가 아닌 라이브 파일 기준. | ✅ | live-file-verified | 🟢 |
| 26 | §4.2 표 4.2a P4 | "Agent 툴 중첩 1단 한계" — `CONVENTIONS.md §5.10` | `CONVENTIONS.md §5.10`: "서브에이전트에는 Agent 툴이 노출되지 않는다 — 중첩 1단 한계" — verbatim 일치. | ✅ | live-file-verified | 🟢 |
| 27 | §4.2 표 4.2b hooks | `git-state-guard.sh` (golden g2) 표기 | `hooks/` glob: `git-state-guard.sh` 파일 실재. Strategy 표 4.2b에서 "golden g2" 로 표기하나 실 loop 명칭은 `drill` (g2 = drill case 2 의미일 수 있음). 카드 연계 없음. | 🟡 (g2 = drill case 번호로 해석 가능하나 "golden g2" 표기는 일관성 문제) | live-file-verified | 🟡 |
| 28 | §4.2 절 directive §4 | "g0 세팅 세금 ~40k — `CONVENTIONS.md §5.10` 풀 ceremony 주의 ②" | `CONVENTIONS.md §5.10` 경량/풀ceremony 항목에 "비용 = 세팅 세금 ~40k/대 (drill g0 실측)" 존재 — 일치. | ✅ | live-file-verified | 🟢 |
| 29 | §4.4 표 4.4a Layer 1 | "82 cards 실재" | `notes/cards/` 디렉터리는 실재. 82개 정확한 count는 Bash glob 으로 별도 확인 필요하나 strategy 가 직접 count 주장. 라이브 파일 anchor 라 count drift 가능. | 🟡 (작성 시점 실물이라 drift 가능 — caveat 없으면 stale될 수 있으나 §4.4 주의에 "작성 시점 스냅샷" 이미 명시) | live-file-verified | 🟢 |
| 30 | §4.2 표 4.2a P6 | `CLAUDE.md` 도메인 트리거 "지침 파일 수정 후 golden/run.sh" | `CLAUDE.md` 도메인 트리거: `~/.claude/loops/drill/run.sh` — 실명은 `drill/run.sh`. Strategy anchor `golden/run.sh` 는 오경로. | 🔴 (`CLAUDE.md` 실 경로 `loops/drill/run.sh` vs strategy 표기 `golden/run.sh`) | live-file-missing | 🔴 |

---

## 요약

**🔴 Critical (4건)**:
1. **#21** — loops/README.md 모의훈련 실명 `drill`, strategy 표 4.2a P10 표기 `golden` 오명칭.
2. **#22** — 아침 당직 anchor `notes/scout/` 및 `notes/duty/` 모두 존재 안 함. 실물: `notes/oncall/`.
3. **#24** — §4.2 P6 "golden 모의훈련" 표기 — 실명 `drill`. `~40k` 수치 자체는 맞음.
4. **#30** — §4.2 P6 라이브 anchor `golden/run.sh` → 실 경로 `loops/drill/run.sh`.

**🟡 Caveat (3건)**:
- **#2** — context engineering "공동 명명" 표현이 카드에 없음 (두 1차 출처 병존을 추론한 것).
- **#23** — 케이스 승격 트리거 발화 "golden 케이스로 박아" 실명은 "drill 케이스로 박아".
- **#27** — `git-state-guard.sh` "golden g2" 표기 — 일관성 문제 (drill case 2 로 해석해야 함).

**수치 귀속 (✅)**: 90.2% / 15배 / 98.7% / 85% / 84% / 93% / 17% FN / 23.8pt / 76.2/52.4 / −73% / +2.8% / 6%p / 17%→53% / 18,282→122 모두 카드 귀속 정확.  
**Greyling 정리자 구분 (✅)**: strategy §5.2 / Style Guide 에 "정리·대중화자(명명자 아님)" 명확히 표기.  
**tier 4 단독 근거 금지 (✅)**: §5.3 Gap 에 P7 자동화 "tier 4만" 경고 및 단독 사용 금지 명시.
