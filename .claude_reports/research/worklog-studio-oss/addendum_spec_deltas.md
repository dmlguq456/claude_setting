# Addendum — spec-grounded research 보완 (§24/§25 정조준)

> **조사일** 2026-06-23 · **목적**: 1차 research(`00_briefing.md`)는 worklog-board spec이 §24(스튜디오)·§25(실험대시보드)로 *이미 구체적 lift 타깃을 확정*(일부는 studio-c1에 구현·커밋)했다는 걸 모른 채 한 generic 랜드스케이프였다. 본 addendum은 그 결과를 **spec의 실제 확정 결정·미결(§24.19·§25.14)에 정조준해 재평가**한다.
> **spec은 건드리지 않았다** — 본 문서는 research addendum이며, 실제 spec 반영은 사용자 결정 후 `autopilot-spec update`로.
> **상세 근거**: `_internal/addendum_A1_bridge.md` · `_internal/addendum_A2_canvas.md` · `_internal/addendum_A3B2_verify.md` · `_internal/addendum_B1_downsample.md`

---

## ★ 메타 결론 (헤드라인)

**정조준 보완의 순효과 = spec 검증 + 오정제 3건 차단 + 진짜 추가 2건.**

1차 briefing이 "정제 후보"로 민 3건(ACP·Sandpack·odiff)은 **spec의 확정 결정에 대질하니 전부 _전환 비권고_** 로 뒤집혔다 — 즉 spec의 기존 선택(OD-lift·srcdoc·getBoundingClientRect)이 worklog 제약에 더 맞는다는 게 외부 대안 조사로 *역으로 검증*됐다. 반면 spec이 미결로 남긴 자리에선 **진짜 새 값 2건**(E4 다운샘플 알고리즘 확정·검증 사다리 axe-core 편입)을 건졌다.

| # | 정조준 | 1차 briefing 제안 | spec 대질 후 결론 | 성격 |
|---|---|---|---|---|
| A1 | §24.4 브리지 | ACP로 정제 | **OD-lift 유지** (이미 studio-c1 구현·커밋, ACP는 future 트리거) | 오정제 차단 |
| A2 | §24.5 캔버스 | Sandpack/renderify | **srcdoc 유지** (Sandpack self-host 골격 stale·renderify는 CDN본드) | 오정제 차단 |
| A3+B2 | §24.12 검증 | odiff 게이트 | **getBoundingClientRect 유지** + **axe-core 신규 편입** | 오정제 차단 + 진짜 추가 |
| B1 | §25 E4 다운샘플 | (1차 미조사) | **min/max decimation 확정** (§25.14 미결 해소) | 진짜 추가 |

> **Takeaway**: research를 spec에 정조준하니 "새 OSS를 갈아끼우자"가 아니라 "spec이 옳다는 외부 검증 + 미결 2곳 채움"이 됐다. odiff 같은 generic 픽은 *생성 UI*라는 본질 앞에서 무너졌다(baseline 전제). 이게 1차 랜드스케이프가 못 본 자리다.

---

## spec 반영 권고표 (autopilot-spec update 시 적용할 것)

