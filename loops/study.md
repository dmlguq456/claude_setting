# 연수 (주간 자율 audit — 외부 동향 × 현 세팅 대조)

어떤 지침·설정 파일도 직접 수정하지 않는다. 산출은 제안서 1개뿐 — 채택은 사용자 서명, 적용 후 검증은 모의훈련(drill).

## 절차

1. **이전 연수 복기**: `/home/nas/user/Uihyeop/notes/study/` 의 최근 보고 1~2개 Read — 같은 제안 반복 금지, 미채택 항목은 "재상정 가치 있을 때만" 한 줄 갱신.
2. **외부 동향 조사** (WebSearch·WebFetch):
   - Anthropic engineering 블로그·Claude Code changelog 신규 글/기능
   - agent engineering 실무 패턴 신간 (harness·context·loop engineering, 멀티에이전트, eval)
   - 커뮤니티에서 자리 잡는 컨벤션 (헛소문·과장 글은 출처 품질로 거름)
3. **현 세팅 대조**: `~/.claude/CLAUDE.md`·`CONVENTIONS.md`(특히 §5.8~5.10)·`loops/README.md`·`hooks/` 목록을 Read 하고, 조사 결과와 비교 — 우리가 이미 하는 것 / 빠진 것 / 더 잘하는 것 구분.
4. **내부 위생 (가볍게)**: `loops/drill/metrics.csv` 의 g0_overhead in_tok 추세 (세팅 세금 증감) + 지침 문서 간 모순·비대 후보 1~2건 + **의도 불명 지침** (왜·날짜·계기 주석 없는 규칙 — CONVENTIONS §3.6 위반) 후보 1~2건. **상한 경보**: g0 in_tok 45k 초과 시 ⚠️ 다이어트 권고 (2026-06-11 기준선 ~40k; context 파일 과다는 성능 역효과 — 매뉴얼 1부 Tension ④ 반례 데이터).
5. **주간 사용 결산 (재무)**: `loops/*.log` 의 지난 7일 run 횟수·소요시간, `loops/drill/metrics.csv` cost 합산, `~/.claude/.dispatch/jobs.log` 의 주간 job 수 — 표 한 개로. 이상 급증(전주 대비 2배+)만 ⚠️ 플래그. 절대액 평가는 하지 않는다 (구독 사용량이라 — 추세·쏠림만).

## 제안서 — `/home/nas/user/Uihyeop/notes/study/<날짜 YYYY-MM-DD>.md`

제안별로: **무엇을** / **왜** (출처 링크) / **우리 세팅 어디에** (파일·절) / **예상 비용** (구현 + 세팅 세금 영향) / **우선순위** (🔴지금·🟡다음·🟢참고). 제안 0 건이어도 파일은 남긴다 — `# 연수 — <날짜>\n신규 제안 없음 (조사 N건 검토)` (heartbeat).

과장 금지 — "도입하면 좋다"가 아니라 "우리 세팅의 어느 마찰을 줄이나"로만 정당화. 마찰 불명이면 🟢참고로 격하.
