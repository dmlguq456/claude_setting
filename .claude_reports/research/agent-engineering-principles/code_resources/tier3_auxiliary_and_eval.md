# Tier 3 — 보조·실험 코드 + Eval 도구

> self-improvement 연구 코드, eval/regression 도구, Inside-the-Scaffold 분석 대상 목록. star/last-update 는 2026-06-11 확인값, 대략치.

---

## 자기개선(self-improvement) 연구 코드

### ace-agent/ace (Agentic Context Engineering)

- **url**: https://github.com/ace-agent/ace
- **stars**: ~1.1k
- **language**: Python (100%)
- **last-update**: 2025-11 (paper+repo 공개)
- **구현 패턴 매핑**: ACE 의 Generator/Reflector/Curator 3-role · delta update + grow-and-refine (context collapse 방지) · "evolving playbook". = 매뉴얼 "오답노트 → 케이스 승격" + context 누적·playbook 화의 알고리즘 정식화 (offline+online adaptation).
- **매뉴얼 인용 가치**: Context Engineering 세대의 학술 정식화 (arXiv 2510.04618) 의 공식 구현 — maker/verifier 역할 분업 (Generator/Reflector/Curator) 의 코드 레퍼런스.
- **카드**: `cards/arxiv-agentic-context-engineering.md`
- **Quick verify**: `git clone https://github.com/ace-agent/ace.git && cd ace && uv sync` (uv 설치 후 API key 설정 필요)

### MaximeRobeyns/self_improving_coding_agent (SICA)

- **url**: https://github.com/MaximeRobeyns/self_improving_coding_agent
- **stars**: ~343
- **language**: Python (~96%)
- **last-update**: 활발 (master)
- **구현 패턴 매핑**: agent 가 **자기 codebase 를 편집**해 cost/speed/benchmark 개선 (meta-agent=target-agent 통합) · benchmark 신호로 self-edit 루프 (maker/verifier) · Docker 격리 실행 (shell 명령 안전). SWE-bench Verified 17%→53%.
- **매뉴얼 인용 가치**: 매뉴얼의 메타-스킬 진화 (post-it·golden loop 로 실패→지침 승격) 와 self-improving 루프 철학의 reference 구현 (arXiv 2504.15228). gradient 없는 reflection-driven 개선.
- **카드**: `cards/arxiv-self-improving-coding-agent.md`
- **Quick verify**: `git clone https://github.com/MaximeRobeyns/self_improving_coding_agent && cd self_improving_coding_agent && make image` (Docker 필수 — agent 가 shell 실행)

---

## Eval / regression 도구

### promptfoo/promptfoo

- **url**: https://github.com/promptfoo/promptfoo
- **stars**: ~22k
- **language**: TypeScript (~97%)
- **last-update**: 2026-06-05
- **구현 패턴 매핑**: CLI/library 로 prompt·model eval + red-teaming · YAML 정의 test suite (golden set) + assertion · provider 간 비교. = 매뉴얼 golden set/eval 회귀 + 오답노트→케이스 승격의 self-hosted CLI 구현.
- **매뉴얼 인용 가치**: eval-driven development 의 가장 접근성 높은 OSS CLI — golden set(YAML) + assertion 으로 "변경 전 회귀 검증" 을 self-host. 매뉴얼 golden loop 의 도구 예시.
- **카드**: `cards/braintrust-eval-driven-development.md` / `cards/redhat-eval-driven-development.md` (개념 출처)
- **Quick verify**: `npm install -g promptfoo && promptfoo --version`

### Braintrust (braintrustdata/*)

- **url**: https://github.com/braintrustdata (org; SDK 가 언어별 분리 — `braintrust-sdk-javascript`, `braintrust-sdk-python`, `autoevals` 등)
- **stars**: SDK 개별 repo 는 소규모 (수십~수백). **핵심 가치는 vendor SaaS 플랫폼** (logging/tracing/evals/playground) — 자체 repo star 로 판단 부적합.
- **language**: TypeScript / Python (SDK), autoevals 는 평가 scorer 모음
- **last-update**: 2026-06-05 (braintrust@3.17.0)
- **구현 패턴 매핑**: golden set (frozen core) + expanding dataset (growing set) + failure-driven evolution (production 실패 → golden 승격). = 매뉴얼의 "frozen core vs growing set" 이분법의 1차 개념 출처 (eval-driven-development 카드).
- **매뉴얼 인용 가치**: "eval = working spec / failure→golden 승격" 개념의 명명 출처. 단 self-host 가 아닌 SaaS — 개념 인용 위주, 구현은 promptfoo 권장.
- **카드**: `cards/braintrust-eval-driven-development.md`
- **Quick verify**: `npm install braintrust autoevals` (또는 `pip install braintrust`) — 단 platform API key 필요

### langchain-ai/langsmith-sdk

- **url**: https://github.com/langchain-ai/langsmith-sdk
- **stars**: ~0.9k (client SDK; LangSmith 플랫폼은 SaaS)
- **language**: Python (~60%) + TS
- **last-update**: 2026-06-10 (v0.8.14)
- **구현 패턴 매핑**: debug/eval/monitor LLM·agent · dataset 기반 evaluation + tracing. eval-driven 회귀·관찰성. LangGraph 와 통합.
- **매뉴얼 인용 가치**: trace 기반 eval + dataset regression 의 reference SDK (LangChain 생태계). 매뉴얼 eval 회귀의 관찰성 측면 도구.
- **Quick verify**: `pip install -U langsmith && python -c "import langsmith; print(langsmith.__version__)"` (LangSmith API key 필요)

---

## Inside-the-Scaffold 13개 분석 대상 (arXiv 2604.03515)

> source-code taxonomy 논문의 분석 대상. harness 차원(control loop·tool interface·resource management)의 비교 레퍼런스. 13개 중 7개가 각 15k+ stars (채택 신호).

| Agent | 비고 (harness 차원) |
|---|---|
| OpenCode | control loop / tool set 다양 |
| Gemini CLI | CLI 형 control loop |
| Codex CLI | OpenAI CLI agent |
| **OpenHands** | event-sourcing state, containerized 격리 (Tier 1 상세) |
| Cline | IDE 통합 control loop |
| **Aider** | repo map retrieval, git-as-state (Tier 1 상세) |
| **SWE-agent** | ACI, generate-test-repair (Tier 1 상세) |
| mini-swe-agent | 경량 SWE-agent |
| AutoCodeRover | AST-aware retrieval |
| Agentless | fixed pipeline (loop 없는 phased) |
| Prometheus | knowledge graph retrieval |
| Moatless Tools | tree search / phased |
| DARS-Agent | depth-first tree search |

- **매뉴얼 인용 가치**: "scaffold/harness 가 행동을 결정한다" 를 13개 OSS 소스코드로 측정한 1차 학술 근거 (file path+line number grounding). 개별 repo 깊이 인용보다 **taxonomy 표 자체**를 harness 차원 비교에 인용.
- **카드**: `cards/arxiv-inside-the-scaffold.md` (개별 repo URL 은 논문 내 pinned commit 참조 — 본 survey 에서 일괄 URL 검증은 미수행, 인용 시 논문 경유 권장)