| 자리 | spec 기존 결정 | research 발견 | ★ 권고 | 구체 변경 위치 |
|---|---|---|---|---|
| **§24.4 브리지** | OD `runtimes/` lift (claude.ts·codex.ts buildArgs·claude-stream.ts) — **studio-c1 `34852d4`에 ~2232 LOC 구현 완료** | ACP 어댑터(claude-agent-acp v0.49·codex-acp v1.0·gemini/goose 네이티브) 성숙 중. 단 claude-agent-acp는 *CLI 아닌 Agent SDK* 래퍼 | **유지** + ACP를 §24.19 future 미결로 등재 | §24.4 주석 1줄 + §24.19 신규 미결 "ACP swappable 백엔드 (트리거: claude CLI 네이티브 ACP / OD 유지비 실측 증가)" |
| **§24.5 캔버스** | srcdoc + self-host React (OD `srcdoc.ts`·`react-component.ts` lift, unpkg→self-host inline) | Sandpack self-host 핵심 `sandpack-bundler` ⭐89·19개월 정체 / renderify는 JSPM CDN 본드(드리프트 계승) | **유지** + renderify 패턴만 escape hatch 참고 | §24.5 끝 drift 기록 1줄 + §24.19 옆 "multi-file/npm 의존 확장 시 import-map(blob) 또는 Sandpack 재평가" 트리거 |
| **§24.12 검증** | forked verifier + OCD parity + getBoundingClientRect 픽셀측정 + 폴백 사다리 | odiff는 baseline 전제라 *생성물 부적합*(exit 21=차원불일치≠레이아웃붕괴). baseline-free lint가 정답 | **유지** + baseline-free 사다리 1차 명문화 + **axe-core 편입** + odiff 위치 격하 | §24.12에 게이트 순서 명문화 / axe-core(`@axe-core/playwright`, MPL-2.0) 객관 WCAG 추가 / odiff는 "고정 reference PNG 존재 시만 보조" |
| **§25 E4 다운샘플** | "파일 스트리밍 + 다운샘플 + tail-follow" (알고리즘 §25.14 미결) | uPlot 내장 다운샘플 0. min/max는 step-index 고정 bucket→증분 O(Δ)·peak보존 | **min/max decimation 확정** (정적 zoom은 LTTB 보조, 위치=runner SSE 직전) | §25.8 line 22를 확정값으로 / §25.14 "LTTB vs stride vs viewport" 미결 → 해소(bucket 크기 B만 측정) |

---

## 정제 차단 3건 — 한 단락 근거

- **A1 (ACP→유지)**: §24.4 OD-lift는 *확정에 그치지 않고 studio-c1에 ~2232 LOC 구현·커밋*됨 → ACP 전환은 정제가 아니라 재작성. 게다가 worklog 제약("PATH의 claude/codex CLI 재사용·`--permission-mode`·JSONL 직독 연속성 §24.10")에 OD가 더 정확히 맞는다 — claude-agent-acp는 claude code *CLI*가 아니라 *Agent SDK*를 감싸 §24.2·§24.10과 구조적 균열. ACP가 §24.19 원격(Topology B)을 더 깔끔히 풀지도 않음(ws 전송은 ACP도 비표준). ACP의 유일 순익은 "어댑터 유지비 이전" → future 트리거로 등재. (codex-acp `CODEX_PATH`는 CLI 래퍼라 codex 쪽 전환 장벽이 claude보다 낮음 — 메모.)
- **A2 (Sandpack→유지)**: §24.5 srcdoc+self-host React는 self-host 드리프트를 *새 인프라 0*(babel·react inline)으로 푼다. Sandpack self-host는 unpkg 한 줄을 *stale한 별 origin 번들러(`sandpack-bundler` ⭐89·19개월) 운영·fork 유지*로 바꿔 드리프트를 *키운다*. renderify는 JSPM CDN 본드라 spec이 피하려는 CDN 의존을 계승. 산출물 1차 대상이 §24.16 "단일 자기완결 HTML 1장"이라 multi-file 번들러는 과함. renderify의 progressive preview·es-module-lexer만 *multi-file escape hatch* 참고 패턴으로.
- **A3+B2 (odiff→getBoundingClientRect 유지 + axe-core 추가)**: ★1차 briefing의 odiff 픽을 *생성 UI 케이스에서 뒤집음*. odiff는 두 장(base+cur) 필수=baseline 전제인데 **생성물은 매번 합법적으로 달라 안정 baseline이 없다**. exit `21`은 의미상 레이아웃 붕괴가 아니라 *이미지 차원 불일치*라 §24.12가 잡으려는 overflow/overlap을 못 잡음. → spec의 getBoundingClientRect 직접측정이 baseline-free 결정론으로 우월. 보완책 = **baseline-free 사다리**(console 에러 0 → getBoundingClientRect 절대규칙[overflow·overlap·0-size·off-screen] → 깨진 이미지[`naturalWidth=0`] → **axe-core 객관 WCAG** → OCD boolean parity → 사람 6축). odiff/toHaveScreenshot/reg-suit는 "사람이 승인한 고정 reference PNG가 디스크에 있을 때만" 회귀 보조로 격하.

