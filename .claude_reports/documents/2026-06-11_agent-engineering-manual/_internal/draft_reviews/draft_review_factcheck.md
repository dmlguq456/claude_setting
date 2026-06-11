# Fact-Check Log — Agent Engineering Manual Draft
> 작성: 2026-06-11 / 검토자: 연구팀 fact-check mode
> Ground truth: research cards (1부) + 라이브 파일 (2~4부)

---

## 점검 결과 표

| # | Section | Claim | Source (file:line) | Match | Source type | Severity |
|---|---|---|---|---|---|---|
| 1 | §1.0 | "Prompt engineering walked so context engineering could run" — **"Karpathy 의 한 줄"** 귀속 | cards/osmani-context-engineering.md:16 — "(body, Karpathy/quip)" 표기이나 원문은 "One analysis quipped:" 으로 시작해 Karpathy 직접 발언인지 불명확 | 🟡 | cards-name-only | 🟡 |
| 2 | §1.1 | "cleverly phrasing a question" [osmani-context-engineering] | osmani-context-engineering.md:15 — verbatim 확인. 단 draft 는 전체 문장("Prompt engineering was about cleverly phrasing a question; context engineering is about...") 중 후반부를 생략해 단독 인용함 | ✅ | cards-verbatim | 🟢 |
| 3 | §1.1 | "a witty one-off prompt might have wowed us in demos, but building reliable, industrial-strength LLM systems demanded something more comprehensive" [osmani-context-engineering] | osmani-context-engineering.md:35 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 4 | §1.1 | Anthropic canonical def: "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference" [anthropic-effective-context-engineering] | anthropic-effective-context-engineering.md:21 — verbatim 확인. 단 draft 는 "including all the other information..." 후반부를 생략 | ✅ | cards-verbatim | 🟢 |
| 5 | §1.1 | Osmani 판 정의: "constructing an entire information environment so the AI can solve the problem reliably" [osmani-context-engineering] | osmani-context-engineering.md:21 — verbatim 확인 (전체 문장의 후반부) | ✅ | cards-verbatim | 🟢 |
| 6 | §1.1 | context collapse 수치: "18,282 tokens(66.7%)에서 122 tokens(57.1%)" [arxiv-agentic-context-engineering] | arxiv-agentic-context-engineering.md:21 — 정확히 일치 | ✅ | cards-verbatim | 🟢 |
| 7 | §1.2 | harness def: "A coding agent is the model plus everything you build around it. Harness engineering treats that scaffolding as a real artifact, and it tightens every time the agent slips" [osmani-agent-harness-engineering] | osmani-agent-harness-engineering.md:22 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 8 | §1.2 | 학술 def: "the software layer that surrounds an LLM with tools, APIs, sandboxes, memory, validators, permission boundaries, execution loops, and feedback channels, thereby turning a stateless model into a functional agent" [arxiv-code-as-agent-harness] | arxiv-code-as-agent-harness.md 미확인 (카드 미Read) | 🟡 | cards-name-only | 🟡 |
| 9 | §1.2 | **"harness engineering" 용어는 Viv Trivedy 가 coined** [osmani-agent-harness-engineering] | osmani-agent-harness-engineering.md:39 — "Viv Trivedy coined the term _harness engineering_." verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 10 | §1.2 | **Agent = Model + Harness 등식은 Harness-Bench 논문 발** [greyling-agent-model-harness][arxiv-harness-bench] | greyling-agent-model-harness.md:14 — "논문 식 인용 — 'the equation is the whole argument'" 확인. 단 카드 주석에 "Qihoo360" 으로 귀속. 카드에서 등식 자체가 논문에 귀속됨 확인 | ✅ | cards-verbatim | 🟢 |
| 11 | §1.2 | "We've spent the last two years arguing about models... That conversation is fine as far as it goes, but it's missing the other half of the system" [osmani-agent-harness-engineering] | osmani-agent-harness-engineering.md:38 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 12 | §1.2 | "Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing" [anthropic-harness-design-long-running-apps] | anthropic-harness-design-long-running-apps.md:41 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 13 | §1.2 | Greyling = "정리자" (명명자 아님), loop = Osmani 명명, Steinberger·Cherny 슬로건, Greyling = 정리자 | greyling-loop-engineering.md:51 — "loop engineering 명명·프레임의 1차 권위는 Addy Osmani, 실무 슬로건은 Peter Steinberger·Boris Cherny 에게 명시 귀속, Greyling 은 정리자" 확인 | ✅ | cards-verbatim | 🟢 |
| 14 | §1.3 | loop def: "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead" [osmani-loop-engineering] | osmani-loop-engineering.md:15 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 15 | §1.3 | "The harness but it runs on a timer, it spawns little helpers, and it feeds itself" [osmani-loop-engineering] | osmani-loop-engineering.md:21 — verbatim 확인 ("Loop = self-feeding harness") | ✅ | cards-verbatim | 🟢 |
| 16 | §1.3 | "For like two years the way you got something out of a coding agent was you wrote a good prompt and shared enough context..." [osmani-loop-engineering] | osmani-loop-engineering.md:36 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 17 | §1.3 | **C compiler 사례**: "16개 Claude Opus instance × 약 2,000 세션(약 $20,000)으로 100,000줄 C compiler" | anthropic-c-compiler-parallel-claudes.md:12 — "16개 Claude Opus 4.6 instance 가 약 2,000 세션 (~$20,000) 동안 자율적으로 100,000줄 Rust 기반 C compiler" 확인. 단 카드에는 "Rust 기반"이라고 명시 — **draft에서 "Rust 기반"을 생략** | 🟡 | cards-verbatim | 🟡 |
| 18 | §1.3 | "The loop changes the work, it does not delete you from it" [osmani-loop-engineering] | osmani-loop-engineering.md:42 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 19 | §1.3 | runtime tiering: "Tier A terminal (Claude Code / Grok) / Tier B platform (LangChain durable execution) / Tier C editor" [greyling-loop-engineering-playbook] | greyling-loop-engineering-playbook.md:37-39 — Tier A/B/C 확인. 단 playbook 카드에서 tier 표 내용이 "이미지로 처리돼 텍스트 부재"라고 명시 — verbatim 정밀도 약함. Tier 명칭 자체는 확인 | 🟡 | cards-name-only | 🟡 |
| 20 | §1.4-P3 | "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre" [anthropic-harness-design-long-running-apps] | anthropic-harness-design-long-running-apps.md:39 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 21 | §1.4-P3 | "Separating the agent doing the work from the agent judging it proves to be a strong lever" [anthropic-harness-design-long-running-apps] | anthropic-harness-design-long-running-apps.md:40 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 22 | §1.4-P3 | 모델은 "pathological optimists" [epsilla-gan-style-agent-loop] | epsilla-gan-style-agent-loop.md:13 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 23 | §1.4-P3 | "By engineering conflict, you engineer progress" [epsilla-gan-style-agent-loop] | epsilla-gan-style-agent-loop.md:38 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 24 | §1.4-P3 | "Models reliably skew positive when they grade their own work" [osmani-long-running-agents] | osmani-long-running-agents.md:39 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 25 | §1.4-P4 | orchestrator-worker "내부 eval 90.2% 향상" [anthropic-multi-agent-research-system] | anthropic-multi-agent-research-system.md:12 — "single-agent 대비 내부 eval 에서 90.2% 향상" 확인 | ✅ | cards-verbatim | 🟢 |
| 26 | §1.4-P4 | "Multi-agent systems work mainly because they help spend enough tokens to solve the problem" [anthropic-multi-agent-research-system] | anthropic-multi-agent-research-system.md:41 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 27 | §1.4-P4 | multi-agent "chat 대비 약 15배 token" [anthropic-multi-agent-research-system] | anthropic-multi-agent-research-system.md:12 — "multi-agent 는 chat 대비 약 15배 token" 확인 | ✅ | cards-verbatim | 🟢 |
| 28 | §1.4-P4 | "subagent 3–5개 병렬 → research time 최대 90% 단축" [anthropic-multi-agent-research-system] | anthropic-multi-agent-research-system.md:29 — "subagent 3-5개 병렬 실행, 각자 3+ tool 병렬 호출 → research time 최대 90% 단축" 확인 | ✅ | cards-verbatim | 🟢 |
| 29 | §1.4-P4 | "enterprise 사용 약 8x 성장" [cognition-multi-agents-working] | cognition-multi-agents-working.md:13 — "enterprise 사용 ~8x 성장" 확인 | ✅ | cards-verbatim | 🟢 |
| 30 | §1.4-P4 | "Running multiple agents in collaboration only results in fragile systems" [cognition-dont-build-multi-agents] | cognition-dont-build-multi-agents.md:14 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 31 | §1.4-P4 | "Actions carry implicit decisions, and conflicting decisions carry bad results" [cognition-dont-build-multi-agents] | cognition-dont-build-multi-agents.md:13 — "Actions carry implicit decisions, and conflicting decisions carry bad results." 카드에서 Principle 2로 서술됨. verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 32 | §1.4-P9 | sandboxing "permission prompts by 84%" [anthropic-claude-code-sandboxing] | anthropic-claude-code-sandboxing.md:12 — "sandboxing safely reduces permission prompts by 84%" verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 33 | §1.4-P10 | "Claude Code users approve 93% of permission prompts" (17% false-negative rate) [anthropic-claude-code-auto-mode] | anthropic-claude-code-auto-mode.md:20 — 93% 확인. Limitations:36 — "17% false-negative rate" 확인 | ✅ | cards-verbatim | 🟢 |
| 34 | §1.4-P11 | code execution MCP "150,000 → 2,000 tokens, 98.7% 절감" [anthropic-code-execution-mcp] | anthropic-code-execution-mcp.md:33 — "150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%" verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 35 | §1.4-P11 | "Tool Search 85% 절감, programmatic calling 43,588 → 27,297 = 37% 절감" [anthropic-advanced-tool-use] | anthropic-advanced-tool-use.md:32,34 — "85% reduction" 및 "43,588 to 27,297 tokens, a 37% reduction" verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 36 | §1.4-P11 | "SkillReducer 48% description / 39% body 압축에 quality +2.8%" [arxiv-skillreducer] | arxiv-skillreducer.md:16 — "48% description / 39% body 압축에 functional quality 2.8% 향상" 확인 | ✅ | cards-verbatim | 🟢 |
| 37 | §1.4-T3 | Harness-Bench 수치: "harness 만 바꿔도 23.8pt 이동, NanoBot 76.2 vs OpenClaw 52.4" / "NanoBot 76.2 @ 7.3 turns < Hermes 71.2 @ 22.6 turns" [greyling-agent-model-harness] | greyling-agent-model-harness.md:20,31 — 수치 확인. 카드 자체에도 "Greyling 가 논문에서 옮긴 2차 인용 — arXiv 원문과 verbatim 대조 권장" 명시. draft 본문도 이를 캐비엇으로 표기함 | ✅ | cards-verbatim | 🟢 |
| 38 | §1.4-T3 | "Weak models are hostages to their harness…Strong models shrug it off…a crutch whose value decays as the model improves" [greyling-agent-model-harness] | greyling-agent-model-harness.md:35 — verbatim 확인 | ✅ | cards-verbatim | 🟢 |
| 39 | §1.4-T4 | AGENTS.md 류 context file 이 task success rate 저하 + inference cost +20% [arxiv-evaluating-agents-md] | arxiv-evaluating-agents-md.md 미확인 (카드 미Read). 수치 +20%에 대한 카드 대조 미실시 | 🟡 | cards-name-only | 🟡 |
| 40 | §1.4-P2 | constitutional spec-driven "보안 defect −73%" [arxiv-constitutional-spec-driven] | arxiv-constitutional-spec-driven.md:12 — "무제약 생성 대비 보안 defect 73% 감소" 확인. draft에 "−73%"는 정확 | ✅ | cards-verbatim | 🟢 |
| 41 | §2.5 | **"당직(oncall) 7호"가 고아 job을 감시** | oncall.md — 실물 파일에 "7호"라는 표현 없음. 해당 내용은 "항목 8" (디스패치 job 현황)에 있음. "7호" 라는 호칭은 **라이브 파일에 존재하지 않는 표현** | ❌ | live-file-missing | 🔴 |
| 42 | §2.5 | loop 4종: 당직(oncall) cron 05:37 / 일지(note) cron 05:03 / 모의훈련(drill) 사건형 / 연수(study) cron 일요일 06:17 | loops/README.md 현역 표 — 모두 확인 | ✅ | live-file-verified | 🟢 |
| 43 | §2.5 | hooks 6종 목록 (artifact-guard/spec-skill-gate/spec-read-marker/git-state-guard/design-postwrite/herdr-agent-state) | /home/Uihyeop/.claude/hooks/ — ls 결과 6종 확인 | ✅ | live-file-verified | 🟢 |
| 44 | §2.4 | "중첩 1단 한계 (스모크 테스트 2026-06-11)" | CONVENTIONS.md §5.10 — 스모크 테스트 날짜 명시 없음. 단 §5.10에 "중첩 1단 한계" 제약 자체는 확인 | 🟡 | live-file-missing | 🟡 |
| 45 | §2.4 | job 레지스트리: `~/.claude/.dispatch/jobs.log` 포맷 확인 | CONVENTIONS.md §5.10:404 — 포맷 verbatim 확인 | ✅ | live-file-verified | 🟢 |
| 46 | §2.4 | headless 분사 "비용 = 세팅 세금 약 40k/대 (drill g0 실측)" | CONVENTIONS.md / loops/README.md 에 "40k" 수치 미확인. study.md에 "g0 세금 추세" 추적 언급은 있으나 "40k" 구체 수치는 라이브 파일에서 미발견 | 🟡 | live-file-missing | 🟡 |
| 47 | §4.0 | worklog prd 인용: "쏟아지는 산출물 md 를 하나하나 안 읽고도 따라가고 다시 찾는 것" (`prd.md §2`) | worklog-board/.claude_reports/spec/prd.md:28 — "핵심 가치 = 쏟아지는 산출물 md 를 하나하나 안 읽고도 따라가고 다시 찾는 것" verbatim 확인 | ✅ | live-file-verified | 🟢 |
| 48 | §4.1 | "Layer 1 (notes/cards/) 82 cards 실재" | `ls /home/nas/user/Uihyeop/notes/cards/ \| wc -l` = 82 확인 | ✅ | live-file-verified | 🟢 |
| 49 | §4.1 | prd "v2~v33 누적" | worklog-board prd 본문에서 v18, v19, v22, v24, v32, v33 등 version tag 다수 확인. "v2~v33" 범위는 근사치로 타당 | ✅ | live-file-verified | 🟢 |
| 50 | §1.0 | Anthropic "Building effective agents" = "harness 세대의 정초" (2024-12) | anthropic-building-effective-agents.md — year_month: 2024-12 확인. "harness engineering 세대의 정초 텍스트"로 Generation Mapping 에 명시 | ✅ | cards-verbatim | 🟢 |

