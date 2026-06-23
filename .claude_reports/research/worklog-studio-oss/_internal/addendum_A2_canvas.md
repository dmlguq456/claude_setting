# Addendum A2 — §24.5 캔버스: Sandpack(self-host) vs srcdoc + self-hosted React

> 정조준 질문: spec §24.5 는 라이브 프리뷰를 **srcdoc + self-host React**(OD `srcdoc.ts buildSrcdoc` + `injectSandboxShim` lift, `sandbox="allow-scripts"` no-same-origin + CSP, 디바운스 ~100ms, JSX 는 iframe 안 Babel transform — unpkg CDN→self-host 드리프트 반영)로 _이미 확정_. (1) Sandpack self-host bundler 가 그 드리프트를 더 표준으로 푸나? (2) 생성물이 단일 HTML/JSX 1장이면 srcdoc 로 충분한가, multi-file/의존성이 흔해 번들러가 필요한가? (3) renderify(babel-standalone) 가 둘 사이 경량 중간해인가?
>
> 메타데이터는 GitHub API / npm registry 실측 (2026-06-23 조회). 미확인은 "(미확인)".
>
> **★ 결정적 선행 사실 (조사 중 확인)**: ① spec §24.5 는 OD `srcdoc.ts`/`react-component.ts` lift 를 _이미 확정_, 빌드 마일스톤 `C2(M1)` 에 "React self-host 전환"이 명문화돼 있고 라이선스 고지 대상 파일(`web/runtime/srcdoc.ts`·`react-component.ts`)까지 §24.16 에 박혀 있음 — A1(브리지)처럼 코드 커밋까지는 (미확인)이나 spec 결정은 srcdoc 쪽으로 _잠김_. ② **Sandpack self-host 경로의 핵심 레포 `codesandbox/sandpack-bundler` 는 ⭐89 · push 2024-11-19 (조사일 기준 ~19개월 정체) · Apache-2.0** — 메인 `codesandbox/sandpack`(⭐6,168) 도 push 2025-04-24 로 ~14개월 정체. self-host 골격이 _둘 다 stale_. ③ renderify 의 의존성 resolve 는 **JSPM CDN 본드**("retry + timeout + multi-CDN fallback for remote module fetches", `RENDERIFY_RUNTIME_JSPM_ONLY_STRICT_MODE` 도 manifest pinning 일 뿐 _오프라인 import-map 자체호스팅은 미제공_) — spec 이 피하려는 "CDN 드리프트"를 _그대로 안고 옴_.

---

## 1. 세 방식 실측 메타데이터 (2026-06-23)

| 방식 | 핵심 레포/패키지 | ⭐stars | license | 최근 push | npm unpacked | 성숙도·정체 |
|---|---|---|---|---|---|---|
| **srcdoc + self-host React (§24.5 = 확정)** | OD `nexu-io/open-design` (lift 원본) + 자체호스트 `@babel/standalone` + `react`/`react-dom` | OD 69,580 | Apache-2.0(OD)·MIT(babel/react) | OD 2026-06-23(활발) | babel-standalone ~31MB / react+dom ~7MB (unpacked; 실배포는 prod build min+gzip 으로 babel ≈ 수백KB·react+dom ≈ ~45KB gz) | OD 활발 유지. self-host 부품(babel·react)은 _업계 표준·영구 유지_. **lift 코드만 내 책임** |
| **Sandpack self-host** | `@codesandbox/sandpack-client`(client) + `codesandbox/sandpack-bundler`(self-host 번들러) | sandpack 6,168 / bundler **89** | Apache-2.0 | sandpack **2025-04-24** / bundler **2024-11-19** | sandpack-client ~64MB / sandpack-react ~1.2MB (unpacked) | **둘 다 정체** — 특히 self-host 번들러(⭐89)는 ~19개월 무push. 내가 fork·유지 떠안을 위험 |
| **renderify (babel-standalone 중간해)** | `webllm/renderify` | 23 | MIT | 2026-06-17(활발) | (npm 미배포 추정·미확인) | 신생 ⭐23·1인 추정. 활발하나 프로덕션 검증 (미확인). **JSPM CDN 의존 = local-first 와 균열** |

**한 줄 요약**: self-host 의 "표준·영구 유지" 부품은 오히려 **§24.5 가 이미 고른 babel+react** 쪽이다. Sandpack 의 self-host 골격(bundler)은 stale(⭐89·19개월)이고, renderify 는 CDN 본드라 local-first 에서 가장 약하다.

---

## 2. 비교표 — [self-host 난이도·트랜스파일·multi-file·부분렌더·격리·번들무게·성숙도]