## 진짜 추가 — B1 (E4 다운샘플)

uPlot은 내장 다운샘플이 없다(README: *"aggregation … do it in advance"*). spec §25.8은 "다운샘플"만 확정하고 알고리즘은 §25.14 미결이었다. → **min/max decimation 1픽**: bucket 경계가 step-index 고정이라 append 시 *마지막 bucket만 재계산* → tail-follow의 O(Δ) 증분 충족(LTTB look-ahead는 순수 증분 불가). peak 2점 보존이라 loss spike·best 마커가 안 잘리고 uPlot의 "min/max-per-N" 발상과 정합. 위치=runner SSE 직전(파일 SoT·DB 적재 X·대역폭 §25.8 합치). 정밀 zoom 정적뷰만 LTTB 보조(`janjakubnanista/downsample` MIT). reservoir(peak 탈락)·M4(SQL 집계용)는 탈락.

---

## 인용 정직성·정정 (필수 — 신뢰)

- ⚠️ **Macaron-A2UI (arXiv 2605.24830)**: 논문은 *실재*하고 generative UI 주제도 맞으나, A3+B2 초안이 인용한 **"4단계 결정론 baseline-free lint + 재시도3 → 91.3%→99.2% renderable, fully deterministic and baseline-free" 수치·주장은 abstract에서 확인되지 않음**(abstract는 A2UI-Bench 75.6점 벤치마크 프레이밍·754B 모델). 전문 본문에 있을 가능성은 있으나 *확인 불가* → **본 권고의 근거에서 강등**. baseline-free 결론은 이 논문 없이도 자립한다(getBoundingClientRect는 구조상 baseline-free·QA Wolf "stable structure + DOM metrics, not screenshot diff"·OCD parity 결정론층 코드 확인).
- ✅ **TopoPilot (arXiv 2603.25063)**: 실재·내용 일치(verifier가 structural/semantic pass/fail) — 보조 인용으로 유효.
- ✅ **MinMaxLTTB (arXiv 2305.00332)**: 실재 2023 논문(min-max 선별 후 LTTB) — B1 보조 인용 유효.
- **odiff exit-code(0/21/22)**: README 본문에 코드표 미게재 → 외부 2출처 합치로만 확인(단정 X).
- **1차 `00_briefing.md` 정정**: 축4(b) "odiff 1픽"은 *생성 UI 검증 케이스에선 본 addendum이 supersede* — getBoundingClientRect baseline-free 사다리가 1차, odiff는 고정 reference 회귀 한정. (00_briefing 상단에 포인터 배너 추가함.)

---

## 순(純) spec 변경 목록 (사용자 승인 시 autopilot-spec update로 — 전부 additive·기존 결정 무번복)

1. §24.4: 주석 1줄(ACP 평가 결과) + §24.19에 "ACP swappable 백엔드 (future, 트리거 명시)" 미결 1항.
2. §24.5: drift 기록 1줄(Sandpack/renderify 비채택 사유) + §24.19 옆 multi-file escape hatch 트리거 1줄.
3. §24.12: baseline-free 게이트 사다리 순서 명문화 + axe-core 객관 WCAG 편입 + odiff "고정 reference 시만 보조" 격하.
4. §25.8/§25.14: 다운샘플 = min/max decimation(+LTTB zoom 보조·위치 runner SSE 직전) 확정, §25.14 해당 미결 해소.

> 모두 §1~§23 무접촉·기존 §24/§25 결정 무번복·additive. feat-studio-c1 구현 방해 0(오히려 C1의 OD-lift·srcdoc 선택을 외부 검증으로 뒷받침).
