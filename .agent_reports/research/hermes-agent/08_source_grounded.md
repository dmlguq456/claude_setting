# 08 — 실소스 grounding: 코드로 검증·정정·보강 (메모리 축 심층)

> 보강 챕터. 기존 `03_memory_system.md`·`cards/axis3_memory.md` 는 docs·2차 자료 기반이라 ❓미검증 항목이 있었다. 본 챕터는 **실소스를 직접 읽어** 그 claim 들을 [CONFIRMED / CORRECTED / FILLED-❓] 로 판정하고 file:line 증거를 박는다. **기존 03/axis3 는 덮어쓰지 않는다** — 정정 사항은 본 챕터의 검증 표에 [CORRECTED] 로 명시한다.

---

## (a) 클론 메타

| 항목 | 값 |
|---|---|
| repo | `github.com/NousResearch/hermes-agent` |
| clone 위치 | `.agent_reports/research/hermes-agent/_ref_src/hermes-agent/` |
| commit SHA | `29c6985590043fc672a6c9a7cdb9a8695388d1ac` |
| commit 날짜·메시지 | `2026-06-15 06:18 -0700` · `fix(nix): refresh npm deps hash` |
| 검증일 | 2026-06-15 |
| 검증 방법 | 메모리 서브시스템 8개 모듈 + cross-axis 진입점 직접 read + grep, 핵심 정정 citation 6건 main-context spot-check 일치 |

> 본 챕터의 모든 `file:line` 은 위 commit 기준. 아래 경로는 전부 `_ref_src/hermes-agent/` 상대.

---

## (b) 코드 구조 맵 — 메모리 서브시스템

기존 연구가 "3층 + optional provider" 로 본 메모리 시스템은 실소스에서 **세 갈래의 독립 메커니즘**으로 구현돼 있다. (이 분리를 03/axis3 는 일부 뭉뚱그렸다 — 아래 (d)·검증표에서 disentangle.)

```
[1] 큐레이트 메모리 파일 (MEMORY.md / USER.md)
    tools/memory_tool.py            MemoryStore — add/replace/remove, char-limit, dup-reject,
                                    threat-scan, frozen snapshot 렌더(용량 헤더), 외부 drift 감지
    tools/write_approval.py         write_approval 게이트 + 파일백 pending 스토어
    hermes_cli/write_approval_commands.py   /memory pending|approve|reject 명령
    agent/background_review.py      in-session "nudge" = 백그라운드 review fork 의 프롬프트
    agent/agent_init.py             nudge_interval(=10)·char-limit·counter 초기화
    agent/turn_context.py           턴 카운터 증가 + 임계 체크 (nudge 트리거 지점)
    agent/turn_finalizer.py         임계 도달 시 _spawn_background_review 호출
    agent/tool_executor.py          memory tool 호출 시 카운터 리셋

[2] SQLite 세션 아카이브 (state.db, FTS5)
    hermes_state.py (4777L)         스키마·마이그레이션·FTS5 2종·search_messages·WAL/retry
                                    └ session_search tool 의 백엔드

[3] 외부 memory provider (단일 active, 교체식)
    agent/memory_provider.py        MemoryProvider ABC (prefetch/sync_turn/get_tool_schemas …)
    agent/memory_manager.py         provider 오케스트레이터 (prefetch_all / 백그라운드 워커)
    plugins/memory/__init__.py      디렉터리 스캔 discovery + register(ctx) 엔트리
    plugins/memory/{honcho,holographic,mem0,hindsight,openviking,
                    retaindb,supermemory,byterover}/   번들 8종
    agent/curator.py (1835L)        skill 수명주기 (active→stale→archived) — 메모리 파일 미관여

[무관] gateway/memory_monitor.py    프로세스 RSS 누수 모니터 — 메모리 *provider* 와 무관 (정정)
```

**cross-axis 진입점 (간단):**
- 축1 아키텍처: `run_agent.py` (`AIAgent`, `_spawn_background_review` @1419), `agent/agent_init.py` (에이전트 초기화·툴셋 바인딩).
- 축2 loop·self-improve: `agent/turn_context.py`(턴 빌드)→`agent/turn_finalizer.py`(턴 마감·백그라운드 review)→`agent/background_review.py`(자기회고 fork). skill 자기개선 nudge 도 같은 경로(`agent_init.py:1203` `_skill_nudge_interval=10`).
- 축4 보안: `tools/threat_patterns.py`(injection/exfil 패턴, `scan_for_threats`/`first_threat_message`), 메모리 write·snapshot 양쪽에서 호출.

