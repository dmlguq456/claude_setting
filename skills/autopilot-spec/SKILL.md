---
name: autopilot-spec
description: "_요구사항·청사진 작성_ 의 일반화 entry — 신규 의도 또는 기존 코드 정돈·공개 준비 자리 모두. mode 5종 (app / library / api / cli / research) + 다중 + auto. PRD 구조 = 공통 + mode 별 독립 섹션. autopilot-research / analyze-project 결과 자동 인용. analyze-project 의 _신규 의도 → 청사진_ 대칭 자리. 실제 코드 작업은 autopilot-code 가 담당 (specs/<name>/ 컨텍스트 자동 감지)."
argument-hint: "<task description> [--mode auto|app|library|api|cli|research (콤마로 다중) | setup-only] [--qa quick|light|standard|thorough] [--user-refine]"
---

> 산출물 폴더: `.claude_reports/specs/<name>/` (CONVENTIONS.md §5 3-tier).

## Purpose — _요구사항·청사진 작성_ entry

본 skill 은 _코드 작업이 아닌_ 자리 담당. _무엇을 만들지·어떻게 정돈할지·공개 자리 어떤 API_ 같은 _spec 청사진_ 결정:

| Mode | 자리 | spec 의 핵심 |
|---|---|---|
| **app** | 사용자 대상 앱 (Next.js / Expo 등) | 피처·시나리오·API Contract·data model·ui flow + 스택·scaffolding·skeleton |
| **library** | 공개 라이브러리·패키지 (npm·pip·crate) | 공개 API (export 함수·class·type) + 사용 예시 + 호환성·versioning + module 구조 |
| **api** | 백엔드 API 서비스 (UI 없음) | endpoint·body·error·auth·rate limiting + 데이터 모델 |
| **cli** | 명령줄 도구 | 명령·옵션·서브 명령·input/output·exit code |
| **research** | 연구·실험 코드 정돈·재현성 | entry point (train·eval) + 실험 설정 (configs) + 재현 명령 + 예상 metric + baseline 비교 |

복합 mode (예: `library + cli`, `research + cli`) 자연 — 한 프로젝트가 _여러 측면_ 가지면 _복합 PRD_ 자연. PRD 가 _공통 + mode 별 섹션_ 으로 구성.

> 코드 작업 자체 (실제 함수·class·API 구현·리팩터링·디버그) 는 **autopilot-code** 가 담당 — `specs/<name>/` 컨텍스트 자동 감지로 spec Read 후 그 청사진 따라 구현.

## 흐름 안에서 본 skill 의 자리

```
사전:    autopilot-research (외부 조사) + analyze-project (기존 코드 분석)
           ↓
청사진:   autopilot-spec  ← 본 skill. mode 별 PRD + (app mode 만) scaffolding·skeleton
           ↓
시각:    autopilot-design  ← (옵션, UI 자리만)
           ↓
구현:    autopilot-code  ← spec 자동 Read, 그 청사진 따라 구현 (반복)
           ↓
보강:    autopilot-spec --mode setup-only  ← (가끔, app mode 만) ship 첫 setup·env·domain·migration deploy 안내
```

## Default Invocation Rule (메인 Claude 자동 라우팅)

본 skill 은 글로벌 [`CLAUDE.md`](../../CLAUDE.md) §6 "autopilot-* 호출 패턴" 의 _컨펌 의무_ 적용 대상.

### Trigger 신호 (자연어 발화 예시)

| mode | 발화 |
|---|---|
| **app** | "X 앱 만들어줘" / "Y 서비스" / "PRD 부터" |
| **library** | "X 라이브러리로 정리" / "npm 패키지로 만들자" / "공개 API 정리" |
| **api** | "X API 서버 만들자" / "endpoint 정리" |
| **cli** | "X CLI 도구" / "명령줄 옵션 정리" |
| **research** | "X 연구 코드 정돈" / "재현성 준비" / "학회 공개 코드 준비" |
| **복합** | "라이브러리 + CLI 도구로" / "연구 코드 + 재현 가능 CLI" |
| **보강 setup (app)** | "Vercel 셋업" / "배포 준비" / "env 변경·domain 연결" |

