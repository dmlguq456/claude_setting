# 데이터·결과 분석 방법론 (Ui-Hyeop Shin)

> 사용자의 실험 데이터·결과 분석 접근법·검증 패턴. 분석팀 / 연구팀 / 기획팀 참조.

## 분석 접근

- _signal fidelity + perceptual quality 두 축 분리_ — universal restoration 자리에서 항상 두 그룹.
- _ablation 분리_ — 한 변경 = 한 row, 누적 비교 형태.

## 검증 패턴

- 본문 수치는 실험 log / json summary 에서 직접 추출 (fabrication 금지).
- rebuttal 표·통계는 _원본 script_ 로 재현 가능해야 함 (예 `heteroscedasticity_analysis.py`).

## 통계 처리

- Spearman ρ — utterance 단위·frequency 단위 둘 다 계산.
- CV (coefficient of variation) — raw vs normalized 두 비교.
- p-value 작으면 (`p ≈ 0`) 명시.

## TODO (analyze-user 로 보강 예정)

- 자주 쓰는 데이터 source 경로
- 분석 script 의 공통 구조
- 결과 검증 체크리스트


## 사용자 수동 메모

> 본 절은 _사용자 영역_. `/notes --scope user <aspect>` 가 append. analyze-user 는 _읽기만_ 하고 손대지 않음.

_(아직 비어 있음 — `/notes --scope user analysis add ...` 로 첫 항목 추가)_