| 축 | **srcdoc + self-host React (§24.5)** | **Sandpack self-host** | **renderify(babel-standalone)** |
|---|---|---|---|
| **self-host 난이도** | **낮음** — react·react-dom·babel-standalone 정적 자산을 srcdoc `<script>` 본문/blob 로 inline. 별 서버·별 origin 빌드 0. (iframe 은 no-same-origin 이라 외부 asset URL 불가 → inline 강제, 단일 자기완결 HTML 과 동형 §24.16) | **높음** — `sandpack-bundler` 를 `yarn build` 후 **별도 origin 서버**(`server.js`·`_headers`)에 호스팅, `bundlerURL` 로 지정. 그 번들러 레포가 stale(⭐89) → 내가 fork·유지. 별 origin 운영 부담 | **중** — zero-server 지만 bare import 를 **JSPM CDN** 으로 resolve. 오프라인/BYOK 면 JSPM 미러를 _내가_ 깔아야 함(react+babel inline 보다 무거움). spec 드리프트를 _옮길 뿐_ 안 풂 |
| **트랜스파일** | iframe 안 `@babel/standalone` transform 후 eval (OD `react-component.ts:9` `buildReactComponentSrcdoc` lift) | 별 origin 번들러가 처리(브라우저 내 번들, 서버 불필요) | iframe/worker 안 `@babel/standalone` + `es-module-lexer` import 추출 |
| **multi-file/의존성** | **약함** — srcdoc 1장 = 단일 모듈. multi-file·npm 의존은 import map(blob)으로 _수동_ 배선해야 하고 transitive resolve 없음 | **강함** — multi-file 번들·의존성 resolve·HMR 라이브러리 기본 제공(이 방식의 유일 강점) | **중** — JSPM 으로 transitive bare import resolve(react bridge·recharts 보장, 그 외 best-effort). 단 CDN 본드 |
| **부분 렌더(생성 중 점진)** | **있음** — §24.5 디바운스 ~100ms srcdoc 교체(`postMessage od:srcdoc-transport-activate`)가 OD 기설계. 스트리밍 델타 배선은 vercel/chatbot `onStreamPart` 흡수 권고(축2 본문) | **약함** — `updateSandbox()` 를 델타마다 호출하면 파일단위 갱신 가능하나 _토큰 스트리밍 API 부재_, onStreamPart 와 별도 조합 필요 | **강함(명시)** — `renderPromptStream` 이 `llm-delta`/`preview`/`final` chunk emit, progressive preview 내장(diff 기반 Preact 재조정) |
| **격리** | `sandbox="allow-scripts"` **no-same-origin** + CSP(§24.5). same-document 격리(별 origin 아님) — XSS 봉인은 no-same-origin + CSP 가 담당 | **별 origin bundler iframe** — origin 분리라 _경계는 한 단 더 강함_. 단 그 별 origin 을 내가 운영·CSP 설계 | worker/iframe/ShadowRealm 3-mode + 정책 체커(blocked tags·allowlist·execution budget) — 유연하나 babel eval 경계는 sandbox 봉인 전제 |
| **번들무게** | **가벼움** — babel(prod ~수백KB gz)+react+dom(~45KB gz) inline. 단순 HTML 1장이면 babel 도 생략 가능 | **무거움** — 별 origin 번들러 런타임(MB급). 단순 HTML 1장엔 명백한 오버킬 | **중** — babel-standalone + es-module-lexer 런타임. CDN fetch 가 첫 렌더 지연 |
| **성숙도** | OD 활발(⭐69.6k)·babel/react 표준. **lift 코드만 내 유지** | sandpack ~14개월·bundler ~19개월 정체. self-host 골격 stale | ⭐23 신생·1인 추정. 프로덕션 검증 (미확인) |

---

## 3. self-host 드리프트(unpkg→self-host)를 각 방식이 어떻게 푸나

- **srcdoc + self-host React (§24.5)** — 드리프트를 **정면으로 푼다(가장 깔끔)**. CDN `<script src>` 를 react/react-dom/babel-standalone _정적 자산 inline_ 으로 바꾸면 끝. iframe no-same-origin 이라 외부 URL 못 쓰는 제약이 오히려 inline 을 강제 → 결과가 §24.16 "단일 자기완결 HTML"과 자연 정합. 새 인프라 0.
- **Sandpack self-host** — 드리프트를 **표준 옵션으로 우회**(`bundlerURL` 지정)하지만 _깔끔하진 않다_. unpkg 한 줄을 "별 origin 번들러 서버 1대 운영 + stale 레포(⭐89·19개월) fork 유지"로 바꾸는 셈 — 드리프트의 _규모를 키운다_. self-host 가 "표준"인 건 맞으나 운영비가 §24.5 inline 보다 훨씬 큼.
- **renderify** — 드리프트를 **안 푼다(오히려 계승)**. bare import 를 JSPM CDN 으로 resolve 하는 게 본질이라, spec 이 escape 하려는 "런타임이 CDN 에 묶임"을 그대로 가져온다. 오프라인 자체호스트 import-map 은 미제공 → 직접 JSPM 미러 구축은 react+babel inline 보다 무거운 일.

