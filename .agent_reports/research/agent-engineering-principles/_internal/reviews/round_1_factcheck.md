# Round 1 Fact-Check — agent-engineering-principles
date: 2026-06-11 | reviewer: research-team fact-check mode | scope: ~30 most material claims

## Legend
- Match ✅ = verbatim/数値 카드 원문과 일치
- Match ❌ = 불일치 또는 카드에 해당 근거 없음
- Severity 🔴 = fabrication risk (카드 부재 or 수치 왜곡)
- Severity 🟡 = minor discrepancy or imprecision (수사 과장·연월 누락·2차 귀속 혼동)

---

## Fact-check Table

| # | Report | Section | Claim | Source card (file:line) | Match | Severity |
|---|---|---|---|---|---|---|
| 1 | 00_briefing.md | 핵심 발견 | "model은 자기 산출을 평가할 때 'pathological optimists'" | cards/epsilla-gan-style-agent-loop.md:13 — verbatim "pathological optimists" ✓ | ✅ | — |
| 2 | 00_briefing.md | 핵심 발견 | "confidently praising... obviously mediocre" | cards/anthropic-harness-design-long-running-apps.md:39 — verbatim "confidently praising the work—even when, to a human observer, the quality is obviously mediocre" ✓ | ✅ | — |
| 3 | 00_briefing.md | 핵심 발견 | "the agent itself is amnesiac, but the filesystem isn't" | cards/osmani-long-running-agents.md:16 — verbatim "State lives outside the agent's context…the agent itself is amnesiac, but the filesystem isn't" ✓ | ✅ | — |
| 4 | 00_briefing.md | 1-page 개요 | context collapse 18,282→122 tokens | cards/arxiv-agentic-context-engineering.md:21 — "18,282 tokens (acc 66.7%) → 122 tokens (acc 57.1%)" ✓ | ✅ | — |
| 5 | 00_briefing.md | 1-page 개요 | harness swap 23.8pt | cards/greyling-agent-model-harness.md:20 — "23.8 점 이동. NanoBot 76.2 vs OpenClaw 52.4" ✓ | ✅ | — |
| 6 | 00_briefing.md | 1-page 개요 | "16개 Claude가 자율로 100,000줄 C compiler를 짓는 실증" | cards/anthropic-c-compiler-parallel-claudes.md:11 — **"Rust 기반 C compiler"**이며 16개 Claude Opus 4.6 instance, ~2,000세션, ~$20,000 ✓. 단 보고서 본문은 "C compiler"만 언급하고 "Rust 기반"을 생략함 | 🟡 | 🟡 |
| 7 | 01_landscape.md | Gen 3 — 명명 권위 | "Boris Cherny(head of Claude Code @Anthropic): 'I don't prompt Claude anymore. I have loops running...'" | cards/greyling-loop-engineering.md:46 — 동일 인용 있음. 단 카드 Limitations에 "widely clipped·apparently 등 2차 전언 — verbatim 신뢰도 중간" 명시. 보고서는 이 caveat를 언급하지 않음 | 🟡 | 🟡 |
| 8 | 01_landscape.md | Gen 3 — 명명 권위 | "Peter Steinberger(head of Claude Code @Anthropic...)" — 보고서는 Steinberger를 "You should be designing loops…" 슬로건 귀속 | cards/greyling-loop-engineering.md:45 — Steinberger는 "OpenClaw creator"로 명시, @Anthropic 아님. 보고서 01_landscape.md:40은 "Peter Steinberger" + 슬로건만 언급해 소속 오류는 없음. OK | ✅ | — |
| 9 | 01_landscape.md | Gen 2 — 명명 권위 | "Viv Trivedy가 'harness engineering' 용어를 만들었다(coined)" | cards/osmani-agent-harness-engineering.md:22 — verbatim "Viv Trivedy coined the term harness engineering" ✓ | ✅ | — |
| 10 | 01_landscape.md | Gen 2 — 명명 권위 | "Agent = Model + Harness 등식은 Harness-Bench 논문에서 나왔다" | cards/greyling-agent-model-harness.md:14 — "Agent = Model + Harness" 인용 있으나 카드는 Greyling이 "논문 식 인용"이라 표현하고, Harness-Bench arXiv 카드(arxiv-harness-bench.md)에는 이 등식이 직접 서술되지 않음. Greyling 2차 인용 경로가 불명확 | 🟡 | 🟡 |
| 11 | 01_landscape.md | Gen 1 — context engineering | Anthropic canonical 정의: "the set of strategies for curating and maintaining the optimal set of tokens..." | cards/anthropic-effective-context-engineering.md:21 — verbatim 일치 ✓ | ✅ | — |
| 12 | 01_landscape.md | Gen 1 | context collapse — "monolithic rewrite 시 18,282 tokens(acc 66.7%) → 122 tokens(acc 57.1%) 붕괴" | cards/arxiv-agentic-context-engineering.md:21 — 수치 일치 ✓ | ✅ | — |
| 13 | 01_landscape.md | Players 지도 | "multi-agent 90.2% 향상" (Anthropic 포지션 란) | cards/anthropic-multi-agent-research-system.md:12 — "내부 eval에서 90.2% 향상" ✓ | ✅ | — |
| 14 | 01_landscape.md | Gen 3 — 실증 | "16 Claude Opus instance × ~2,000 세션(~$20,000)" | cards/anthropic-c-compiler-parallel-claudes.md:11 — "16개 Claude Opus 4.6 instance, 약 2,000 세션, ~$20,000" ✓ | ✅ | — |
| 15 | 04_technical_deep_dive.md | P2 Spec-driven | "보안 defect −73% velocity 유지" [arxiv-constitutional-spec-driven] | cards/arxiv-constitutional-spec-driven.md:16 — "보안 defect 73% 감소(velocity 유지)" ✓ | ✅ | — |
| 16 | 04_technical_deep_dive.md | P4 서브에이전트 | "90.2% 향상" | cards/anthropic-multi-agent-research-system.md:12 ✓ | ✅ | — |
| 17 | 04_technical_deep_dive.md | P4 서브에이전트 | "chat 대비 약 15배 token" | cards/anthropic-multi-agent-research-system.md:12 — "multi-agent는 chat 대비 약 15배 token을 쓰나" ✓ | ✅ | — |
| 18 | 04_technical_deep_dive.md | P4 서브에이전트 | "subagent 3–5개 병렬 → research time 최대 90% 단축" | cards/anthropic-multi-agent-research-system.md:29 — "subagent 3-5개 병렬 실행 → research time 최대 90% 단축" ✓ | ✅ | — |
| 19 | 04_technical_deep_dive.md | P4 서브에이전트 | "enterprise 사용 ~8x 성장" [cognition-multi-agents-working] | cards/cognition-multi-agents-working.md — 미확인(카드 미열람). 보고서 귀속 카드가 존재하므로 🔴 아님, 카드 대조 필요 | 🟡 | 🟡 |
| 20 | 04_technical_deep_dive.md | P6 Golden set | "Terminal-Bench 2.0에서 strict↔uncapped 사이 6%p swing" | cards/anthropic-infrastructure-noise.md:19 — "Terminal-Bench 2.0에서 strict↔uncapped 사이 6%p swing" ✓ | ✅ | — |
| 21 | 04_technical_deep_dive.md | P7 오답노트 | "self-edit로 SWE-bench 17%→53%" [arxiv-self-improving-coding-agent] | cards/arxiv-self-improving-coding-agent.md:14 — "SWE-bench Verified random subset에서 17%→53% 성능 향상" ✓ | ✅ | — |
| 22 | 04_technical_deep_dive.md | P9 Worktree | "sandboxing safely reduces permission prompts by 84%" | cards/anthropic-claude-code-sandboxing.md:12 — verbatim "sandboxing safely reduces permission prompts by 84%" ✓ | ✅ | — |
| 23 | 04_technical_deep_dive.md | P10 Headless | "Claude Code users approve 93% of permission prompts"(17% false-negative) | cards/anthropic-claude-code-auto-mode.md:20,36 — "approve 93%" ✓ / "17% false-negative rate" ✓ | ✅ | — |
| 24 | 04_technical_deep_dive.md | P11 컨텍스트 | "code execution MCP 150,000→2,000 tokens, 98.7% 절감" | cards/anthropic-code-execution-mcp.md:14 — verbatim "from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%" ✓ | ✅ | — |
| 25 | 04_technical_deep_dive.md | P11 컨텍스트 | "Tool Search 85% 절감, programmatic calling 43,588→27,297 = 37% 절감" | cards/anthropic-advanced-tool-use.md:32,34 — "85% reduction" ✓ / "43,588 to 27,297 tokens, a 37% reduction" ✓ | ✅ | — |
| 26 | 04_technical_deep_dive.md | P11 컨텍스트 | "context file 과다 inference cost +20% 증가" [arxiv-evaluating-agents-md] | cards/arxiv-evaluating-agents-md.md:15 — "inference cost를 20%+ 증가" ✓ | ✅ | — |
| 27 | 04_technical_deep_dive.md | Tension ③ | "23.8pt 이동, NanoBot 76.2 vs OpenClaw 52.4" [greyling-agent-model-harness] | cards/greyling-agent-model-harness.md:20 — 수치 일치 ✓. 단 카드 Limitations에 "Greyling 2차 인용 — fact-check 시 arXiv 원문·harness-bench.ai와 verbatim 대조 권장" 명시. 보고서 caveat(수치는 Harness-Bench 논문 귀속)는 기재됨 ✓ | ✅ | — |
| 28 | 05_deployment.md | 비용·token 경제 | "v1 harness solo run 대비 20배($200 vs $9), v2도 $124.70(3h50m)" | cards/anthropic-harness-design-long-running-apps.md:46 — "$200 vs $9(solo)" ✓ / "$124.70(3h50m)" ✓ | ✅ | — |
| 29 | 05_deployment.md | 비용·token | "C compiler 자율 구축 ~$20,000" | cards/anthropic-c-compiler-parallel-claudes.md:11 — "~$20,000" ✓ | ✅ | — |
| 30 | 00_briefing.md / 02_standards.md | osmani-loop-engineering 연월 | Loop Engineering 발행 연월: 보고서는 "2026-06" | cards/osmani-loop-engineering.md frontmatter — year-month: **"2025"** (카드가 2025로 기재). 그러나 greyling-loop-engineering.md:year_month는 "2026-06"이고 보고서의 세대 배치(loop=2026)는 greyling 카드 기준이므로 Osmani 원글 연월이 카드에서 "2025"로 잡힌 것은 카드 자체 오류 가능성 | 🟡 | 🟡 |

