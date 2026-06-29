# Addendum A1 — §24.4 브리지: OD `runtimes/` lift vs ACP 채택

> 정조준 질문: ACP(Agent Client Protocol)로 가면 CLI별 어댑터(buildArgs/stream 파서)를 _직접 유지_하는 비용을 표준 계약으로 없앨 수 있나? §24.4 의 **OD-lift 확정**을 정제할 가치가 있나, 아니면 OD 어댑터가 더 실용적인가?
>
> 메타데이터는 GitHub API / npm registry 실측 (2026-06-23 조회). 미확인은 "(미확인)".
>
> **★ 결정적 선행 사실 (조사 중 발견)**: §24.4 의 OD-lift 는 _이미 코드로 구현·커밋됨_ — worktree `worklog-board-wt/studio-c1` 커밋 `34852d4 feat(studio-host): C1 세션호스트 어댑터 — OD runtimes lift`. `studio-host/src/runtimes/` 에 11 파일(총 ~2232 LOC) 실재: `types.ts`(153)·`defs/claude.ts`(102)·`defs/codex.ts`(163)·`claude-stream.ts`(628)·`json-event-stream.ts`(431)·`detection.ts`(382)·`role-marker-guard.ts`(303) 등. 헤더에 `Adapted from open-design (Apache-2.0)` 고지 포함. **즉 이건 "확정을 정제할까"가 아니라 "이미 들인 구현을 갈아엎을까"의 문제** — 권고의 무게추가 결정적으로 달라진다.

---

## 1. ACP 어댑터 현황 표 (2026-06-23 실측)

| 어댑터/CLI | 레포 | ⭐stars | license | 최근 push | 최신 ver | 성숙도·정체 |
|---|---|---|---|---|---|---|
| **claude** (claude-agent-acp) | `agentclientprotocol/claude-agent-acp` | 2,130 | Apache-2.0 | 2026-06-22 | **v0.49.0** (npm `@agentclientprotocol/claude-agent-acp`) | **production·활발** (created 2025-08, 거의 매일 release). ⚠️ **Claude _Agent SDK_ 를 감쌈 (claude code CLI 아님)** — perm/세션이 SDK 모델. ⚠️ npm scope 이전: 구 `@zed-industries/claude-code-acp`(0.16.2) **deprecated**(renamed). org 도 `zed-industries → agentclientprotocol`. |
| **codex** (codex-acp) | `agentclientprotocol/codex-acp` | 41 | NOASSERTION | 2026-06-23 | **v1.0.0** (오늘, npm `@agentclientprotocol/codex-acp`) | **방금 1.0 도달** (created 2025-12). stdio ACP server, Codex App Server 구동. ★ **`CODEX_PATH` 로 내 codex 바이너리 재사용 명시** — "내 PATH CLI 재사용" 제약에 정확 부합. perm/sandbox/approval/MCP 매핑. |
| **gemini** (네이티브) | `google-gemini/gemini-cli` | 105,511 | Apache-2.0 | 2026-06-23 | v0.47.0 | **네이티브 ACP** — `packages/cli/src/acp/`(acpUtils·acpErrors 등) + `docs/cli/acp-mode.md`. 어댑터 불필요, CLI 자체가 ACP agent. |
| **goose** (네이티브) | `aaif-goose/goose` | 50,061 | Apache-2.0 | 2026-06-23 | (활발) | **네이티브 ACP**(`session/prompt`, 외부 `agent-client-protocol` crate + `goose-acp-macros`) _그리고_ `goosed` /reply SSE 둘 다. per-tool 권한 엔진·SQLite 세션. (Rust — TS 하네스면 별도 프로세스.) |
| **(계약)** ACP 프로토콜 | `agentclientprotocol/agent-client-protocol` | 3,480 | Apache-2.0 | 2026-06-23 | TS SDK `@agentclientprotocol/sdk` **0.29.0**(어제 publish) | 와이어 계약 + 다언어 SDK(TS/Rust/Py/Java/Kt). v1 stable + v2 draft 병행. `registry` 레포(257★)에 구현체 카탈로그. |

**성숙도 요약**: gemini(네이티브)·goose(네이티브)는 _완성_. claude(Agent SDK 래퍼)·codex(`CODEX_PATH` CLI 래퍼)는 _별도 npm 어댑터_ 로 활발 유지 — 둘 다 메인테이너가 따로 있어 _내가 안 떠안음_. **단 claude 어댑터는 CLI 가 아닌 SDK 를 감싸는 게 worklog 제약과의 유일한 균열.**

