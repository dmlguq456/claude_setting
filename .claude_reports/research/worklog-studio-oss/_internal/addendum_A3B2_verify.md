# Addendum A3+B2 — §24.12 디자인 검증 재조준: 결정론 게이트 + baseline 없는 생성물 난제

> **조사일** 2026-06-23 · **모드** technology(OSS·기법) · **QA** thorough(메타데이터 gh api 실측 + arxiv/문서 교차) · **렌즈** local-first·BYOK·디스크=상태·design-mcp(Playwright preview/screenshot/eval_js/getConsoleLogs) 재사용·MIT/Apache·**결정론(boolean) 게이트, LLM-judge/임의 점수 회피**
> **선행조사 기준선**: `00_briefing.md`/`axis4_manifest_design.md` 가 **odiff exit-code(0/21/22)** 를 verifier 게이트 후보로 제시함 → 본 addendum 이 그 후보를 §24.12 의 `getBoundingClientRect` 직접측정과 대질·재평가.
> **§24.12 위치 확인**: 본 문서가 검증하는 §24.12 = worklog-studio 디자인 검증 spec (forked verifier·OCD boolean parity rubric·게이트·픽셀 직접측정·폴백 사다리). OCD parity 구현 출처 = `analysis_project/doc/design-studio/ocd-verification-lift.md`(opencoworkai/open-codesign `verify-ui-kit-parity.ts`/`verify-ui-kit-visual-parity.ts`/`BENCHMARKS.md` 인용).

---

## 0. 핵심 결론 (TL;DR)

- **(A3)** odiff 는 §24.12 의 `getBoundingClientRect` 직접측정보다 **나은 게이트가 아니라, 보완도 제한적**이다. 결정적 이유: **odiff 는 두 장(base+cur)을 요구하는 baseline-전제 도구**이고, **생성 디자인엔 안정 baseline 이 없다**(=B2 의 본질). odiff 의 exit `21`("layout diff")은 *의미상 레이아웃 붕괴가 아니라 단순 이미지 차원 불일치*다 — §24.12 가 잡으려는 overflow/overlap 을 직접 잡지 못한다. → **getBoundingClientRect 가 baseline-free 결정론 게이트로 우월. odiff 는 "고정 reference 디자인 PNG 가 디스크에 있을 때만" 보조(승인된 디자인 회귀 감시)로 격하.**
- **(B2)** baseline 없이 "생성물이 깨졌나"의 결정론 게이트 = **절대규칙 lint 다발**: ① getBoundingClientRect 기반 레이아웃 절대규칙(viewport overflow·0-size·overlap·off-screen) ② console/runtime 게이트(에러 0·hydration·`naturalWidth=0` 깨진 이미지·빈 렌더) ③ axe-core 객관 규칙(WCAG color-contrast 등 baseline-free) ④ OCD식 boolean parity rubric(pass/total, 누락=fail) ⑤ (옵션) self-consistency diff(같은 프롬프트 N회 상호 odiff = 안정성 측정, 단일 baseline 불요). 이 전부 *고정 golden 불필요·결정론*. **toHaveScreenshot/reg-suit/odiff(단일 baseline)은 생성물에 부적합** — 매 생성이 합법적으로 달라 baseline 자체가 정의 불가.
- **외부 검증(강한 신호)**: Macaron-A2UI(arXiv 2605.24830) 가 정확히 이 설계를 입증 — **4단계 결정론·baseline-free lint(format→structure→data-binding→semantic) + 에러피드백 재시도 3회**로 first-attempt 91.3% → 최종 99.2% renderable. "fully deterministic and baseline-free—no reference images required" 명시. = §24.12 의 lint-우선 결정론 루프와 동형이고 *수치 증거*까지 있음.

---

## (A3) odiff vs getBoundingClientRect 비교표

| 항목 | **odiff** (`dmtrKovalenko/odiff`) | **getBoundingClientRect** (eval_js, §24.12) |
|---|---|---|
| baseline 필요? | **예 — 두 장(base+cur) 필수**. base 없으면 동작 불가 | **아니오 — 단일 렌더에서 절대판정** (요소가 viewport 밖/0-size/겹침) |
| 무엇을 판정? | 두 이미지 *픽셀·차원 diff* | 요소의 *절대 기하*(rect.x/y/w/h, viewport 경계 대비) |
| exit/출력 | `0`=match·`21`=layout diff(=**차원 불일치일 뿐**)·`22`=pixel diff (실측 확인) | rect 수치 → JS 로 boolean 규칙 평가(overflow/overlap/off-screen) |
| "레이아웃 깨짐" 직접 잡나? | **아니오** — `21` 은 "이미지 크기 다름", overflow/overlap 의미 아님 | **예** — overflow/overlap/off-screen 을 *절대값*으로 직접 측정 |
| 결정론? | 예(픽셀 결정론) | 예(브라우저 layout engine 실측, jsdom 아닌 real engine) |
| 생성물 적합? | **부적합**(baseline 없음) — 고정 reference 있을 때만 | **적합** — 생성물에 baseline 0 으로 작동 |
| 이미 의존? | 아니오(신규 단일 바이너리, MIT, ⭐3,068) | **예** — design-mcp eval_js 가 이미 Playwright real-browser |
| 비용/무게 | 단일 SIMD 바이너리, ~0 / 단 base PNG 디스크 보관 필요 | 0(이미 있음) |