---

## (c) Claim 검증 표 — 03 / axis3 의 주요 claim별 판정

> 범례: **CONFIRMED** = 소스가 claim 그대로 확인 / **CORRECTED** = claim 이 실소스와 다름(정정) / **FILLED-❓** = 기존 ❓미검증 항목을 소스로 해소 / **REFINED** = 방향은 맞으나 메커니즘 정밀화.

### C1 — 3층 아키텍처 + skill 수명주기

| # | 기존 claim (03/axis3) | 판정 | 실소스 증거 |
|---|---|---|---|
| 1 | 메모리 = curated 파일 + SQLite archive + optional provider 3층 | **CONFIRMED** | `tools/memory_tool.py` (파일) · `hermes_state.py` (archive) · `agent/memory_provider.py`+`plugins/memory/` (provider) |
| 2 | char limit MEMORY 2,200 / USER 1,375 | **CONFIRMED** | `tools/memory_tool.py:124` `def __init__(self, memory_char_limit=2200, user_char_limit=1375)` |
| 3 | memory tool actions = add/replace/remove, **read action 없음** | **CONFIRMED** | dispatch `tools/memory_tool.py:700-710`, schema enum `:768-771` `["add","replace","remove"]`. ⚠️주의: 모듈 docstring `:20` 등이 아직 `read` 를 언급하나 **stale 문서** (dispatch·schema 엔 없음). |
| 4 | replace/remove 는 `old_text` substring matching | **CONFIRMED** | `:369` `matches = [(i,e) for i,e in enumerate(entries) if old_text in e]` (remove 도 `:426` 동일). 복수 distinct 매치 → "be specific" 에러. |

### C2 — agent-curated write + write_approval

| # | 기존 claim | 판정 | 실소스 증거 |
|---|---|---|---|
| 5 | write_approval `false`(default)=자유, `true`=approval 필요·background write 는 pending staged | **CONFIRMED** | `tools/write_approval.py:74-89` (`write_approval_enabled`, default `False`), `evaluate_gate:274-275` off→allow. background-origin write 는 항상 stage(`:277,:281`). |
| 6 | pending 검토 명령 `/memory pending·approve·reject·approval on/off` | **CONFIRMED** | `hermes_cli/write_approval_commands.py:84-97` dispatch. `_approve:108-138` (replay 후 discard), `_reject:158-170`. |
| 6b | (pending 스토어 구현 = ❓ 미상) | **FILLED-❓** | **파일백 JSON**, 레코드당 1파일: `<HERMES_HOME>/pending/{memory,skills}/<id>.json`, atomic `os.replace` (`tools/write_approval.py:110-151`). |
| 7 | promote/skip 휴리스틱 (선호·교정→저장, trivia→skip) | **CORRECTED (성격 정정)** | 이건 **코드 게이트가 아니라 model-facing 프로즈**다. 툴 schema description `tools/memory_tool.py:742-764` ("WHEN TO SAVE…/SKIP…") + background review 프롬프트. 실제 *코드로 강제되는* write 게이트는 emptiness·exact-dup·char-limit·threat-scan 뿐 — 의미 분류기는 없음. → **03 §7 표가 "우리는 프로즈, Hermes 는 코드 게이트" 처럼 읽히게 한 부분은 정정**: 양쪽 다 프로즈다(아래 (e) 참조). |

### C3 — periodic nudge (자기회고)

