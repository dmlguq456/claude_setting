# Round 1 — Research Survey Quality Review

> 검토자: 품질관리팀 (plan-review 모드 — survey 산출물 construction quality 적용)
> 대상: `research/agent-engineering-principles/` (00~07 8개 + analysis_summary.md, 61 cards)
> 다운스트림: `autopilot-draft --mode doc` — 사용자 매뉴얼 1부 '원칙의 세대사'
> 축: coverage / no-fabrication(spot check) / progressive disclosure / actionable roadmap / cross-reference 유효성
> 날짜: 2026-06-11

---

## 종합 verdict

**🟡 권고만 — 블로킹 없음.** 요구 범위(세대 4단 + 패턴 11종 + 카드 인용 구조)를 빠짐없이 망라했고, spot-check 한 정량 수치는 전부 카드에 verbatim 으로 존재하며, chapter 간 inline 링크 8/8 유효, 다운스트림이 바로 쓸 outline·citation map·Next Pipeline 이 갖춰져 있다. 아래는 매뉴얼 작성 품질을 한 단계 더 끌어올리는 보완 권고다.

---

## 🔴 실행 전 반드시 수정할 문제

**발견된 문제 없음 ✅**

(coverage 누락·fabrication·깨진 링크·roadmap 공백 등 블로킹 사유 없음. 근거는 아래 검증 로그 참조.)

---

## 🟡 보완하면 좋은 점

### 1. 패턴 번호 체계가 챕터마다 미세하게 다르다 — 매뉴얼이 P-번호로 인용하면 혼동
- **현황**: `04_technical_deep_dive.md`·`06_implementation.md` 는 P1~P11(11종 평면 번호). `analysis_summary.md §1②` 헤더는 "실무 패턴 축 (10개 + 보조 1)"로 컨텍스트 절약을 _보조 P11_ 로 분리 표기한다. `01_landscape.md` lineage diagram 은 번호 없이 이름으로만 노드를 둔다.
- **왜 문제**: 다운스트림 06 citation map 이 "1.4 P1 plan ~ P11 컨텍스트" 로 P-번호를 카드 매핑 키로 쓰는데, analysis_summary 를 같이 참조하면 "P11=보조"인지 "11번째 정규 패턴"인지 한 번 더 판단해야 한다. 매뉴얼 카탈로그를 GoF 식 named pattern 으로 쓸 거라(06 §1.4) 번호보다 이름이 안전하다.
- **제안**: 매뉴얼 draft 단계에서 패턴을 P-번호 대신 _이름_ 으로 인용하도록 06 §1.4 에 한 줄 명시하거나, analysis_summary 헤더를 "11종(컨텍스트 절약 포함)"으로 정렬. 확신 낮음 — 의도적으로 P11 을 보조로 강등한 것일 수 있으니(절약은 cross-cutting 성격) 확인만.

### 2. fact-check 위임 수치의 "검증 대상" 표식이 06 figure 캡션엔 안 붙어 있다
- **현황**: 00·04 는 Harness-Bench 수치(76.2/52.4/23.8)·context collapse(18,282→122)를 "tier 4, fact-check 단계에서 arXiv 원문 대조" 로 명확히 깃발 꽂았다. 그런데 06 §3 figure 후보 표의 캡션 초안("18,282→122 tokens", "84%/93%/17%FN")은 그 caveat 없이 단정형 문장으로 들어가 있다.
- **왜 문제**: figure 캡션은 draft 에 거의 그대로 복붙되는 자산이라, 캡션만 보고 옮기면 tier-4 단독 인용 금지 원칙이 그 자리에서 새어나갈 수 있다. (사용자 feedback: "진단 리포트 과대추정 경향 — 수치 그대로 약속 X" 와 같은 결.)
- **제안**: 06 §3 캡션 초안에 출처 tier + "fact-check 대조 대상" 을 괄호로 병기(예: "…18,282→122 tokens (ACE Fig 2, tier 4 — fact-check 대조)"). 한 줄 추가면 충분.

### 3. P10(headless/cron)·P7 자동화의 근거 얇음이 챕터엔 잘 깔렸으나 06 timeline 🟢 한 줄로만 압축됨
- **현황**: 04 미해결 과제 1·3, 05 §2 Gap 알림이 "tier 3 의존·자동 승격은 tier 4 only" caveat 를 충실히 명시. 06 §5 writing-timeline 은 이를 "🟢 caveat-heavy 패턴 P7·P9·P10 — 미해결 과제 절에 둔다" 한 줄로만 받는다.
- **왜 문제**: 다운스트림이 06 만 보고 쓰기 시작하면(roadmap 챕터의 본분), 이 패턴들을 어디까지 단정해도 되는지의 _경계선_ 을 04 로 되돌아가 다시 읽어야 한다. roadmap 의 self-containment 가 살짝 빈다.
- **제안**: 06 §2 argument scaffolding 표에 P7-자동화·P10 행을 추가하고 "단정 가능 범위: 원칙 O / 자동 메커니즘은 tier 4 backing 명시" 를 reuse. (지금 표엔 7개 주장만 있고 이 둘이 빠져 있음.)

