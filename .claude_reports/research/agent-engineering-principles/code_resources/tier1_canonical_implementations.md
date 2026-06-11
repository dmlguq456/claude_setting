# Tier 1 — 패턴의 Canonical 구현

> 매뉴얼 인용 기준: "이 패턴이 실제 구현된 곳" 레퍼런스. star/last-update 는 WebFetch/WebSearch 확인값 (2026-06-11 기준), 대략치.

---

## humanlayer/12-factor-agents

- **url**: https://github.com/humanlayer/12-factor-agents
- **stars**: ~23k
- **language**: TypeScript (~80%)
- **last-update**: 활발 (273 commits, 2026 진행 중)
- **구현 패턴 매핑**: state 영속성 (Factor 5/6/12 — unify execution+business state, launch/pause/resume, stateless reducer) · control flow 명시화 (Factor 8) · context ownership (Factor 2/3) · small focused agents (Factor 10). manifesto+예제 코드 형태.
- **매뉴얼 인용 가치**: 매뉴얼이 주장하는 "agent = 상태를 변환하는 결정론적 소프트웨어 (loop-until-goal 아님)" 와 상태 파일 단일 출처 (`pipeline_state.yaml`/`plans/*`/`_RUNLOG.md`) 철학의 1차 manifesto 출처.
- **카드**: `cards/humanlayer-12-factor-agents.md`
- **Quick verify**: `git clone https://github.com/humanlayer/12-factor-agents && ls content/` (원칙별 markdown 챕터 확인)

---

## github/spec-kit

- **url**: https://github.com/github/spec-kit
- **stars**: ~90k–110k (출처별 편차 큼 — 급성장 중. 직접 fetch=111k, 2차 출처=71~90k. "~100k+ 급성장" 으로 인용 권장)
- **language**: Python (~95%)
- **last-update**: 2026-06-09 (v0.10.1)
- **구현 패턴 매핑**: spec-first / plan-then-execute (Specify→Plan→Tasks→Implement 4-phase) · spec = living artifact 영속 · Tasks 단계의 TDD-유사 task 분해 (maker-verifier 인접). 30+ AI coding agent 호환 toolkit.
- **매뉴얼 인용 가치**: 매뉴얼 spec-first 파이프 (research/analyze → spec → code) 와 단계가 거의 동형 — "intent is the source of truth" 의 제도화 1차 toolkit. 하드 순서 게이트 (spec 없이 code 금지) 의 외부 근거.
- **카드**: `cards/github-spec-kit.md`
- **Quick verify**: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git && specify --help`

---

## anthropics/claude-code

- **url**: https://github.com/anthropics/claude-code
- **stars**: ~132k
- **language**: Python (~80%) + Shell + TypeScript
- **last-update**: 활발 (661 commits)
- **구현 패턴 매핑**: harness loop (terminal agentic coding) · CLAUDE.md 계층 부트스트랩 · skill/plugin progressive disclosure · git workflow 자동화. 본 family 의 실행 기반 그 자체.
- **매뉴얼 인용 가치**: 매뉴얼이 기술하는 harness·CLAUDE.md·skill 시스템의 reference 구현 (issue tracker·docs 공개). best-practices 카드와 짝.
- **카드**: `cards/anthropic-claude-code-best-practices.md`
- **Quick verify**: `curl -fsSL https://claude.ai/install.sh | bash && claude --version` (또는 Homebrew/npm)

---

## anthropics/claude-agent-sdk-python

- **url**: https://github.com/anthropics/claude-agent-sdk-python
- **stars**: ~7.3k
- **language**: Python (~99%)
- **last-update**: 2026-06-10 (v0.2.96)
- **구현 패턴 매핑**: programmatic harness (query/ClaudeSDKClient) · custom tools via in-process MCP · **hooks for controlling agent behavior** (= 본 family hook gate 와 동형) · headless 통합. 본 실행 환경 (Claude Agent SDK) 의 토대.
- **매뉴얼 인용 가치**: "trigger from anywhere"(12-factor Factor 11) 의 programmatic 진입점 + hook 기반 behavior 제어의 reference SDK. CLAUDE.md hook 강제 (`artifact-guard`/`spec-skill-gate`) 의 메커니즘적 근거.
- **카드**: `cards/anthropic-managed-agents.md` (인접)
- **Quick verify**: `pip install claude-agent-sdk && python -c "import claude_agent_sdk; print(claude_agent_sdk.__version__)"`