---

## 4. ★ spec 반영 권고 — **§24.5 srcdoc + self-host React 유지 (전환 X)**, renderify 는 _패턴 흡수만_

**택1: "§24.5 srcdoc 유지".** 하이브리드(단일=srcdoc·복합=Sandpack)도 고려했으나 _현 시점 비권고_ (아래 근거).

**근거**
1. **Sandpack 전환은 드리프트를 키운다.** spec 의 self-host 동기는 "CDN 한 줄 제거 + local-first". §24.5 inline 은 새 인프라 0 으로 그걸 달성하는데, Sandpack self-host 는 _stale 한 별 origin 번들러 서버(`sandpack-bundler` ⭐89·push 2024-11)_ 운영·fork 유지를 떠안게 한다 — local-first·"디스크=상태"·재사용 렌즈에 역행. self-host 가 "표준"이라는 장점이 운영비·정체 리스크에 압도됨.
2. **lift 가 이미 잠겨 있다.** §24.5 가 OD `srcdoc.ts`/`react-component.ts` lift 를 확정하고, `C2(M1)` 마일스톤·§24.16 라이선스 고지 대상까지 srcdoc 경로로 박혀 있음. A1(브리지)에서 OD `runtimes/` lift 가 이미 코드 커밋된 정황을 보면, 캔버스도 갈아엎기보다 _이미 들인 OD 정합 경로를 완성_ 하는 게 일관됨.
3. **생성물 형태가 srcdoc 에 맞는다.** 디자인 스튜디오 산출물은 §24.16 이 "단일 자기완결 HTML(self-host React/Babel 인라인)"로 명시 — 즉 _단일 HTML/JSX 1장_ 이 1차 대상이고, 이 경우 Sandpack 의 multi-file 번들·HMR 은 과함. multi-file 의존 컴포넌트는 _현 spec 범위 밖_ 이라 번들러 도입 근거가 약함.
4. **renderify 는 CDN 본드라 local-first 에서 탈락(중간해 아님).** progressive preview(`renderPromptStream`)·3-mode sandbox 는 매력적이나, 의존성 resolve 가 JSPM CDN 이라 spec 의 드리프트를 _옮겨올 뿐_. ⭐23 신생 성숙도도 직접 의존 비권고. **패턴만 흡수** — (a) progressive `llm-delta/preview/final` chunk 모델은 §24.5 디바운스 재로드 + vercel/chatbot `onStreamPart` 배선의 _참고 설계_ 로, (b) `es-module-lexer` import 추출은 _장차_ multi-file/npm 의존이 실제 필요해질 때(escape hatch) 자체 import-map(blob) resolve 의 레시피로.

**구체 file/section**
- **유지(변경 없음)**: `spec/prd.md` §24.5 "캔버스 = sandboxed iframe (M1)" — srcdoc + self-host React 경로 그대로. `C2(M1)` 빌드 마일스톤·§24.16 고지 대상 불변.
- **명시 보강(권장, 선택)**: §24.5 JSX 경로 항목 끝에 _"Sandpack self-host 는 검토했으나 별 origin 번들러(`sandpack-bundler` ⭐89·19개월 정체) 운영비가 inline self-host 대비 역행 → 비채택. renderify(babel-standalone)는 JSPM CDN 본드라 local-first 와 균열 → 패턴(progressive preview·es-module-lexer)만 _escape hatch_ 참고"_ 한 줄을 drift 기록처럼 남겨, 후속 세션이 같은 질문을 재발화하지 않게.
- **escape hatch 조건(§24.19 미결 옆에 1줄)**: _"산출물이 multi-file/npm 의존으로 확장되면 — 그때 비로소 (a) 자체 import-map(blob) resolve 또는 (b) Sandpack self-host 재평가. 현 단일 HTML/JSX 범위에선 srcdoc 충분."_ — 하이브리드를 _지금 짓지 말되 트리거를 명문화_.

**한 줄 결론**: §24.5 의 srcdoc + self-host React 는 self-host 드리프트를 _가장 적은 인프라로_ 이미 풀었다. Sandpack 전환은 stale 한 별 origin 번들러 운영비로 드리프트를 키우고, renderify 는 CDN 본드라 local-first 를 깬다 — 둘 다 채택 X, renderify 의 progressive preview·es-module-lexer 만 multi-file escape hatch 의 참고 패턴으로 흡수.