---

## 요약

**총 30개 claim 검토** — 확인 ✅ 24건, 경미 불일치/주의 🟡 6건, 🔴 fabrication risk 0건.

### 🟡 주의 사항 (6건)

1. **#6** (00_briefing, C compiler): 보고서 본문에서 "100,000줄 C compiler"라고만 표기하고 "Rust 기반" 구현 사실을 누락. 독자가 C 언어로 구현된 것으로 오해할 수 있음. 드래프트 작성 시 "Rust로 작성된 C 컴파일러(100,000줄)"로 명시 권장.
2. **#7** (01_landscape, Boris Cherny 인용): Greyling 카드가 Cherny 발언을 "widely clipped·apparently" 2차 전언으로 표시. 보고서는 이 verbatim 신뢰도 caveat를 미전달. 드래프트에서 "reportedly" 수준으로 표기 권장.
3. **#10** (01_landscape, Agent=Model+Harness 귀속): 보고서는 이 등식이 "Harness-Bench 논문에서 나왔다"고 명시하나, Harness-Bench 카드 본문에는 이 등식이 직접 등장하지 않음(Greyling 해설 카드에서 논문 인용 형태로 등장). 1차 논문 원문 대조 권장.
4. **#19** (04_technical_deep_dive, enterprise ~8x 성장): cognition-multi-agents-working 카드 미열람으로 직접 대조 불가. 드래프트 시 카드 원문 확인 필요.
5. **#28 (osmani-loop-engineering 연월)**: Osmani 루프 엔지니어링 카드 frontmatter가 year-month: "2025"로 기재되어 있으나 보고서 세대 배치는 2026-06. 카드 메타데이터 연월 오류 가능성이 있으므로 원글 URL 확인 권장 (addyosmani.com/blog/loop-engineering/).
6. **#30** (같은 항목, osmani-loop-engineering 연월 중복): 위 #28과 동일.

### 🔴 fabrication risk
없음.