---

## anthropics/claude-code-action

- **url**: https://github.com/anthropics/claude-code-action
- **stars**: ~7.9k
- **language**: TypeScript (~94%)
- **last-update**: 2025-08-26 (v1.0)
- **구현 패턴 매핑**: headless/CI 진입점 · `@claude` 멘션 → PR 자동 생성 (interactive) · prompt 즉시 실행 (automation) · cron schedule trigger · prompt=skill 호출 · CLAUDE.md 준수. Claude Agent SDK 위에 구축.
- **매뉴얼 인용 가치**: "trigger from anywhere" 를 GitHub Actions CI 진입점으로 실체화한 canonical action — 매뉴얼의 headless·cron·gh CLI 권장의 직접 구현.
- **카드**: `cards/claude-code-github-actions.md`
- **Quick verify**: (action 이므로 직접 실행 X) workflow 에 `uses: anthropics/claude-code-action@v1` + `with: prompt:`, `claude_args:` 추가 후 `@claude` 멘션.

---

## All-Hands-AI/OpenHands

- **url**: https://github.com/All-Hands-AI/OpenHands
- **stars**: ~76k
- **language**: Python (~63%)
- **last-update**: 2026-06-10 (Release 1.8.0)
- **구현 패턴 매핑**: full agentic harness (control loop + tool/env interface + execution isolation) · containerized 실행 격리 · multi-entry (CLI/GUI/Cloud/SDK). Inside-the-Scaffold 의 13개 분석 대상 중 하나 (event-sourcing state·containerization).
- **매뉴얼 인용 가치**: harness/scaffold 가 행동을 결정한다는 주장의 대표 OSS 구현. execution isolation (worktree/container 격리) 패턴의 production-scale 예시.
- **카드**: `cards/arxiv-inside-the-scaffold.md` (분석 대상으로 포함)
- **Quick verify**: `docker run -it -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock docker.all-hands.dev/all-hands-ai/openhands:latest` (docs 의 최신 태그 확인 권장)

---

## SWE-agent/SWE-agent

- **url**: https://github.com/SWE-agent/SWE-agent
- **stars**: ~19.5k
- **language**: Python (~95%)
- **last-update**: 2025-05-22 (v1.1.0)
- **구현 패턴 매핑**: Agent-Computer Interface (ACI) 설계 · generate-test-repair loop · SWE-bench 회귀 평가 기반. Inside-the-Scaffold 분석 대상.
- **매뉴얼 인용 가치**: tool/환경 인터페이스 설계 (ACI) 가 agent 성능을 좌우한다는 harness engineering 주장의 학술-인접 구현. eval-driven (벤치 기반) 루프 예시.
- **카드**: `cards/arxiv-inside-the-scaffold.md` (분석 대상)
- **Quick verify**: `pip install swe-agent && sweagent --help` (또는 docs 의 "Hello world from the command line")

---

## Aider-AI/aider

- **url**: https://github.com/Aider-AI/aider
- **stars**: ~46k
- **language**: Python (~80%)
- **last-update**: 2025-08-09 (v0.86.0)
- **구현 패턴 매핑**: terminal pair-programming harness · repo map (PageRank 기반 retrieval) · git 자동 commit (상태 영속) · edit/patch format. Inside-the-Scaffold 분석 대상.
- **매뉴얼 인용 가치**: context retrieval (repo map) + git-as-state 패턴의 경량 reference. harness 의 retrieval/edit-format 차원 예시.
- **카드**: `cards/arxiv-inside-the-scaffold.md` (분석 대상)
- **Quick verify**: `python -m pip install aider-install && aider-install && aider --help`
