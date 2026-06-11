---
name: pangyo-lexicon
description: research 보고서 다듬기에서 반복 등장한 판교체·번역체 어휘와 한국어 치환 누적 메모
metadata:
  type: feedback
---

# 판교체 어휘 누적 메모 (research 보고서 polish)

agent-engineering-principles 보고서 세트(00~07) 다듬기에서 반복된 패턴.

## 영어 동사·형용사 박힘 → 한국어 풀이
- `coined` → "용어를 만들었다(coined)" (약어 보존하되 한국어 동사 부여)
- `fragile 해질` → "깨지기 쉬워질(fragile)"
- `thin 해짐` → "옅어진다"
- `regress 한다` 는 도메인 동사라 보존, `~화 한다`(taxonomy화/permanent guards화) → "정리했다 / 굳힌다"
- 명사구 끝 체언종결(`...task 소스로`, `...artifact 로`) → "...task 소스로 삼는다 / artifact 로 제시한다" 동사 보강
- `외재화` → "외부로 빼낸다" (한 문서 내 통일)

## 표기 결정 (이 보고서 세트)
- 도메인 영어 보존: prompt/context/harness/loop engineering, maker-verifier, worktree, headless, golden set, compaction, scaffolding, fragile, pass@k, FN 등 + 카드 [slug] + mermaid + 표 셀 개조식
- "층" 과 누적 "layer" 분리: L1~L4 안전장치는 "층"(한국어), 세대 누적 개념어는 "layer"(도메인 굳은 표현) 보존
- 표 셀·개조식 bullet 의 명사 종결("~함/~임")은 그대로, 산문 문장만 "~다" 능동·자연 어순으로

## 일반 원칙
- "~없음/~필요/~가능" 명사 종결이 산문에 박히면 "~없다/~해야 한다/~할 수 있다" 로 풀기
- 영어 1:1 수동/직역 어순("X 한계로 재정의" → "X 의 한계로 문제를 다시 정의한다")