### Default 옵션 권장값

- `--mode`: **`auto`** (default) — 발화·기존 코드·산출물 검사로 자동 추론 (단일 또는 복수)
- `--qa`: `standard` (high-stakes 신호 시 thorough 자동 상향)
- `--user-refine`: **off** (사용자 명시 시만 on)

### Override 1순위 — autopilot 우회

- 코드 작업 (구현·리팩터링·디버그) — `/autopilot-code` 직접 (spec 자동 Read)
- 디자인만 — `/autopilot-design` 직접
- 작은 작업 (한 파일 수정·rename) — `Agent(개발팀)` 직접
- `/autopilot-spec <args>` slash 직접 입력 — 컨펌 skip

## Language Rule
- Think in English internally. Write user-facing output in Korean.
- Code identifiers, file paths, technical terms stay in English.

## Argument Parsing

### --mode (auto-detect default)

| 값 | 의미 |
|---|---|
| `auto` (default) | 발화·코드 단서로 자동 추론. 단일 또는 복수 mode |
| `app` | 앱 spec — PRD + 스택 + scaffolding + skeleton |
| `library` | 라이브러리 spec — 공개 API + 사용 예시 + 호환성·versioning + module 구조 |
| `api` | API 서비스 spec — endpoint + auth + 데이터 모델 |
| `cli` | CLI spec — 명령·옵션·input/output |
| `research` | 연구 코드 spec — entry + configs + 재현 명령 + 예상 metric |
| `app,library` 등 콤마 | 복수 mode — 한 PRD 안 mode 별 독립 섹션 |
| `setup-only` (app mode 한정) | 보강 setup — ship 첫 setup·env·domain·migration deploy 안내 |

### --qa
- `quick` / `light` / `standard` (default) / `thorough` — [CONVENTIONS.md §1](../../CONVENTIONS.md)

### --user-refine
- PRD 작성 후 사용자 메모 받고 refine loop (`_internal/refine_v{N}.md` 백업)

## Mode 자동 추론 단서 (`auto` 기본)

| 단서 | 추론 mode |
|---|---|
| `package.json` 의 `bin` 필드 / `setup.py` 의 `entry_points` / `pyproject.toml` 의 `[project.scripts]` | **cli** |
| `package.json` 의 `main` / `exports` / `pyproject.toml` 의 `[project]` + `__init__.py` 의 명시 export | **library** |
| `argparse` / `click` / `commander` / `typer` import | **cli** |
| `configs/*.yaml` + 학습·평가 metric 출력 / `*.ipynb` | **research** |
| Next.js / Expo / SvelteKit / Astro / Vite + React framework | **app** |
| FastAPI / Express / Hono + UI 없음 | **api** |
| 발화 키워드 | 발화 mode |

자동 추론 결과는 _컨펌 한 줄_ 로 사용자 확인 후 진행:

```
=== mode 추론 ===
- 발화 "정돈·공개" + 기존 코드 분석:
  · train.py / eval.py + argparse  → cli ✓
  · configs/ + 학습 metric 출력      → research ✓
  · models/__init__.py 의 export    → library ✓ (옵션)

복합 mode: research + cli (+ library 옵션) — 이대로 진행?
(진행 / 수정 — mode 추가·제거 / 단일 mode 선택 / 중단)
```

## Procedure

### Step 1: 정보 수집 (read-only, 컨펌 X)

**1-1. 프로젝트 name 추출** — 발화·cwd·기존 `package.json`·`pyproject.toml` 등.

**1-2. mode 자동 추론** — 위 단서 표 적용.

**1-3. 기존 자산 분석** — `analyze-project` 산출물 (`.claude_reports/analysis_project/code/`) 발견 시 자동 인용. 부재 시 cwd 코드 직접 검사.

**1-4. autopilot-research 결과 자동 import** — `.claude_reports/research/` 발견 시 reference 패턴·외부 baseline 인용.

**1-5. (app mode 만) 환경·스택 후보 정리** — Node / pnpm / Docker 확인, 스택 후보 2-3 안.

