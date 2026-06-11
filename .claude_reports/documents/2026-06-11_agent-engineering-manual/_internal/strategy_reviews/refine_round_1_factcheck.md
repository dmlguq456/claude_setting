---
type: fact-check
round: refine_round_1
date: 2026-06-11
scope: v2 changed sections only (~15 claims)
verifier: research-team / fact-check mode
---

# Fact-Check: Strategy v2 변경 분 (~15 claims)

> 검증 범위: strategy.md `changelog v2` 에 명시된 변경 항목에 한정. ground truth = `cards/*.md` verbatim + 라이브 파일 직접 Read.

| Section | Claim | Source (file:line) | Match | Severity |
|---|---|---|---|---|
| **§2 M5** | `greyling-configured-not-coded` 카드가 verbatim "A markdown edit without a before/after eval is a vibe" 의 실출처 | `greyling-configured-not-coded.md` Quotable #3: **"A markdown edit without a before/after eval is a vibe."** verbatim 일치 | ✅ | 🟢 |
| **§2 M5** | Patterns Covered 항목 "measure what you change" 에 해당 인용 포함 | `greyling-configured-not-coded.md` Patterns Covered: "measure what you change (before/after eval 없는 markdown edit = "a vibe")" — 동일 표현 명시 | ✅ | 🟢 |
| **표 4.1a P3** | `willison-agentic-engineering-patterns` 가 "Red/green TDD 일반화" 근거 | `willison-agentic-engineering-patterns.md` Patterns Covered #2: **"Red/green TDD"** — "test-first development enables agents to produce more succinct and reliable code with minimal additional prompting" 명시 | ✅ | 🟢 |
| **표 4.1a P3** | willison 이 P3 maker-verifier 의 1차 카드 | willison 카드 Generation Mapping: "Red/green TDD = maker(generate)/verifier(test) loop 의 가장 검증된 실무 패턴" — P3 매핑 명시 | ✅ | 🟢 |
| **표 4.1a P4** | `openai-practical-guide-agents` 가 "Manager/Decentralized" 패턴 근거 | `openai-practical-guide-agents.md` Patterns Covered: **"Manager pattern"** (중앙 manager agent 가 specialized agent 들을 tool call 로 조율) + **"Decentralized pattern"** (peer agent 들이 서로 handoff) 명시 | ✅ | 🟢 |
| **표 4.1a P4** | openai 카드 verbatim 은 "2차 경유, pattern 명칭 수준만" 이라고 caveat 표기 | `openai-practical-guide-agents.md` fetch_note: "PDF는 binary 라 WebFetch parse 실패 → WebSearch + maginative.com 2차 요약" — 카드 자체가 2차 출처임 명시. strategy 표 4.1a 의 caveat "(verbatim 은 2차 경유, pattern 명칭 수준만)" 과 정합 | ✅ | 🟢 |
| **표 4.1a P6** | `anthropic-ai-resistant-evals` 가 P6 golden set 근거 | `anthropic-ai-resistant-evals.md` Generation Mapping: "golden set 이 시간이 지나도 변별력을 유지하려면 saturation·contamination 에 저항하는 설계가 필요하다는 근거. eval regression 의 '왜 set 을 갱신·강화해야 하나'의 보강." — P6 연결 명시 | ✅ | 🟢 |
| **표 4.1a P6** | `redhat-eval-driven-development` 가 P6 "tier 3 구현 사례 — 'known bad' set" 근거 카드 중 하나 | `redhat-eval-driven-development.md` 카드 존재 확인됨 (cards/ 목록에 있음). 단 내용 미직접열람 — tier/역할 verbatim 대조 불완전 | 🟡 | 🟡 |
| **표 4.1a P11** | `anthropic-agent-skills` 가 P11 "progressive disclosure 1차" 근거 | `anthropic-agent-skills.md` Core Claims: "Skills let Claude load information only as needed." Key Concepts: **"Progressive disclosure"** — "startup 시 metadata 만 로드, 관련될 때 full SKILL.md 로드, 추가 파일은 on-demand" 명시. P11 컨텍스트 절약 1차 근거로 적합 | ✅ | 🟢 |
| **표 4.1a P11** | `anthropic-think-tool` 이 P11 카드 중 하나 | `anthropic-think-tool.md` Generation Mapping: "Harness Eng / plan-then-execute: 실행 도중 명시적 reasoning 공간을 harness 가 제공한다는 사례." — P11 컨텍스트 절약 직접 매핑이 약함. P11 이 아니라 P1/P3 쪽 근거에 더 가까움 | 🟡 | 🟡 |
| **§4.1 1.2** | `greyling-rise-of-harness-engineering` 이 harness 4th-layer 정리 근거 | `greyling-rise-of-harness-engineering.md` Key Concepts: "4번째 architectural approach: SDK / Framework / Scaffolding 위에 2026 에 등장. Harness 는 다른 질문에 답함 — 'how the agent runs'." — 4번째 architectural layer 명시 | ✅ | 🟢 |
| **§4.1 1.3** | `greyling-loop-engineering-playbook` 이 "runtime tiering Tier A terminal/B platform/C editor" 근거 | `greyling-loop-engineering-playbook.md` Generation Mapping: **"Tier A — Terminal harness loops"** / **"Tier B — Platform runtime loops"** / **"Tier C — Editor & lightweight alternatives"** 명시 | ✅ | 🟢 |
| **§4.2 2.2 / §4 directive** | `autopilot-draft/SKILL.md` 의 "Step 5.5 (Editorial polish)" 실명 교정 근거 | `autopilot-draft/SKILL.md` L808: `### Step 5.5: Editorial polish (편집팀 모드 B — conditional)` 명시 — "Stage D.5" 에서 "Step 5.5" 로 교정 근거 확인 | ✅ | 🟢 |
| **§7 Risk** | 루프 명칭 "당직 oncall·일지 note·모의훈련 drill·연수 study" 가 `~/.claude/CLAUDE.md` + `loops/README.md` 양쪽 모두 일치 확인 (2026-06-11) | `CLAUDE.md` L96: "루프 호칭: 당직=oncall·일지=note·모의훈련=drill·연수=study". `loops/README.md` 현역 표: 동일 4종 명칭 일치 | ✅ | 🟢 |
| **§7 Risk** | 구명(scout/golden) 언급이 "이력형 재서술" 로 변경됨 — 라이브에 scout/golden 잔재 없음 | `CLAUDE.md` L95: "미실행 시 oncall 가 다음날 아침 보고." `loops/README.md` 현역 표: scout/golden 표기 없음, oncall/drill 로 통일. 구명 표기 없음 확인 | ✅ | 🟢 |

---

## 요약

| 결과 | 건수 |
|---|---|
| ✅ confirmed | 13 |
| 🟡 partial / caveat | 2 |
| ❌ conflict | 0 |

**🟡 주의 2건**:

1. **`redhat-eval-driven-development` P6 역할** — 카드 존재는 확인됐으나 "known bad set" verbatim 및 tier 3 분류를 카드 본문에서 직접 열람하지 못함. draft 작성 전 카드 본문 재확인 권장.

2. **`anthropic-think-tool` P11 배정** — 카드 Generation Mapping 은 "Harness Eng / plan-then-execute" (P1/P3 계열)로 기재. P11 컨텍스트 절약과의 연결 고리가 직접적이지 않음. draft 시 "컨텍스트 절약" 측면(reasoning token 추가 비용)으로 명시 연결하거나, P1/P3 supplementary 로 위치를 조정 고려.