| # | 기존 claim | 판정 | 실소스 증거 |
|---|---|---|---|
| 8 | nudge = 사용자 아닌 **에이전트 자신에게** 보내는 internal 회고 프롬프트 | **CONFIRMED** | `agent/background_review.py:34-43` `_MEMORY_REVIEW_PROMPT` ("Review the conversation above and consider saving to memory… If nothing is worth saving, just say 'Nothing to save.'"). fork 된 review 에이전트에 user_message 로 주입(`:486-491`, 툴은 memory/skill 로 제한). |
| 9 | (a) 턴 카운터: user 턴마다 `turns_since_memory`++, `>= nudge_interval` 이면 background review | **CONFIRMED + FILLED-❓** | `agent/turn_context.py:209-217` — 게이트 조건 `_memory_nudge_interval>0 AND "memory" in valid_tool_names AND _memory_store`, 충족 시 `_turns_since_memory += 1`, `>= 임계` 면 `should_review_memory=True` 후 0 리셋. 발사: `agent/turn_finalizer.py:393-401` `_spawn_background_review(...)`. |
| 9b | **정확한 `nudge_interval` 턴 수치** (1차 미노출 ❓) | **FILLED-❓ = 10** | `agent/agent_init.py:1113` `agent._memory_nudge_interval = 10`, config override `:1121` `int(mem_config.get("nudge_interval", 10))`. (skill 측도 `:1203` `=10`.) |
| 9c | (메커니즘 정밀화) | **REFINED** | memory tool 을 *실제로 호출*하면 카운터 0 리셋(`agent/tool_executor.py:268-270`, `:863-867`) → nudge 는 "**memory write 없이 10턴 경과**" 시에만 발사. resume 시 prior 히스토리로 hydrate(`turn_context.py:191-192`). |
| 10 | nudge 가 승격뿐 아니라 **레이어 배치 결정**까지 수행 | **REFINED (격하)** | `_MEMORY_REVIEW_PROMPT` 자체는 user persona/선호/행동기대만 묻는다 — "어느 레이어" 의 명시 분기는 nudge 프롬프트엔 없고 툴 description 프로즈에만 있다. → "레이어 배치까지 수행"은 *프로즈 암시* 수준, 별도 메커니즘 아님. |

### C4 — FTS5 cross-session recall (스키마·검색)