> **판정**: §24.12 의 getBoundingClientRect 직접측정이 *생성물 게이트로서 odiff 보다 구조적으로 우월* — baseline-free 이고, odiff 의 `21` 이 못 잡는 "의미상 레이아웃 깨짐"을 절대값으로 직접 잡는다. odiff 의 진짜 쓰임새는 *생성물 검증이 아니라* "사람이 승인한 고정 디자인이 디스크에 있고, 이후 코드 변경이 그 픽셀을 회귀시켰나"의 **회귀 감시**다 — §24.12 의 baseline-free 게이트와는 다른 문제. (메타 실측: odiff MIT·archived=false·pushed 2026-06-11·Zig.)

---

## (B2) baseline-free 결정론 검증 기법 표 (생성/변동 UI 대상)

| 기법 | OSS / API | baseline 필요? | 생성물 적합 | 결정론 | 무엇을 잡나 |
|---|---|---|---|---|---|
| **레이아웃 절대규칙 lint** (overflow·0-size·overlap·off-screen) | getBoundingClientRect (design-mcp eval_js, 이미 의존) + Playwright `expect().toBeInViewport()`(v1.31+, Apache-2.0 ⭐91k) | **아니오** | ◎ | ◎ | 요소 화면밖/겹침/0크기 — 절대 깨짐 |
| **console/runtime 게이트** | design-mcp `getConsoleLogs`(이미 의존) — 콘솔 에러 0·hydration 에러·`did-fail-load` | **아니오** | ◎ | ◎ | 런타임 깨짐·로드 실패 |
| **깨진 이미지/빈 렌더** | eval_js: `img.naturalWidth===0`·root subtree 비어있음·면적 0 | **아니오** | ◎ | ◎ | 미로드 자산·빈 화면 |
| **접근성 객관규칙** | **axe-core**(`dequelabs/axe-core`, MPL-2.0 ⭐7,257, pushed 2026-06-18) — WCAG color-contrast 등 CSS 계산 객관 항목 | **아니오** | ◎ | ◎ | contrast·ARIA·label 등 *객관* WCAG(주관 항목 제외) |
| **OCD boolean parity rubric** | open-codesign `verify-ui-kit-parity.ts`(결정론, LLM無: 요소수·텍스트커버·토큰커버 가중합)+`verify-ui-kit-visual-parity.ts`(12 boolean, `parityScore=pass/total`, 누락=fail) | **아니오**(결정론층) / vision층은 *목표 mockup* 1장(=고정 reference, baseline 아님) | ◎ | ◎(점수 derive, 모델 점수 안 냄) | 고정 체크리스트 충족 여부 |
| **self-consistency diff** | 같은 프롬프트 N회 생성 → 상호 odiff/구조 diff(*고정 baseline 대신 자기일관성*) | **아니오**(N개 상호) | ○(안정성 측정용, 깨짐판정 아님) | ◎ | 생성 *불안정성*(같은 입력 큰 변동) |
| **DOM 구조/semantic 게이트** | Macaron-A2UI식 4단계(format→structure→data-binding→semantic) — 필수 필드·타입·enum·바인딩·의도 정합 | **아니오** | ◎ | ◎ | 구조 무결·렌더가능성 |
| ~~toHaveScreenshot~~ | Playwright `toHaveScreenshot` / **reg-suit**(MIT ⭐1,277) | **예(고정 baseline)** | **✗** | ◎ | *생성물엔 부적합* — baseline 정의 불가 |
| ~~odiff 단일 baseline~~ | odiff(MIT ⭐3,068) | **예** | **✗(생성물)** / ○(고정 reference 회귀) | ◎ | 픽셀·차원 diff(고정 reference 있을 때만) |

> **핵심**: 상단 7기법은 모두 *고정 golden 없이* 작동 = "생성물이 절대적으로 깨졌나"를 결정론 boolean 으로 답함. 픽셀-diff류(odiff/toHaveScreenshot/reg-suit)는 *fixed baseline 전제*라 매번 합법적으로 바뀌는 생성 UI 에 부적합(QA Wolf: "assert on stable structure … validate DOM/canvas metrics via getBoundingClientRect rather than visually comparing screenshots").

---

## (B2 보강) 에이전트 루프 결합 선례 (maker→render→verifier 에 boolean 게이트)

- **Macaron-A2UI** (arXiv 2605.24830): 4단계 결정론 lint + **에러피드백 재시도 3회** → 91.3%→99.2%. "fully deterministic and baseline-free". = §24.12 lint-우선 루프의 *수치 증거 있는 동형*.
- **OCD verify-and-iterate** (`BENCHMARKS.md`): boolean rubric→status enum→FAIL 시 `reason` 텍스트로 re-decompose, max 2 rounds. §24.12 의 "PASS 침묵·FAIL 텍스트·라운드 상한"과 1:1.
- **TopoPilot** (arXiv 2603.25063): verifier 가 *boolean-constrained tool* 로만 답해 downstream 결정론 보장 — §24.12 의 "모델은 점수 못 냄, 스크립트가 derive" 규율과 동형.