### Step 2: 한 화면 컨펌

```
=== Spec 결정 자리 ===
프로젝트 name:    <name>
mode (추론):     <mode list> (근거: <증거>)
사전 자료:       autopilot-research / analyze-project 발견 — 인용 자리 N

(app mode 만 추가) 환경 / 스택 후보:
  Node ✓ / pnpm ✓ / Docker ✗
  스택: 1. Next.js+Prisma+Turso  2. Expo+tRPC  3. SvelteKit+Drizzle
  → 권장 1순위 (근거: <발화>)

이대로 진행? (진행 / 수정 — mode·스택 변경 / 중단)
```

### Step 3: PRD 작성 — 공통 + mode 별 섹션

`specs/<name>/01_spec/PRD.md`:

```markdown
# <Project Name> Spec

## 공통
- Module 구조
- 의존성
- 언어·런타임 버전
- License

## [app] (해당 mode 만)
### 피처 목록 (P0/P1/P2)
### 사용자 시나리오 (3-5개)
### 비기능 요구
### 데이터 모델 초안 (entity·관계·migration plan)
### API Contract (백·프론트 공유 — endpoint·body·error·auth)
### 화면 흐름 (UI 있을 시)

## [library] (해당 mode 만)
### 공개 API (export 함수·class·type)
### 사용 예시 (README 자리)
### 호환성·versioning (semver 정책)
### Module 구조 (src/{io, core, utils}/ 같은)

## [api] (해당 mode 만)
### Endpoint (POST /api/X / GET /api/Y / ...)
### Body / Response shape
### Error code
### Auth (token / OAuth / API key)
### Rate limiting

## [cli] (해당 mode 만)
### 명령 (train / eval / serve / ...)
### 옵션 (--config / --resume / --output / ...)
### Input/Output 형식
### Exit code

## [research] (해당 mode 만)
### Entry point (train.py / eval.py / 명령 예시)
### 실험 설정 (configs/*.yaml 구조)
### 재현 명령 (학습·평가·테스트)
### 예상 metric (PSNR / Acc / SI-SDR / 등)
### Baseline 비교
```

mode 가 단일이면 _해당 섹션만_, 복수면 _각 섹션 독립_.

### Step 4: (app mode 한정) Scaffolding + Skeleton 코드 생성

app mode 만:
- `create-next-app` 등 scaffolding
- `prisma/schema.prisma` 또는 동등 — entity 정의만
- 빈 page routes — _Hello world_ 정도
- 기본 layout
- 실제 기능 (CRUD logic) 은 **autopilot-code 자리**, 본 skill 안 X

library / api / cli / research mode 는 _코드 생성 안 함_ — 기존 코드 위 청사진만. autopilot-code 가 본 spec 따라 실제 구현·정돈.

### Step 5: [CONFIRM Gate — refine 진입 가능]

```
Spec 완성:
  mode: <list>
  주요 결정: <요약 3-5 bullet>

(진행 — autopilot-design 또는 autopilot-code / 수정 — refine v2 / 중단)
```

`--user-refine` on 또는 사용자 _수정_ 발화 시 PRD refine loop.

## Mode B — `setup-only` (app mode 한정 보강)

이미 `specs/<name>/` 있고 _ship 첫 setup·env·domain·migration deploy 안내_ 자리:

### Step 1: 현재 상태 점검
- `pipeline_state.yaml` 의 stack 검증
- `git remote -v` (GitHub 연결)
- 기존 `vercel.json`·`.github/workflows/`·`.env.example` 발견 여부
- git working tree clean 검증

### Step 2: 사용자 발화 분류

| 신호 | 처리 |
|---|---|
| "배포 셋업" / "Vercel" | **ship 첫 setup** |
| "env 변경" | env 보강 |
| "도메인" | DNS 안내 |
| "migration 운영 배포" | DB migration deploy 안내 (destructive 위험) |

### Step 3: ship 첫 setup (가장 흔함)

**3-1. 호스팅 선정** — 사용자 confirm:

