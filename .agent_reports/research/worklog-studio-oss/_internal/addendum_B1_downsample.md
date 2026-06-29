# Addendum B1 — §25 E4 uPlot 다운샘플 알고리즘 (spec 미해결 공백)

> **대상 공백**: spec §25.8 (E4) 은 대용량 metrics 를 "파일 스트리밍 + 다운샘플 + 라이브 tail-follow" 로 확정했으나, 다운샘플 _알고리즘_ 은 §25.14 미결("LTTB vs stride vs viewport — 구현 cycle 에서 측정 후 확정"). uPlot 은 내장 다운샘플이 없다(README: *"No data parsing, aggregation, summation or statistical processing — just do it in advance"* — WebFetch leeoniya/uPlot, 2026-06-23 실측). 즉 _수만~수백만 step 의 metrics.jsonl 을 uPlot 라이브 곡선으로 줄이는 레이어_ 를 §25 위에 얹어야 한다.
> **렌즈**: local-first · 디스크(jsonl)=SoT · DB 적재 X(파일 스트리밍, §7 lock) · 라이브 tail-follow(증분 선호) · Next.js · MIT/Apache · 경량(uPlot 철학). 기존 §25(uPlot·jsonl·파일스트리밍) 불침범 — 그 위 다운샘플 레이어만 권고.

---

## 1. 알고리즘 비교표

| 알고리즘 | peak 보존 | 증분 친화(tail-follow) | OSS 구현 | license | 비용·특성 |
|---|---|---|---|---|---|
| **min/max decimation** (per-bucket min+max 쌍 보존) | **상** — bucket 내 극값 2점 보존, peak 누락 0 (단 픽셀당 최대 4점 — Chart.js 명시) | **상** — bucket 경계가 step-index 로 **고정**(deterministic). 새 append 는 _마지막 (부분) bucket 만_ 재계산, 앞부분 불변 → 진짜 증분 | uPlot 자체가 이 발상 사용("min/max-per-N-samples 저장 후 추가 다운샘플" — WebSearch 실측) · Chart.js `decimation {algorithm:'min-max'}` (Apache-2.0) | O(n) 1-pass, 단순 buffer. 픽셀당 4점이라 점수는 LTTB 보다 많지만 uPlot 이 166K pts/25ms 라 무관 |
| **LTTB** (Largest-Triangle-Three-Buckets) | **상(모양)·중(극값)** — 삼각형 면적 최대점 선택으로 _곡선 모양_ 우수, 단 극값을 항상 집지는 않음 | **하(순수)** — bucket b 의 선택점이 bucket b+1 의 평균에 의존(look-ahead), append 시 경계 이동하면 전 구간 재계산 경향. 스트리밍 변형은 "고정 bucket 크기" 로 우회하나 마지막 미완 bucket 흔들림 | `janjakubnanista/downsample`(101★·MIT·TS·d.ts) · `pingec/downsample-lttb`(80★·MIT) · Chart.js `'lttb'`(Apache-2.0) · `d3fc` decimation(1.3k★·MIT) | O(n) 1-pass. **정적 뷰·최소 점수 트렌드**에 최적. arxiv MinMaxLTTB(2305.00332)= min-max 선별 후 LTTB 로 스케일(증분 보완 선례) |
| **reservoir sampling** (TensorBoard scalar reservoir, 고정크기 균등) | **하** — 무작위 균등 샘플이라 peak 보존 보장 0(가장 큰 spike 가 탈락 가능) | 중 — 고정 reservoir 에 증분 삽입은 되나, 곡선이 매 갱신마다 _재배치_ 되어 라이브 시 시각적으로 불안정 | TensorBoard 내장(Apache-2.0, 코드 발췌만) | 대용량 scalar(최대 5M step) 검증 선례지만, _시각 충실도_ 보다 _고정 메모리_ 가 목적 |
| **M4** (rasterization-aware: 픽셀열당 min·max·first·last 4점) | **최상** — 픽셀-perfect(원본과 렌더 동일 보장) | 중 — bucket=픽셀열이라 viewport/폭 바뀌면 전면 재계산. **SQL GROUP BY 집계용**(DB 쿼리 1급) | 논문(VLDB 2014) 알고리즘. JS 단독 성숙 라이브러리 약함 — DB(M4 SQL) 친화 | §25 는 DB 적재 X(파일 SoT) → M4 의 본령(SQL 집계)과 어긋남. **부적합** |

