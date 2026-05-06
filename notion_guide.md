# Notion 운영 가이드

> 본 파일은 Notion 작업 시 참조하는 _도메인 가이드_입니다 (workspace 구조 + 페이지 타입 템플릿 + 운영 규칙). Claude Code 메인 컨텍스트에서 직접 Notion MCP 도구를 호출할 때 이 가이드를 따르세요.
>
> 이전: `agents/record-team.md` (sub-agent)로 분리되어 있었으나, sub-agent runtime의 MCP 도구 접근 제약으로 (2026-05-06) 메인 Claude가 직접 처리하는 방식으로 이전. **sub-agent에 위임하지 말 것** — 도구가 안 보임.

---

## TL;DR — Notion 작업 시 절차 (반드시 이 순서)

CLAUDE.md의 도메인 트리거가 발동하면 (사용자가 노션·Notion·기록·실험 결과 정리 등을 언급), 다음 4단계 _순서대로_:

1. **본 파일 Read** — Notion 작업 _시작 전_에 본 파일 전체를 한 번 읽고 (i) workspace 구조, (ii) 적절한 페이지 타입, (iii) 운영 규칙을 머리에 깔아둠.
2. **MCP 도구 로드** — `ToolSearch(query="select:mcp__claude_ai_Notion__notion-search,mcp__claude_ai_Notion__notion-fetch,mcp__claude_ai_Notion__notion-update-page,mcp__claude_ai_Notion__notion-create-pages,mcp__claude_ai_Notion__notion-create-comment")`. 자주 쓰는 5개. 필요 시 추가.
3. **Search-fetch first** — 같은 작업의 기존 페이지가 있는지 `notion-search`로 확인 → 있으면 사용자에게 "이미 있음, 갱신할까 / 새로 만들까" 묻기. 없으면 새로 생성.
4. **작업 실행** — 페이지 타입에 맞는 템플릿 ([Type 1-4](#페이지-타입) 참조) + 안전 규칙 ([페이지 갱신 안전 규칙](#notion-페이지-갱신-안전-규칙)) 준수.

**sub-agent로 위임 금지**. 메인 Claude가 직접. (sub-agent runtime은 MCP 도구를 못 봄)

---

## Notion MCP 도구 사용 cheat sheet

| 작업 | 도구 | 비고 |
|---|---|---|
| 페이지 검색 | `notion-search` | 키워드로 페이지/DB 항목 찾기 |
| 페이지 콘텐츠 읽기 | `notion-fetch` | id 또는 URL. update 전에 반드시 fetch |
| 페이지 콘텐츠 부분 갱신 | `notion-update-page (command="update_content")` | old_str → new_str 다중 search-replace. **이걸 default로** |
| 페이지 콘텐츠 전체 교체 | `notion-update-page (command="replace_content")` | **위험** — 자식 페이지 삭제 가능. 거의 사용 X |
| 페이지 properties 갱신 | `notion-update-page (command="update_properties")` | DB 항목의 status/tag 등 |
| 페이지 생성 | `notion-create-pages` | 부모 페이지/DB id 필수 |
| 댓글 추가 | `notion-create-comment` | 페이지 또는 inline |

**update_content 사용 패턴**:
```python
notion-update-page(
    page_id="...",
    command="update_content",
    properties={},
    content_updates=[
        {"old_str": "정확히 일치해야 하는 기존 텍스트", "new_str": "새 텍스트"},
        # ... 여러 부분 동시 갱신 가능 (max ~100)
    ]
)
```

**중요**: `old_str`은 fetch 결과의 워딩과 _한 글자도_ 어긋나면 실패. 정확히 복사·붙여넣기.

## Workspace Structure

### Core DBs (HOME level)

| DB | 용도 | 주요 속성 |
|---|---|---|
| **mpWAV** | 회사 업무 | Project, Process (TODO/DOING/DONE), Subject, Importance, Now, Deadline |
| **IIPLab** | 연구실/연구 작업 | Project, Process, Process[Lab Meeting], Urgency, Subject, Deadline |
| **Research** | 개인 연구 (논문) | mpWAV & IIPLab과 연결됨 |
| **Notes** | 빠른 메모/아이디어 | Tags (Paper Idea/Task/Web_Tip), 중요 |
| **Reference** | 논문 레퍼런스 | Journal/Conference, Field, index, 중요도, year, PDF, AI summary |

### Key Pages

- **Agents/Skills** (`34987c2bb75380d68df4d6ce4d469bff`) — Claude Code skill/agent documentation. `/sync-skills`가 자동 갱신.
- **CLAUDE Notion** (`32287c2bb75381a59d18dc724b7dd343`) — 운영 지침 (source of truth)
- **📋 Templates** (`32887c2bb75381839bd2e04dd6ec532c`) — 페이지 생성 템플릿

## 작성 원칙

1. **Concise** — 핵심만. filler / 중복 설명 금지. one fact = one line.
2. **Uniform format** — 아래 페이지 타입 템플릿 사용. 새 구조 발명 금지.
3. **Short breath** — bullet > paragraph. 숫자는 표. 글 덩어리 금지.

## 페이지 타입

컨텍스트에서 페이지 타입을 판별하고 매칭되는 템플릿 사용. 새 페이지 생성 시 먼저 📋 Templates에서 가져옴.

### 공통 구조 (모든 타입)

모든 페이지는 다음 layout:
1. **Dashboard** (상단) — status/goal 한눈에. 현재 상태를 찾기 위해 스크롤 X.
2. **History summary** — `📋 이력 (최신순)`, 항목당 max 5줄, 설정 + 결과 capture.
3. **Body** — 날짜/주제 섹션을 **toggle headings** (`## heading {toggle="true"}`)로, 최신순.
4. 새 항목 추가 시: **history summary 먼저 갱신**, 그 다음 toggle 섹션.

### Type 1: 실험 로그

쓰는 시점: training / evaluation / ablation / hyperparameter tuning

```
## 📌 현재 목표
One-line goal

## 📋 실험 이력 (최신순)
- MM.DD: experiment description + key result (max 5 lines per entry)

---
## 🗓️ YYYY.MM.DD — {toggle="true"}
	- Purpose in 1 line
	- Settings: **lr=2e-4**, **batch=4**, **epoch=20**
	- Result: **PESQ 3.21** (prev 3.15 → +0.06)
	- Next plan
	| Setting | Value |
	|---|---|

---
## 📊 종합 결과 {toggle="true"}
	| Experiment | Setting | PESQ | STOI | Note |
	|---|---|---|---|---|
```

### Type 2: 회의록

쓰는 시점: lab meeting / company meeting / discussion

```
## 📌 회의 정보
| 항목 | 내용 |
|---|---|
| 일시 | YYYY.MM.DD (HH:MM) |
| 장소 | — |
| 참석자 | — |
| 목적 | — |

---
## 📝 안건 및 논의 내용
### 1. 안건명
- Key discussion points (bullet, concise)

---
## ✅ Action Items
| 담당자 | 할 일 | 마감 |
|---|---|---|

---
## 💡 기타 메모
```

### Type 3: 논문 작업

쓰는 시점: paper writing / submission / review response / rebuttal / camera-ready

```
## 📌 현재 상태
| 항목 | 내용 |
|---|---|
| 논문 제목 | — |
| 타겟 저널 | — |
| 단계 | 작성 / 투고 / 리뷰 대응 / 리버틀 / 카메라레디 |
| 마감 | — |

## 📋 작업 이력 (최신순)
- MM.DD: what was done + key result (max 5 lines per entry)

---
## 📝 작성 진행 {toggle="true"}
	| Section | Status | Memo |
	|---|---|---|
	| Abstract | — | — |
	| Introduction | — | — |
	| ... | | |

## 📨 리뷰 대응 {toggle="true"}
	### Reviewer 1
	- **코멘트**: —
	- **대응**: —
	- **실험/수정**: —

## 🔄 리버틀 {toggle="true"}
	### 주요 변경사항
	- —
	### 추가 실험
	- —

---
## 🗓️ YYYY.MM.DD — {toggle="true"}
	- Work done (bullet, concise)
```

### Type 4: 보고용 정리

쓰는 시점: 완료된 작업의 보고용 요약 (예: weekly report, project update)

별도 템플릿 없음 — 대상 DB의 기존 페이지에 날짜 섹션 추가/갱신. 같은 toggle + dashboard 패턴 적용.

## 운영 규칙

### 작업 전

1. **Search first** — `notion-search`로 기존 페이지/항목 확인. 관련 콘텐츠가 이미 있으면 보고: "이미 관련 내용이 있습니다: [page title] — 추가할까요, 새로 만들까요?"
2. **Fetch before edit** — `notion-fetch`로 현재 콘텐츠 읽고 수정.
3. **Partial update preferred** — `update_content` > `replace_content`.

### 페이지 생성

1. 페이지 타입 판별 (실험 / 회의 / 논문 / 보고)
2. 📋 Templates에서 매칭 템플릿 fetch
3. 템플릿 구조 기반 생성
4. 적절한 DB에 배치 (mpWAV vs IIPLab vs Research — 모호하면 사용자에게 질문)

### 콘텐츠 규칙

- **toggle 섹션당 5-7 bullet 이하.** 더 detail 필요하면 사용자가 요청하도록.
- 표는 _숫자 결과_에만. prose에는 사용 X.
- 명시 confirmation 없이 콘텐츠 삭제 금지.
- MCP 도구로 deletion 불가 — 사용자에게 수동 삭제 요청.
- Workspace 구조는 HOME fetch로 결정 (search로 추론 X).

## Notion 페이지 갱신 안전 규칙

### Agents/Skills 페이지 (`34987c2bb75380d68df4d6ce4d469bff`)

`/sync-skills`로 갱신할 때 다음 안전 규칙 _반드시_ 준수:

1. **`update_content`만 사용**. `replace_content`는 사용 금지 — 자식 페이지 삭제 위험.
2. **`<columns>` 안의 `<page>` / `<database>` 자식 링크는 절대 삭제 X**. old_str에 그 영역을 포함시키지 말 것.
3. **search-and-replace는 두 단계로 분리**:
   - (1) 상단 대시보드 영역 교체 (시작 헤더 ~ columns 직전 `---`)
   - (2) 페이지 하단 `*마지막 업데이트: ...*` 라인의 날짜만 갱신
4. fetch로 현재 콘텐츠를 받아 정확한 old_str을 만든 뒤 교체. old_str은 fetch 결과 워딩과 한 글자도 어긋나면 실패.
5. 첫 시도 실패(validation_error 등) 시 재시도하되, `allow_deleting_content`는 절대 true 설정 X.

## 자주 쓰는 작업 패턴

### 1. 실험 결과 로깅
- 페이지 타입: 실험 로그
- 📋 실험 이력 summary 갱신 (max 5줄)
- 🗓️ 날짜 toggle 섹션에 settings + results 추가
- 📊 종합 결과 표 갱신 (해당 시)

### 2. 회의록
- 페이지 타입: 회의록
- 📌 회의 정보 표 채우기
- 안건 항목 concise 기록
- ✅ Action Items 채우기

### 3. 논문 작업 로깅
- 페이지 타입: 논문 작업
- 📌 현재 상태 표 갱신 (단계, 마감)
- 📋 작업 이력 summary 갱신
- 관련 toggle (작성/리뷰/리버틀)에 콘텐츠 추가

### 4. 보고 요약
- 대상 DB에서 기존 프로젝트 페이지 찾기
- 날짜 섹션 추가/갱신 (concise summary)
- 페이지 history summary 섹션 갱신

### 5. Skill 문서 갱신
`~/.claude/` skill 파일 변경 시 `/sync-skills` 호출 — 자동으로 Agents/Skills 페이지 상단 대시보드 갱신.

`/sync-skills`는 메인 Claude가 직접 실행하며, 본 가이드의 [페이지 갱신 안전 규칙](#notion-페이지-갱신-안전-규칙) 5조항을 그대로 따릅니다. (Agents/Skills 페이지의 `<columns>` 안 자식 페이지 링크 11개는 _절대_ 건드리지 말 것.)

---

## 자주 빠지는 함정

1. **sub-agent로 위임** — 절대 X. sub-agent runtime은 `mcp__claude_ai_Notion__*` 도구를 못 봄. 메인 Claude가 직접 호출.
2. **`replace_content` 사용** — 자식 페이지 삭제 위험. _거의 항상_ `update_content`로 부분 갱신.
3. **`old_str` 부정확** — fetch 결과를 그대로 복사했는지 확인. emoji·줄바꿈·공백까지 정확히 일치해야 함.
4. **페이지 생성 시 템플릿 무시** — 📋 Templates에서 fetch 후 그 구조를 따를 것. 새 layout 발명 X.
5. **HOME 구조 추론** — search 결과만으로 DB 추론하지 말고, HOME (`https://www.notion.so/...`) fetch로 정확한 구조 확인.
6. **자식 페이지 / 자식 DB 삭제** — `update_content` 시 `<page>` 또는 `<database>` 태그가 포함된 영역은 _절대_ old_str에 넣지 말 것. 삭제 시 자식 페이지가 트래시로 이동.
7. **워크스페이스 외부 deletion 시도** — MCP는 페이지 삭제 미지원. 사용자에게 수동 삭제 요청.
