# QA fact-check — round 2 (addendum 인용 검증)

조사일 2026-06-23. addendum(A1/A2/A3B2/B1)의 post-cutoff arXiv 인용 + 핵심 메타데이터 재검증.

## arXiv 인용 (오케스트레이터 WebFetch 직접 검증)
| 인용 | addendum 주장 | WebFetch 검증 결과 | 판정 |
|---|---|---|---|
| Macaron-A2UI `2605.24830` | "4단계 결정론 baseline-free lint + 재시도3 → 91.3%→99.2% renderable, fully deterministic baseline-free" | 논문 실재(title 일치, generative UI 주제 O). **그러나 abstract는 A2UI-Bench 75.6점·754B 모델 프레이밍 — 91.3%/99.2%·baseline-free 주장 미확인** | 🟡 **부분 — 논문 실재·수치 강등**(본문 가능성 있으나 확인 불가, 근거에서 제외) |
| TopoPilot `2603.25063` | verifier가 structural/semantic pass/fail | 실재·일치(reliability-centered two-agent, verifier 검증) | ✅ |
| MinMaxLTTB `2305.00332` | min-max 선별 후 LTTB | 실재 2023 논문(알려진 선행연구) | ✅ |

## 기타
- odiff exit `0/21/22`: odiff README 본문에 코드표 미게재 → 외부 2출처 합치로만 확인(addendum이 정직 표기). **단정 회피** 유지.
- A1 "studio-c1 `34852d4` ~2232 LOC 구현" : worktree `git worktree list`로 브랜치 존재 실측 확인됨(커밋 해시·LOC는 에이전트 보고, 본 종합에서 브랜치 존재만 교차확인).

## 조치
- addendum_spec_deltas.md "인용 정직성·정정" 섹션에 Macaron-A2UI 강등 명문화.
- baseline-free 권고는 Macaron 인용 없이 자립(getBoundingClientRect 구조적 baseline-free + QA Wolf 출처 + OCD parity 코드)임을 명시.

**Verdict**: 🟢 자립 근거 유지. 🟡 1건(Macaron 수치) 강등·투명 기록. 날조성 인용(존재하지 않는 논문) 0.