| 스택 | 권장 |
|---|---|
| Next.js | Vercel |
| Next.js + heavy backend | Fly.io |
| 정적 | Cloudflare Pages |
| 컨테이너 | Railway |
| Mobile (Expo) | EAS Build |

**3-2. `.env.example`** — 실제 값 없음, 키만

**3-3. CI/CD 셋업** — `.github/workflows/deploy.yml` (사용자 confirm 후)

**3-4. 도메인** (옵션) — DNS 안내

**3-5. 배포 명령 안내** — `vercel login` / `vercel link` / `vercel deploy --prod` — 사용자 직접 실행

**3-6. `05_ship/deploy_record.md` 작성**

## Forbidden Zones (명시 요청 없이 X)

- 실제 배포 명령 (`vercel deploy`, `fly deploy` 등) — 안내만
- 결제 정보·credit card 등록
- DNS 직접 변경
- 도메인 구매
- 환경변수 _실제 값_ 입력 (사용자 dashboard 직접)
- production DB migration 자동 실행

## CONFIRM Gate 응답 분기 (모든 Gate 공통)

| 응답 | 처리 |
|---|---|
| **진행** | 다음 단계 또는 종료 |
| **수정** | 현 단계 refine v2 (`_internal/refine_v{N}.md` 백업) |
| **back-jump** | 이전 단계 재실행 + 하위 무효화 |
| **중단** | 멈춤, `pipeline_state.yaml` 상태 보존 |

발화 모호 시 옵션 다시 물음 (임의 추측 X).

## Pipeline state 관리

`specs/<name>/pipeline_state.yaml`:

```yaml
project_name: <name>
created: <date>
mode: [library, cli, research]   # 또는 단일 [app]
(app mode 만) stack:
  framework: <chosen>
  db: <chosen>
phases:
  spec: done                    # PRD 완성
  (app mode 만) scaffolding: done
  (app mode 만) skeleton: done
  design: pending               # autopilot-design 진행 시 done
  dev: in_progress              # autopilot-code 가 누적
  (app mode 만) ship_setup: pending
last_updated: <timestamp>
```

autopilot-code 가 본 폴더 안 `dev_log/` 에 누적.

## Return Format

```
.claude_reports/specs/<name>/ -- ✅ spec completed (mode: <list>)
```

다음 단계 안내:
- spec 완료 → "autopilot-design (시각 자리) 또는 autopilot-code (구현·정돈)"
- (app mode) setup 완료 → "이후 push 만으로 자동 deploy"

## Update memory

- 사용자 자주 만나는 mode 조합 (예: research + cli)
- mode 자동 추론 단서 보강
- 스택·언어 선호
- ship setup 자주 만나는 함정

## Examples

### 예시 1 — 가사관리 앱 (단일 app mode)

```
/autopilot-spec "할 일 + 가계부 가사관리 웹 앱"
→ mode auto → app 추론
→ PRD: 피처·시나리오·API Contract·data model·ui flow
→ 스택: Next.js + Prisma + Turso
→ scaffolding + skeleton
→ specs/가사관리/01_spec/PRD.md
```

### 예시 2 — TF-Restormer 연구 코드 정돈 (복합 research + cli)

```
/autopilot-spec "TF-Restormer 정돈·재현성 준비"
→ mode auto → research + cli 추론 (configs/ + argparse + ipynb 단서)
→ PRD 공통: module 구조, 의존성, license
→ PRD [research]: entry / configs / 재현 명령 / 예상 metric
→ PRD [cli]: train.py / eval.py 명령·옵션
→ specs/TF-Restormer/01_spec/PRD.md (코드 생성 X — autopilot-code 가 본 spec 따라 정돈)
```

### 예시 3 — npm 라이브러리 (복합 library + cli)

```
/autopilot-spec "audio-utils — Node 라이브러리 + CLI 도구"
→ mode auto → library + cli
→ PRD [library]: 공개 API (loadAudio / saveAudio / ...) + 사용 예시 + semver
→ PRD [cli]: au-tool 명령 + 옵션
→ specs/audio-utils/01_spec/PRD.md
```