---

## 2. OD 어댑터-lift vs ACP-채택 비교표

| 축 | **OD `runtimes/` lift (§24.4 = 현 구현)** | **ACP 채택** |
|---|---|---|
| **내가 직접 유지하는 코드** | CLI별 어댑터 **~1324 LOC**: `defs/claude.ts`(102)+`defs/codex.ts`(163)+`claude-stream.ts`(628)+`json-event-stream.ts`(431). buildArgs argv·stream 파서 전부 내 책임. | `ClientSideConnection`(`@agentclientprotocol/sdk`) 배선 + `session/update`→SSE 재방출 매핑 **~수백 LOC**. buildArgs·stream 파서 **0**(어댑터가 흡수). |
| **유지비 (CLI 플래그/포맷 변경 추적)** | **내가 떠안음**. claude `-p --input-format stream-json`·`--permission-mode`·codex `exec --json --sandbox`·`-C` argv·`stop_reason`/`stripDuplicateArtifactText`(claude-stream.ts:237-313) — CLI 가 플래그·이벤트 바꾸면 내 파서 깨짐. (OD upstream 이 추적하나 OD pull 도 내가 머지.) | **어댑터 메인테이너가 떠안음** (claude-agent-acp·codex-acp·gemini·goose). CLI 변경 → 어댑터가 흡수, 내 ACP 클라는 불변. _이게 ACP 의 가장 큰 순익._ |
| **권한 모델** | OD ad-hoc + claude `--permission-mode bypassPermissions`(claude.ts:87) → **worklog 정책으로 보정 필요**(§24.2). codex 는 `--sandbox workspace-write` 상속. iframe `sandbox="allow-scripts"` + CSP. | **표준 `session/request_permission` RPC** — 8 후보 중 가장 정식. fs/*·terminal/* 브로커링. 단 _UI 는 여전히 내가 구현_ (계약만 표준). |
| **per-session 연속성** | claude `--resume`/`--session-id`(CLI 보유)·codex 디스크. 디스크 워크스페이스 + JSONL 진실원천(§24.10) — **이미 설계됨**. | ACP `session/load`·`session/new`(id 기반). 표준화되나 _영속화는 어댑터 책임_ — claude-agent-acp 는 SDK 세션, codex-acp 는 codex 세션. worklog 의 "JSONL 직독 재수화"(§24.10) 와 _다른 모델_ — 거울/복원 재설계 필요. |
| **원격 토폴로지 (§24.19 Topology B)** | OD `--expose` ws **실코드 부재(드리프트)** — worklog 신규 구축 필요(§24.19 명시). | ACP 는 **stdio 표준**. 원격은 여전히 stdio↔ws 터널을 _내가_ 깔아야 함(ACP 가 ws 전송을 표준화하진 않음). **더 깔끔히 풀지 않음** — stdio agent 1개를 터널링하는 부담은 OD 와 동급. (오히려 OD 는 spawn cwd 가 이미 로컬이라 터널 경계가 명확.) |
| **드리프트 리스크** | OD upstream 의 `--expose` 부재가 이미 드리프트. claude `bypassPermissions` default 도 worklog 보정 필요. _낮음~중_(코드를 내가 들고 있어 통제 가능, 단 OD 동기화 부담). | claude 어댑터가 **CLI 아닌 SDK** 래퍼 → "내 PATH claude CLI 재사용·`--permission-mode` 정책" 제약과 _구조적 균열_. v1/v2 병행 진화. codex-acp 는 어제 1.0(아직 신생). _중_. |
| **임베드 (Next.js)** | TS 코드 직접 보유 → studio-host 에 그대로. **이미 됨.** | `@agentclientprotocol/sdk`(TS) import. claude/codex 어댑터는 `npx` 자식 프로세스로 spawn(또 다른 프로세스 레이어). |
| **현재 상태** | **✅ 구현·커밋 완료** (worktree studio-c1). 갈아엎으면 매몰. | **0 (재작성)**. C1 폐기 + ACP 재배선. |

---

## 3. ★ spec 반영 권고 — **조건부: §24.4 유지(OD lift), ACP 는 §24.19 에 "swappable 백엔드" 미결로 등재**

### 권고: "§24.4 유지" + "ACP 정제는 조건부 future"

**유지 결정 (지금 OD lift 를 그대로 간다)** — 근거:

1. **매몰비 + 본질 부합**: OD-lift 는 _확정에 그치지 않고 이미 ~2232 LOC 로 구현·커밋_ 됐다(C1 `34852d4`). ACP 전환은 정제가 아니라 _재작성_ 이다. 그리고 worklog 제약("내 PATH claude/codex CLI 재사용, 엔진 교체 X")에 OD 가 더 정확히 맞는다 — OD claude.ts 는 _claude code CLI 자체_ 를 `-p` spawn 하는데, **claude-agent-acp 는 Claude _Agent SDK_ 를 감싼다**(CLI 아님). ACP 로 가면 worklog 의 `--permission-mode`·`--resume`·JSONL 직독(§24.10) 모델이 SDK 세션 모델로 바뀌어 §24.2·§24.10 을 _재설계_ 해야 한다.

2. **원격이 ACP 의 약점 (질문 4 의 반증)**: "ACP 는 stdio 표준이라 원격을 더 깔끔히 푸나?" → **아니다.** ACP 는 stdio _계약_ 만 표준화하고 ws 원격 전송은 표준화하지 않는다. Topology B(§24.19)는 ACP 든 OD 든 똑같이 stdio↔ws 터널을 직접 깔아야 한다. 오히려 OD 는 spawn cwd 가 로컬 워크스페이스(§24.10)라 경계가 명확. ACP 가 §24.19 원격을 더 깔끔히 풀어주지 않으므로 _전환의 명분이 약하다_.

3. **ACP 의 진짜 순익은 "유지비 이전" 하나** — CLI 플래그/스트림 포맷 변경 추적을 어댑터 메인테이너가 떠안는다는 점. 이건 실재하는 이득이나, OD-lift 가 이미 그 ~1324 LOC 를 _작동하는 상태로_ 들고 있고 OD upstream 이 추적을 일부 대신하므로, _지금_ 갈아엎을 만큼 크지 않다. **단 이 이득은 future 에 충분히 커질 수 있다** → 미결로 등재.

### 구체적 spec 변경 (file/section 단위)

- **`spec/prd.md §24.4`**: 변경 없음 (유지). 단 _주석 한 줄 추가_ — "ACP(claude-agent-acp v0.49·codex-acp v1.0·gemini/goose 네이티브)를 swappable 백엔드 대안으로 평가했으나, ① OD-lift 가 이미 C1 구현 완료 ② claude-agent-acp 가 _CLI 아닌 Agent SDK_ 래퍼라 §24.2 권한·§24.10 JSONL 연속성 제약과 균열 ③ 원격(§24.19)을 더 깔끔히 풀지 않음 → 현 lift 유지. addendum_A1 참조."
- **`spec/prd.md §24.19 미결`에 _신규 항목 1개 추가_**: "**ACP swappable 백엔드 (future)** — RuntimeAgentDef 어댑터(§24.4)를 `@agentclientprotocol/sdk` `ClientSideConnection` 으로 추상화해 codex-acp(`CODEX_PATH` 내 바이너리 재사용)·gemini `--acp`·goose 를 _어댑터 0 유지로_ 흡수하는 전환. 트리거: (a) claude code CLI 가 ACP 를 _CLI 네이티브_ 로 지원(현 claude-agent-acp 는 SDK 래퍼라 보류) (b) OD `runtimes/` 유지비가 실측으로 커질 때. 전환 시 §24.10 연속성·§24.2 권한을 ACP `session/load`·`session/request_permission` 으로 재매핑."
- **`spec/prd.md §24.4` codex 단락**: 미세 보강 가능 — codex-acp v1.0 의 `CODEX_PATH` 가 worklog 의 "내 codex 재사용" 을 어댑터 0 으로 달성하는 _가장 가까운 future 진입점_ 임을 메모(codex 쪽이 claude 쪽보다 ACP 전환 장벽이 낮음 — codex-acp 는 CLI 래퍼, claude-agent-acp 는 SDK 래퍼).

### 한 줄 본질
**OD-lift 는 이미 구현됐고 worklog 제약(PATH CLI 재사용·JSONL 연속성·`--permission-mode`)에 더 정확히 맞으며 ACP 가 §24.19 원격을 더 풀어주지도 않는다 → 유지. ACP 의 유일 순익(어댑터 유지비 이전)을 §24.19 의 명시적 future 트리거(claude CLI 네이티브 ACP 지원 / OD 유지비 실측 증가)로 등재해, 갈아엎지 않되 전환 조건을 spec 에 박아 둔다.**