### 4. spec-kit star 편차 caveat 가 07 엔 있으나 03 표엔 "~100k+" 단정으로 노출
- **현황**: 07 star caveat 가 "spec-kit 직접 fetch 111k vs 2차 71~90k, '~100k+ 급성장'으로 인용" 을 정확히 잡았다. 03 Harness 표·07 Tier1 표는 "~100k+ (편차 큼)" 로 편차를 병기해 일관적이다. (이건 잘 처리된 편 — 권고는 약함.)
- **제안**: 없음에 가까움. 매뉴얼이 star 수를 인용하면 무조건 "급성장 중 대략치" 를 동반하라는 07 caveat 를 draft 가 따르는지만 확인.

---

## 🟢 잘 작성된 부분

- **Coverage 완전**: 요구한 세대 4단(prompt→context→harness→loop)은 01 에서 각각 (verbatim 정의 / 명명·정초·대중화 권위 분리 / 직전 세대 한계 = 등장 동력 / 대표 소스)의 4요소로 빠짐없이 정리됐고, 실무 패턴 11종(plan-then-execute·spec-driven·maker-verifier·서브에이전트 분업·파이프라인 세분화·golden set·오답노트→승격·상태 영속성·worktree·headless/cron·컨텍스트 절약)이 04 에서 _문제→원칙(verbatim)→메커니즘→정량→반론→인용 포인트_ 6요소 동형으로 전부 다뤄졌다. 요구 범위 누락 0.
- **No-fabrication 규율 모범**: spot-check 5건(context collapse 18,282→122 / Harness swap 23.8pt·76.2·52.4 / multi-agent 90.2% / sandboxing 84% / code-exec 98.7%)이 전부 인용 카드에 verbatim 으로 존재. tier 4 수치엔 일관되게 "블로그 1차 backing 전용·단독 금지·fact-check 대조" 깃발이 붙어 있고, 명명 권위(Greyling=정리자, Harness-Bench=논문 귀속)와 정리 역할을 인용 단계에서 분리하라는 지침이 00·01·02 에 반복 강조된다. 근거 없는 숫자 0.
- **Progressive disclosure 충실**: 00 briefing 이 1줄요약 → 핵심발견 3~5줄 → 1-page 개요 → Mermaid 세대지도 → top-3 actionable → 전체 가이드 표의 계층 구조를 갖춰, "한 장으로?"부터 "어떻게 시작?"까지 깊이별 진입점이 명확하다. 누락 디렉터리(analysis_project 부재)도 정직하게 알림.
- **Roadmap 즉시 사용 가능**: 06 이 section-by-section outline(1.0~1.5) + argument scaffolding(주장↔지지카드↔반론) + 절별 citation map(1.4 P1~P11 카드 매핑) + figure 후보 + Next Pipeline verbatim 명령까지 갖춰, draft 가 빈 페이지에서 시작하지 않는다. 사용자 강조 항목(산출물 소통)을 draft_directives §2 에서 _정식 패턴 등재_ 로 격상하되 §6 망라 원칙으로 "예시일 뿐 전부 아님" 균형까지 명시한 게 특히 좋다.
- **Cross-reference 무결**: chapter 간 inline `.md` 링크 8개 파일 전부 유효 타깃, 06 이 참조하는 figure 3종(arxiv-agentic-context-engineering_fig2 / inside-the-scaffold_fig1 / code-as-agent-harness_fig1) 실재, analysis_summary §4 timeline 앵커 실재, draft_directives §2/§6/§7 앵커 실재. 깨진 참조 0.
- **반론·tension 균형**: 04 Tensions 4종(서브에이전트 read/write 축·GAN 비유 한계·harness 가치 감쇠론·context file 과다 역효과)이 대립을 시점/작업유형으로 종합하고, 01 adoption stage 표가 mainstream/emerging/contested 를 구분해 "어디까지 단정 가능한가"를 매뉴얼에 미리 깔아준다.

---

## 검증 로그 (이 verdict 의 근거)

- 8개 chapter + analysis_summary 전문 Read, 61 cards 디렉터리 확인 (인용 slug 들이 실파일과 매칭).
- 정량 spot-check 5건 → 전부 카드 verbatim 일치 (grep 대조): 18,282→122 / 23.8·76.2·52.4 / 90.2% / 84% / 98.7%·150,000→2,000.
- inline `.md` 링크 8/8 OK, 06 참조 figure 3/3 실재, analysis_summary §4·draft_directives §2/§6/§7 앵커 실재.
- 403-block 출처(codewithseb-headless-cicd)의 tier-3 caveat 가 카드→04→05 로 손실 없이 전파됨 확인.
- **개별 citation(venue/year/metric) 검증은 fact-checker 역할이라 본 리뷰 범위 외** — 위는 fabrication spot-check 수준.