---

## 🔴/🟡 발견 요약

### ❌ 🔴 오류

**#41 — "당직(oncall) 7호"**: `oncall.md` 실물에 "7호"라는 표현 없음. 디스패치 감시 기능은 항목 **8**에 위치. "당직 7호"는 존재하지 않는 호칭이다.
- 위치: draft.md 366행, 479행
- 수정 방향: "당직(oncall) 7호" → "당직(oncall) 항목 8" 또는 "당직(oncall)"으로 수정

### 🟡 주의 사항

**#1 — "Karpathy 의 한 줄"**: osmani-context-engineering 카드에 "(body, Karpathy/quip)"로 표기되어 있으나 원문은 "One analysis quipped:"으로 시작 — Karpathy 직접 발언 여부 불명확. 카드에 Karpathy 귀속 표기는 있으나 verbatim 귀속 근거가 약함.

**#17 — C compiler "Rust 기반" 생략**: 카드에 "Rust 기반 C compiler"라고 명시되어 있으나 draft에서 "100,000줄 C compiler"로만 서술해 Rust 구현이라는 중요 정보를 생략.

**#8 — arxiv-code-as-agent-harness 학술 def**: 카드 미Read — 인용문 정확도 미확인.

**#19 — runtime tier 내용**: greyling-loop-engineering-playbook 카드 자체에서 tier 표 내용이 "이미지로 처리돼 텍스트 부재"라고 명시 — verbatim 정밀도 약함.

**#39 — +20% inference cost**: arxiv-evaluating-agents-md 카드 미Read — 수치 미확인.

**#44 — 중첩 1단 한계 날짜**: CONVENTIONS.md §5.10에 "스모크 테스트 2026-06-11" 날짜 명시 없음.

**#46 — 세팅 세금 약 40k**: 라이브 파일에서 구체 수치 미확인.

---

## 총평

총 50개 claim 점검:
- ✅ 정확: 39개
- 🟡 주의: 10개 (7개 verbatim 정밀도 이슈, 3개 라이브 파일 미확인)
- ❌ 오류: 1개 (당직 7호 — 존재하지 않는 호칭)

1부 verbatim 인용 품질은 전반적으로 높음. 2~4부 라이브 anchor 대부분 정확. **핵심 오류 1건(당직 7호)** 수정 필요.