---

## ★ §24.12 spec 반영 권고 (갈아엎지 말고 *명문화·재배치*)

§24.12 는 이미 올바른 방향(getBoundingClientRect 직접측정 + boolean parity + console/구조 게이트 + 폴백 사다리). 본 조사가 더하는 것은 **odiff 의 자리를 정확히 못 박고, baseline-free 게이트를 *1차*로 승격**하는 명문화다.

1. **"생성물 결정론 게이트 = baseline-free 규칙 lint 가 1차"를 §24.12 에 명시.** 순서:
   `getConsoleLogs(에러 0)` → `eval_js 레이아웃 절대규칙(getBoundingClientRect: viewport overflow·overlap·0-size·off-screen)` → `깨진 이미지/빈 렌더(naturalWidth=0)` → `axe-core 객관 WCAG(color-contrast)` → `OCD boolean parity rubric(pass/total, 누락=fail, HONEST_SCORES)` → (사람) 6축 미감. 이 사다리 전부 *고정 baseline 0*.
2. **odiff 는 1차 게이트에서 제외, "고정 reference 디자인 PNG 가 디스크에 존재할 때만" 보조 회귀 감시로 한정.** 근거: odiff exit `21` 은 차원불일치이지 overflow/overlap 아님 + base 필수 → 생성물 게이트 부적격. (디스크=상태 렌즈: reference PNG 둘 거면 `spec/design/_baseline/<slug>.png` 같은 명시 위치. 없으면 odiff 단계 skip — 게이트 안 깨짐.)
3. **toHaveScreenshot/reg-suit 를 "생성물엔 미채택" 으로 명시.** baseline 전제라 변동 생성물에 구조적 부적합(자기일관성 측정엔 self-consistency diff 별도).
4. **axe-core 를 게이트에 신규 편입(주관항목 제외).** color-contrast 등 *객관* WCAG 는 baseline-free 결정론 — design-mcp Playwright 페이지에 `@axe-core/playwright` 주입이면 추가 무게 작음(MPL-2.0 — 라이선스 렌즈 OK, 파일단위 copyleft).
5. **(옵션) self-consistency 게이트 추가 고려.** 같은 프롬프트 N회 생성 후 상호 구조 diff 로 *생성 안정성*을 boolean 화(임계 초과 변동=경고). baseline 없이 "이 프롬프트가 신뢰 가능한 생성을 내나"를 잰다 — 깨짐판정과 별개 축.

> **한 줄 결론**: 생성물의 결정론 게이트는 **baseline-free 규칙 lint(getBoundingClientRect + console + 구조/깨진이미지 + axe-core 객관 + OCD parity)가 1차**이고, **odiff/픽셀-diff 는 *사람이 승인한 고정 reference 가 디스크에 있을 때만* 보조 회귀 감시**다. §24.12 의 현재 설계는 옳으며, 본 권고는 odiff 의 위치 격하 + baseline-free 1차 사다리 명문화 + axe-core 편입의 *증분 보강*이다.

---

## 출처 (메타 gh api 실측 / 문서 교차)

- odiff `dmtrKovalenko/odiff` MIT · ⭐3,068 · Zig · pushed 2026-06-11 · archived=false (gh api 실측). exit `0/21/22 = match/layout(=차원)/pixel` (WebSearch 다중 출처 일치; README 본문엔 코드표 미게재라 미확인 1단계 — 그러나 선행 axis4 와 외부 2출처 합치).
- axe-core `dequelabs/axe-core` MPL-2.0 · ⭐7,257 · pushed 2026-06-18 (gh api). 객관 WCAG(color-contrast 등) 결정론·CI `--exit` 게이트.
- Playwright `microsoft/playwright` Apache-2.0 · ⭐91,450 (gh api). `toBeInViewport`(v1.31+)·real-browser getBoundingClientRect·toHaveScreenshot(=baseline 전제).
- reg-suit `reg-viz/reg-suit` MIT · ⭐1,277 (gh api) — baseline 전제 비주얼 회귀(생성물 부적합).
- Macaron-A2UI arXiv 2605.24830 — 4단계 결정론 baseline-free lint + 재시도3 → 91.3%/99.2% (WebFetch 본문 확인).
- OCD parity 구현 — `analysis_project/doc/design-studio/ocd-verification-lift.md`(open-codesign `verify-ui-kit-parity.ts`/`verify-ui-kit-visual-parity.ts`/`BENCHMARKS.md` 인용; 결정론층이 *baseline-free*임을 코드로 확인).
- QA Wolf "Testing Generative AI Applications" — generative UI 는 "stable structure assert + getBoundingClientRect DOM metrics, not screenshot diff" (WebSearch).