---

## 2. 라이브 tail-follow 증분 갱신 패턴 (어디서·어떻게)

- **증분의 핵심 = bucket 경계 안정성**. min/max 와 stride 는 bucket 을 _step-index 절대좌표_ 로 끊으므로(예: bucket k = step [k·B, (k+1)·B)) 새 append 가 들어와도 **앞 bucket 들은 불변, 마지막 미완 bucket 1개만 갱신** → 진짜 O(Δ) 증분. LTTB 는 look-ahead 의존이라 순수 증분이 어렵고, 보통 "확정 구간(앞) + 미확정 tail(끝 몇 bucket) 재계산" 하이브리드로 우회.
- **uPlot 결합**: tail-follow 는 file watcher(§25.2 세션호스트/runner) → SSE `metric_append` → 클라이언트 누적 buffer 에 신규 step push → _마지막 bucket 만_ 갱신한 다운샘플 배열로 `setData()`. uPlot 권장 패턴(WebSearch 실측)은 **큰 배열 pre-alloc + `.subarray()` view 를 setData 에 매 프레임 공급** — 증분 min/max 와 자연 결합(전체 재할당 회피).
- **위치 = 서버(SSE 직전)**: §25.8 은 "파일 스트리밍·DB 적재 X". metrics.jsonl 을 라인 파싱하는 자리(runner/`lib/experiments/stream.ts`)에서 **SSE 로 내보내기 _전_ 다운샘플**하면 (a) 수백만 라인이 클라이언트로 안 흐름(대역폭·메모리), (b) 증분 bucket 상태를 서버가 보유해 O(Δ) 유지. 정밀 정적 뷰(zoom-in)는 클라이언트가 `?from=&to=` 윈도우로 해당 구간만 재요청 → 그 구간 LTTB.

---

## 3. ★ spec 반영 권고 (§25.8 E4 + §25.14)

**1픽 = min/max decimation (증분·peak보존·경량) / 정밀 정적 뷰 보조 = LTTB / 위치 = 서버(runner) SSE 직전.**

- §25.8 line 22 "예: viewport 폭 기준 LTTB/stride 솎기" → **"min/max decimation(라이브 증분 1픽) + 정적 zoom 뷰 LTTB 보조, 위치=runner SSE 직전"** 으로 확정. §25.14 미결 항목("LTTB vs stride vs viewport")은 **본 권고로 해소** (측정 항목으로 남기지 말고 알고리즘 확정 — bucket 크기 B 만 구현 cycle 측정).
- **근거**: (1) **증분성** — min/max 는 bucket 경계가 step-index 고정이라 append 시 마지막 bucket 만 재계산 → tail-follow 의 O(Δ) 요건 충족(LTTB 의 look-ahead 의존은 순수 증분 불가). (2) **peak 보존 + uPlot 정합** — uPlot 자체가 "min/max-per-N-samples 저장 후 다운샘플" 발상을 쓰고 학습곡선의 loss spike·best 마커가 안 잘림(min/max 가 극값 2점 보존). (3) **제약 합치** — 서버측 다운샘플이 §25.8 "파일 SoT·DB 적재 X·대역폭" 과 §25.9 `experiment_metrics` 옵션 캐시(클라우드 coarse 곡선) 양쪽에 동일 코드로 재사용. LTTB 는 정적·최소점 트렌드에서 모양이 더 매끈해 zoom 뷰 보조로만(MIT `janjakubnanista/downsample` 채택). M4·reservoir 는 각각 DB-SQL 본령/시각 충실도 약함으로 탈락.