| # | 기존 claim | 판정 | 실소스 증거 |
|---|---|---|---|
| 11 | 전 세션이 `state.db`(SQLite WAL)에 적재, `session_search` 가 FTS5 로 full-text 검색 | **CONFIRMED** | `hermes_state.py` search 백엔드 `search_messages`(@3227~), WAL fallback `apply_wal_with_fallback:266`. |
| 12 | **schema_version = 11** | **CORRECTED → 16** | `hermes_state.py:110` `SCHEMA_VERSION = 16`. 버전은 전용 `schema_version` 테이블(`:510`)에 저장(state_meta 아님). |
| 12b | (마이그레이션 흐름 = 개략 ❓) | **FILLED-❓** | migrations 리스트/`apply_migrations` 함수 **없음**. 대신 ① 컬럼은 `_reconcile_columns()` 가 live↔SCHEMA_SQL diff 로 선언적 추가, ② *데이터* 마이그레이션만 `if current_version < N:` 인라인 게이트. 열거 가능 스텝: `<10` trigram 테이블 신설+백필(`:1126`), `<11` **FTS 2종 drop·재생성(external-content→inline 전환, `content‖tool_name‖tool_calls` 인덱싱)** (`:1149`), `<12` `messages.active=1` 백필(`:1199`), `<16` delegate/orphan subagent 태깅(`:1211`). 최종 bump 는 FTS 마이그레이션 완료 게이트 후(`:1237`). |
| 13 | `messages_fts` = **external content mode** (`content=messages, content_rowid=id`) | **CORRECTED** | 현 스키마는 **inline/standalone** — 단일 `content` 컬럼, **default unicode61**(tokenize 미지정), `content=`·`content_rowid` **없음**. `hermes_state.py:601-604` `CREATE VIRTUAL TABLE … messages_fts USING fts5(content)`. external-content 형태는 **pre-v11 폐기형** — `<11` 마이그레이션이 drop 후 inline 으로 재생성(`:1149`, 테스트 `tests/test_hermes_state.py:3625` 가 구형을 만들어 업그레이드 검증). → 03/axis3 가 인용한 `content=messages` DDL 은 옛 버전. |
| 14 | `messages_fts_trigram` = trigram tokenizer | **CONFIRMED** | `hermes_state.py:630-634` `… USING fts5(content, tokenize='trigram')`. 역시 standalone. |
| 15 | INSERT/UPDATE/DELETE 3 trigger 로 messages→messages_fts 싱크, delete 는 `INSERT … VALUES('delete', …)` external-content 관용구 | **CORRECTED** | trigger 는 맞으나 **inline 관용구**: delete = `DELETE FROM messages_fts WHERE rowid=old.id`(`:614`), insert 는 `content‖' '‖tool_name‖' '‖tool_calls` 를 인덱싱(raw content 아님, `:607-612`). 그리고 trigram 은 **자체 별도 trigger 세트**(`:636-653`, `_FTS_TRIGGERS:149-156`) — 같은 trigger 가 두 테이블을 싱크하지 않는다. |
| 16 | search 결과 = `>>>match<<<` snippet + 주변 context + 세션 메타 | **CONFIRMED** | `snippet(messages_fts,0,'>>>','<<<','...',40)` (`:3320`; trigram `:3391`). 주변 1메시지 전/후(≤200char) `WITH target … UNION ALL`(`:3470-3528`). |
| 17 | 쿼리 sanitize (unmatched quote/hyphen/dangling operator) | **CONFIRMED** | `_sanitize_fts5_query:3139-3194` 6스텝 (balanced quote 보존→특수문자 strip→`*` 정규화→dangling AND/OR/NOT 제거→하이픈/점/언더스코어 term quote→복원). |
| 18 | WAL: 1s busy timeout, app retry(20–150ms jitter, max 15), checkpoint 50write마다 **PASSIVE** | **CORRECTED (부분)** | retry 상수 CONFIRMED: `_WRITE_MAX_RETRIES=15`·`_WRITE_RETRY_MIN_S=0.020`·`_WRITE_RETRY_MAX_S=0.150`·`_CHECKPOINT_EVERY_N_WRITES=50`(`:674-678`). 단 ① busy timeout 은 **`PRAGMA` 아니라 드라이버 `timeout=1.0`**(`:718`), ② checkpoint 는 **`PRAGMA wal_checkpoint(TRUNCATE)`**(`:945-948`) — 상수 주석은 "PASSIVE" 라 쓰였으나 실제 PRAGMA 는 TRUNCATE. |
| 19 | **bm25 ranking 적용 여부** (❓ doc 미노출) | **FILLED-❓** | FTS5 `rank` 컬럼 사용(= bm25 default). **명시적 `bm25(...)` 호출은 파일 전체에 0건.** ORDER BY: default `ORDER BY rank`, newest/oldest 는 `m.timestamp DESC/ASC, rank`(`:3284-3289`, trigram 재사용 `:3402`). |
| 20 | **messages_fts(unicode61) ↔ messages_fts_trigram 결합 로직** (❓ 핵심) | **FILLED-❓ (재프레이밍)** | **결합(union/fallback)이 아니라 CJK 감지 기반 상호배타 3-way 라우팅**이다 — 쿼리 전체가 정확히 한 경로로 간다. ① 비-CJK → `messages_fts`(unicode61) (`:3460-3468`). ② CJK 이고 `cjk_count>=3 AND 모든 CJK 토큰 ≥3자` → `messages_fts_trigram` 만 (`:3361-3412`, 실패 시 `matches=[]`, fallback 안 함). ③ short/mixed CJK(토큰 <3 CJK자, 예 `广西 OR 桂林`) → **LIKE substring** (`:3413-3459`). 결과는 다른 경로와 **머지하지 않음**. (trigram 은 ≥9 UTF-8 byte=3 CJK자 필요, #20494.) |

### C5 — Honcho / provider 시스템

| # | 기존 claim | 판정 | 실소스 증거 |
|---|---|---|---|
| 21 | provider 9종 (Honcho·OpenViking·Mem0·Hindsight·Holographic·RetainDB·ByteRover·Supermemory·Memori) | **CORRECTED (qualify)** | 하드코딩 registry 없음 — `plugins/memory/__init__.py:90-121` **디렉터리 스캔** discovery. 번들은 **8 디렉터리**(byterover·hindsight·holographic·honcho·mem0·openviking·retaindb·supermemory). **Memori 는 out-of-tree pip 플러그인**(`pip install hermes-memori`, `memory-providers.md:529`) — 번들 8 + Memori = 문서상 9. **동시 1개만 active**(`memory.provider` config). |
| 22 | unified interface | **CONFIRMED** | `agent/memory_provider.py:42` `class MemoryProvider(ABC)`. abstract: `name`/`is_available`/`initialize`/`get_tool_schemas`. recall=`prefetch()`(`:93`), persist=`sync_turn()`(`:115`) — `search`/`write` 라는 단일 메서드는 없고 provider 별 `handle_tool_call`. |
| 23 | 턴 전 background prefetch (non-blocking) | **CONFIRMED + REFINED** | tool loop 전 1회 `prefetch_all`(`agent/turn_context.py:367-372`), 턴 후 `queue_prefetch`(`agent/turn_finalizer.py:383-389`). **thread 기반(asyncio 아님)** — `MemoryManager.queue_prefetch_all` 가 백그라운드 워커로 디스패치(`agent/memory_manager.py:452-471`), Honcho 가 `threading.Thread` 레퍼런스 구현(`plugins/memory/honcho/__init__.py:198-201`). |
| 24 | Honcho 5 tool, 외부 FastAPI 서비스, HONCHO_API_KEY | **CONFIRMED (정밀화)** | 5 tool `ALL_TOOL_SCHEMAS`(`honcho/__init__.py:184`): profile·search·reasoning·context·conclude. 클라이언트는 **official `honcho` SDK over HTTP**(`client.py:29 from honcho import Honcho`), `HONCHO_API_KEY`/`HONCHO_BASE_URL`(`:390-391`) — raw httpx/requests 아니고 로컬 FastAPI 서버도 아님(SDK→cloud/self-host). |
| 25 | Holographic = local SQLite+FTS5+trust+HRR, `fact_store` 9 action, `$HERMES_HOME/memory_store.db` | **CONFIRMED (전부)** | 9 action enum `holographic/__init__.py:57-60` `[add,search,probe,related,reason,contradict,update,remove,list]`. DB `$HERMES_HOME/memory_store.db`(`:160-162`). FTS5 `facts_fts`(`store.py:48-49`). trust `trust_score REAL DEFAULT 0.5`(`store.py:22`), 피드백 +0.05/−0.10(`:356-357`). HRR `hrr_vector BLOB`(`store.py:27`) + bind/unbind(`retrieval.py:135-137`, dim default 1024). |

### C6 — 수명주기 / Curator

| # | 기존 claim | 판정 | 실소스 증거 |
|---|---|---|---|
| 26 | capacity-driven consolidation: 한도 도달 시 memory tool 이 **error 반환**, 같은 턴 재시도(silent drop 아님) | **CONFIRMED** | `add` `:328-341` `if new_total > limit: return {"success":False, "error":"… Consolidate now: use 'replace'…/'remove'… then retry this add — all in this turn.", "current_entries":entries, "usage":…}`. replace 도 대칭 가드 `:394-406`. |
| 27 | exact duplicate 자동 거부 | **CONFIRMED** | `add` `:320-322` `if content in entries: return …"(no duplicate added)"`. load 시 dedup(`:157-158`). |
| 28 | injection/exfiltration 패턴 스캔 | **CONFIRMED** | write 전 `_scan_memory_content(content)` strict scope(`:78-80`, 호출 `:304-306`/`:359-361`), snapshot 빌드 시 위반 엔트리 `[BLOCKED:…]` 치환(`:185-205`). 라이브러리 `tools/threat_patterns.py:187/227`. |
| 28b | 용량 헤더 `[67% — 1,474/2,200 chars]` | **CONFIRMED** | `_render_block:482-498` `header = f"MEMORY (your personal notes) [{pct}% — {current:,}/{limit:,} chars]"`. snapshot 에 freeze. |
| 29 | Curator: inactivity check, `interval_hours`=168h(7d) AND `min_idle_hours`=2h | **CONFIRMED** | `agent/curator.py:56` `DEFAULT_INTERVAL_HOURS = 24*7`, `:57` `DEFAULT_MIN_IDLE_HOURS = 2`. 단 두 게이트는 **별 함수**: interval 은 `should_run_now`(`:247-248`), idle 은 `maybe_run_curator`(`:1828-1831`). |
| 29b | 트리거 = CLI 세션 시작 + gateway cron-ticker | **CONFIRMED** | CLI: `cli.py:11038-11045` `maybe_run_curator(idle_for_seconds=inf)`. gateway: `gateway/run.py:16156-16162`, 폴 `CURATOR_EVERY=60`틱(시간당, 내부 게이트가 7일 cadence 강제). |
| 30 | skill `active→stale→archived` 자동 전이 (usage telemetry) | **CONFIRMED + FILLED-❓** | 상태 문자열 `tools/skill_usage.py:53-55` `"active"/"stale"/"archived"`. 전이는 **마지막 활동 timestamp 기반**(use-count 아님): idle ≥30d→stale, ≥90d→archived, 30d 내 재사용 시 stale→active 복귀 (`agent/curator.py:58-59` `STALE=30/ARCHIVE=90 days`, 로직 `:271-308`). telemetry `~/.hermes/skills/.usage.json`(`skill_usage.py:85-86`). 산출물 `~/.hermes/logs/curator/{YYYYMMDD-HHMMSS}/{run.json,REPORT.md}`(`:504,1031,1172,1182`). |
| 30b | (Curator 가 메모리 파일도 정리하나?) | **CORRECTED (분리)** | Curator 는 **skill 전용** — MEMORY.md/USER.md 미참조, review fork 는 `skip_memory=True`(`curator.py:1760`). 메모리 파일 정리는 [1]의 in-session nudge(background_review)·capacity error 경로지 Curator 가 아니다. → 03/axis3 가 nudge(메모리)와 Curator(skill)를 같은 "자기회고" 묶음으로 둔 부분을 **두 독립 메커니즘으로 분리**. |
| 31 | gateway memory monitor = provider prefetch 관련 | **CORRECTED** | `gateway/memory_monitor.py` 는 **프로세스 RSS 누수 모니터** (`[MEMORY] rss=… ` 라인 주기 emit, default 300s, `:139-193`) — 메모리 *provider*·prefetch 와 **무관**. (조사 대상 파일 목록의 추정이 빗나간 케이스.) |

**집계: 검증 claim 31개 → CONFIRMED 17 · CORRECTED 8 · FILLED-❓ 8 · REFINED 4** (일부 셀은 복합 판정이라 합이 31 초과 — CORRECTED·FILLED 가 같은 행에 겹친 경우 포함).

---

## (d) ❓ 항목 해소 결과 (프롬프트 6개 미검증 항목)

| ❓ 항목 | 해소 | 증거 |
|---|---|---|
| **periodic nudge 의 정확한 `nudge_interval`** | **10턴** (config `memory.nudge_interval` override). 카운터는 `turn_context.py` 에서 user 턴마다 ++, memory tool 실제 호출 시 0 리셋 → "write 없이 10턴" 시 background review fork 발사. | `agent_init.py:1113,1121` · `turn_context.py:209-217` · `turn_finalizer.py:393-401` · `tool_executor.py:268-270,863-867` |
| **session_search bm25 ranking + 이중 테이블 결합 로직** | bm25 = FTS5 `rank` 컬럼(암묵, 명시 `bm25()` 0건). **결합 로직은 존재하지 않음** — CJK 감지로 unicode61 / trigram / LIKE 중 **하나로 라우팅**(상호배타, 머지 없음). | `hermes_state.py:3284-3289`(rank) · `:3344-3468`(3-way 라우팅) |
| **state.db `schema_version` 실값 + 마이그레이션** | **16**. migrations 리스트 없이 `_reconcile_columns`(선언적 컬럼) + `if current_version<N` 인라인 데이터 마이그레이션(10/11/12/16). | `hermes_state.py:110,510,1113-1237` |
| **Curator `interval_hours`/`min_idle_hours` default + 전이** | 168h / 2h. active→stale(30d)→archived(90d), last-activity timestamp 기반·use-count 아님, 30d 내 재사용 시 stale→active 복귀. | `curator.py:56-59,247-248,271-308,1828-1831` |
| **write_approval 게이트 + promote/skip 휴리스틱 위치** | 게이트 = `tools/write_approval.py`(default false, true 시 `<HERMES_HOME>/pending/<sub>/<id>.json` 파일백 staging). promote/skip = **코드 게이트 아님, 툴 description·review 프롬프트의 프로즈**. | `write_approval.py:74-151` · `memory_tool.py:609-663,742-764` |
| **capacity-driven consolidation (char limit, error-on-full)** | 2200/1375 char, 초과 시 **error 반환**("Consolidate now… retry… all in this turn") + `current_entries`·`usage` 동봉. silent drop 아님, exact-dup 거부, threat-scan. | `memory_tool.py:124,320-341,394-406` |

---

## (e) 우리 시스템(mem.py DB-SoT) 대조

우리는 방금 markdown-SoT → SQLite `memory.db` 로 전환했고(`tools/memory/mem.py`, 40KB), FTS5(unicode61)+trigram, working/durable tier, inject/sync hook 을 구현했다. Hermes 실구현과 메커니즘별로 맞대 본다. (03 §7 표를 *코드 근거로* 갱신하는 자리.)

### e-1. cross-session 검색 — **여기서 설계가 갈린다**

| | Hermes (`hermes_state.py`) | 우리 (`mem.py`) |
|---|---|---|
| 테이블 | `messages_fts`(unicode61) + `messages_fts_trigram` | `records_fts`(unicode61) + `records_trig`(trigram) |
| 결합 | **상호배타 3-way 라우팅** (CJK 감지 → 하나만) | **unicode61 항상 실행 + CJK 시 trigram UNION/dedup** (`mem.py:402-441`) |
| ranking | `rank`(암묵 bm25) | **명시 `ORDER BY bm25(records_fts)`** (`mem.py:408,422`) |
| LIKE fallback | short/mixed CJK 전용 경로 | trigram 불가 시 + FTS 실패 시 (`mem.py:430-455`) |

**핵심 차이**: Hermes 는 쿼리를 한 토크나이저로 *라우팅*하므로, CJK 쿼리에선 unicode61 매치가, Latin 쿼리에선 trigram 매치가 **서로 안 보인다**. 우리는 unicode61 을 *항상* 돌리고 CJK 일 때 trigram 결과를 **합집합**(seen_ids dedup)으로 얹는다 → **한·영 혼용**(한국어 산문 + 영어 code/path/metric 토큰, 우리의 실제 사용 패턴)에 더 강하다. 우리 쪽이 mixed-script recall 에선 앞선다고 볼 근거. 단 Hermes 의 라우팅은 trigram noise(짧은 CJK 토큰)를 LIKE 로 빼는 #20494 케어가 있어, 짧은 CJK 검색의 정밀도는 더 챙긴다 — 우리가 차용할 디테일.

> 03 §7 의 "FTS5 자동 cross-session recall = Hermes 의 결정적 우위, 우리는 주입+수동 recall 뿐" 은 **이번 전환으로 좁혀졌다**: 우리도 `mem recall` 이 FTS5+trigram+bm25 로 cross-cwd/cross-session 검색을 한다. 남은 갭은 *자동 트리거*(Hermes 는 `session_search` 를 에이전트가 턴 중 자율 호출) 쪽이지, 인덱스·랭킹 능력이 아니다.

### e-2. write 게이트 / promote-skip — **수렴 (03 정정)**

03 §7 표는 "Hermes = write_approval 게이트 + promote/skip 휴리스틱 / 우리 = 프로즈 가이드, 코드 게이트 없음 → Hermes 앞섬" 처럼 읽혔다. **소스 확인 결과 정정**: Hermes 의 promote/skip 도 **코드 분류기가 아니라 프로즈**(`memory_tool.py:742-764` 툴 description) — 우리가 CLAUDE.md/instruction 에 두는 것과 같은 층위다. Hermes 가 *실제로* 코드로 강제하는 건 emptiness·exact-dup·char-limit·threat-scan 네 가드뿐.
- **우리 대비**: 우리 `mem.py` 도 write 시 `sanitize()` 로 injection-pattern·secret-masked 플래깅(`mem.py:250-256,278`), durable near-dup 플래깅(`:776,798` "consolidate 후보 — 자동삭제 X"). threat-scan·dedup 은 **양쪽 다 코드 가드로 보유** = 수렴.
- **진짜 차이는 write_approval 게이트**: Hermes 는 background-origin write 를 pending JSON 으로 staging 후 사람이 approve(`/memory approve`). 우리는 §7 자동 write 불변식(confirm 없이 저장, prune/삭제만 confirm). **trade-off** — Hermes=안전(검토 게이트)·마찰↑, 우리=연속성(fire-and-forget)·마찰↓. 우리 정책상 우위 아닌 *의도된 선택*.

### e-3. 자동 회고 트리거 — **Hermes 앞섬(턴 카운터), 단 우리 nudge 와 층위 다름**

- Hermes: `nudge_interval=10` 턴 카운터 → background review **fork**(별 에이전트가 대화 snapshot 보고 memory tool 자율 호출). 완전 자동.
- 우리: 턴 카운터 없음. context ~50%+/wind-down 신호 시 working tier 자동 write(§7 불변식) — *메인 Claude 자신*이 기록(별 fork 아님).
- **차용 후보**: 턴 카운터 기반 자동 회고는 우리에 명시적 기계가 없다. 단 우리 working auto-write 가 기능적으로 일부 대체. Hermes 의 "write 없이 N턴 → 회고" 발사 조건은 hook 으로 이식 가능한 패턴.

### e-4. capacity 규율 — **다른 메커니즘, 같은 목표**

- Hermes: 하드 char ceiling(2200/1375) + **error-on-full** 로 같은 턴 consolidation 강제. 시간 기반 prune 없음.
- 우리: working tier **TTL `expires`** 자동 만료(`mem.py:775` `tier='working' AND expires < today`) + durable **near-dup 플래깅**(자동삭제 X, consolidate 후보 표시). tier 분리로 용량 압박을 구조적으로 분산.
- **평가**: Hermes 의 error-on-full 은 "꽉 차면 즉시 정리" 를 강제하는 영리한 장치 — 우리 durable 엔 그런 강제 게이트가 없다(near-dup 은 플래깅만). working TTL 은 우리가 가진 추가 축. **차용 후보**: durable 에도 soft ceiling + "consolidate 후보 N건" 경고를 inject 에 띄우는 것.

### e-5. 그대로 유효한 우리 우위

- **행동양식 ≠ memory** 분리(원칙 문서가 단일 출처) — Hermes 는 행동기대도 USER.md 에 쌓음(`_MEMORY_REVIEW_PROMPT` 가 "how you should behave" 를 저장 대상으로 명시). 우리는 관심사 분리·버전관리에서 앞섬. (03 §7 결론 유지.)
- **DB-SoT + git-tracked `dump.jsonl` 결정론 mirror**(`mem.py:489-514`) — Hermes state.db 는 git 미추적 런타임 아카이브. 우리는 SoT(DB)와 추적가능 텍스트 mirror 를 분리 → 메모리 변화의 diff/리뷰 가능. 우리 고유.

### e-6. 종합 — 갱신된 메모리 축 스코어카드

| 메커니즘 | 이전(03 §7) 판정 | 소스 확인 후 갱신 |
|---|---|---|
| cross-session FTS recall | Hermes 앞섬(큰 갭) | **거의 동등** — 우리도 FTS5+trigram+bm25. 우리는 mixed-script UNION 으로 일부 앞서고, Hermes 는 short-CJK 라우팅·자동 turn-call 로 일부 앞섬 |
| write_approval / promote-skip | Hermes 앞섬(게이트) | **promote-skip 은 수렴(둘 다 프로즈)**; write_approval 게이트만 Hermes 고유(trade-off) |
| 자동 회고 트리거 | Hermes 앞섬 | 유지 — 턴 카운터(=10)는 우리에 없음(working auto-write 가 부분 대체) |
| capacity 규율 | Hermes 앞섬 | 유지 보완 — Hermes error-on-full vs 우리 TTL+near-dup, 메커니즘 상이 |
| 행동양식 분리 / DB-SoT+mirror | 우리 앞섬 | **유지·강화** |

**최종 Takeaway(갱신)**: 03 이 "FTS5 자동 recall = Hermes 결정적 단일 우위" 라 했으나, **memory.db 전환으로 인덱스·랭킹 갭은 사실상 닫혔다.** 남은 진짜 갭은 두 가지 — ① `session_search` 를 에이전트가 턴 중 *자율 호출*하는 통합(우리는 `mem recall` 이 사람·hook 트리거), ② `nudge_interval`-류 *자동 턴 카운터 회고*. 이식 1순위는 이 둘로 재조준된다. 반대로 promote/skip 게이트 갭은 *환상*이었다(양쪽 프로즈) — 굳이 코드 분류기를 만들 이유는 소스에 없다.

---

## 부록 — 본 챕터가 정정한 03/axis3 진술 요약 (CORRECTED 목록)

1. `schema_version` **11 → 16** (C12).
2. `messages_fts` external-content(`content=messages, content_rowid`) → **inline standalone(content only)** (C13); pre-v11 폐기형이 인용됨.
3. FTS delete-trigger external-content 관용구 → **inline `DELETE … WHERE rowid`**, trigram 은 별도 trigger 세트, content 는 `content‖tool_name‖tool_calls` (C15).
4. 이중 테이블 "결합 로직" → **결합 없음, CJK 3-way 라우팅** (C20).
5. WAL busy timeout = PRAGMA → **드라이버 `timeout=1.0`**; checkpoint PASSIVE → **TRUNCATE** (C18).
6. provider "9종" → **번들 8 + out-of-tree Memori**, 하드 registry 없이 dir 스캔 (C21).
7. promote/skip = (Hermes 코드 게이트로 읽힘) → **양쪽 다 프로즈**, 코드 가드는 dup/limit/threat 뿐 (C7, e-2).
8. nudge(메모리)와 Curator(skill)를 한 회고 묶음 → **두 독립 메커니즘**, Curator 는 skill 전용(`skip_memory=True`) (C30b).
9. `gateway/memory_monitor.py` = provider 관련 추정 → **프로세스 RSS 누수 모니터, 무관** (C31).
