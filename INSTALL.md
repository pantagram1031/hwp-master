# 설치 및 배포 가이드 (Claude Code / Codex / Cowork / claude.ai)

## 빠른 설치와 진단

`.hwp`를 직접 편집하는 전체 워크플로우에는 **Windows에 로컬 데스크톱
한컴오피스 한글이 먼저 설치되어 있어야 한다.** 이 저장소는 한컴오피스나 그
라이선스를 포함·설치하지 않는다. 한컴독스 웹 버전만으로는 COM 백엔드를 실행할 수 없다.

```powershell
git clone https://github.com/pantagram1031/hwp-master.git
cd hwp-master
python -m pip install ".[windows,proof,test]"
python scripts/doctor.py --require-com --require-proof
python -m pytest -q
```

COM이 필요 없는 Linux/macOS CI 또는 오프라인 HWPX 검사만 설치할 때:

```bash
python -m pip install ".[test]"
python scripts/doctor.py --json
```

위 최소 설치는 외부 런타임 패키지 없이 핵심/XML 명령만 준비한다. PDF proof가
필요하면 `python -m pip install ".[proof]"`를 추가한다.

## 사전 준비 (Windows, COM 백엔드용)
```powershell
# Python 3.12 권장 (한글 2022 기준 검증 환경)
pip install pyhwpx pywin32
# 레이아웃 QA(공백/간격 수치 측정·PDF 렌더)용
pip install pymupdf
# (선택) 이미지 종횡비 자동 높이 — 없으면 PNG 헤더 직독으로 폴백
pip install pillow
# 확인
python -c "from pyhwpx import Hwp; h=Hwp(); print('OK'); h.quit()"
python -c "import fitz; print('pymupdf', fitz.__version__)"
```
첫 실행 시 pyhwpx가 보안모듈을 자동 등록한다. 한글 프로세스가 떠 있으면 모두 종료 후 실행.
`scripts/layout_qa.py`(레이아웃 수치 게이트)는 pymupdf(fitz)가 필요하다.

## 1. Claude Code (Windows) — 권장 메인 환경
```powershell
# 개인 스킬로 설치
xcopy /E /I hwp-master %USERPROFILE%\.claude\skills\hwp-master
# 또는 프로젝트 스킬: <프로젝트>\.claude\skills\hwp-master
```
이후 Claude Code에서 "이 보고서.hwp에 수식 넣어줘" 같은 요청 시 스킬이 트리거된다.
PDF 검증: Claude Code는 PDF/이미지를 직접 읽을 수 있으므로 `--export-pdf` 결과를
열어 보라고 하면 시각 검증까지 루프가 완성된다.

## 2. OpenAI Codex (Windows)
Codex는 동일한 SKILL.md 규격을 지원한다.
```powershell
# 개인 스킬
xcopy /E /I hwp-master %USERPROFILE%\.agents\skills\hwp-master
# 팀/프로젝트 스킬: <프로젝트>\.agents\skills\hwp-master
```
추가로 프로젝트 AGENTS.md에 한 줄 박아두면 안정적이다:
> 한글(.hwp/.hwpx) 문서 작업은 반드시 `.agents/skills/hwp-master/SKILL.md`의
> 절차(inspect → ops 편집 → save-as → PDF 검증)를 따른다.

pantakit 통합: pantakit의 school/research 도메인 프로필에서 이 스킬 경로를
양쪽 엔진(claude/codex) 공용 자산으로 등록하면 한 벌로 유지보수된다.

## 3. Claude Cowork
Cowork는 격리 VM에서 동작하므로 **COM(로컬 한글 접근)은 보장되지 않는다.**
- 스킬 설치: Cowork의 스킬/플러그인 메뉴로 이 폴더를 등록 → XML 백엔드 경로 사용
- COM이 필요한 작업(수식 픽셀 퍼펙트, .hwp 직접 편집)은 Code 탭(=Claude Code)으로 핸드오프

## 4. claude.ai (웹)
리눅스 샌드박스 → COM 불가, **XML 백엔드 전용**.
- 기존 hwpx 스킬이 이미 업로드되어 있으므로 .hwpx 생성/편집은 그대로 동작
- 이 스킬에서 가져갈 것: `scripts/eqn.py` (LaTeX→HwpEqn 변환은 순수 파이썬이라 샌드박스에서 동작)
- .hwp 파일이 오면: "Windows의 Claude Code에서 편집하거나 .hwpx로 재저장 요청"으로 안내

## 디렉토리 구조
```
hwp-master/
├── SKILL.md                      # 의사결정 트리 + 워크플로우
├── INSTALL.md                    # 이 문서
├── scripts/
│   ├── com_backend.py            # Windows COM (inspect/edit/convert)
│   ├── eqn.py                    # LaTeX → HwpEqn
│   ├── form_inspect.py           # 양식/앵커/쪽 지표 추출
│   ├── layout_plan_check.py      # 집필 전 cast-off 게이트
│   ├── fill_report.py            # 조립·측정·proof 루프
│   ├── tidy_hwpx.py              # 오프라인 HWPX 정리
│   ├── contact_sheet.py          # 전체 PDF proof sheet
│   └── doctor.py                 # 설치/의존성/연동 진단
└── references/
    ├── hwpeqn_cheatsheet.md      # 한글 수식 문법
    └── com_api_reference.md      # pyhwpx/HAction 패턴
```

## 선택적 비공개 회귀 픽스처

공개 저장소와 CI는 합성 픽스처만 사용한다. 실제 양식으로 추가 회귀 테스트를
실행하려면 다음 환경변수만 로컬에서 설정한다. 파일은 Git에 추가하지 않는다.

```powershell
$env:HWP_MASTER_PRIVATE_FIXTURES="C:\private\hwp-fixtures"
$env:HWP_MASTER_FORM_FIXTURE="C:\private\form.hwpx"
$env:HWP_MASTER_OUTPUT_FIXTURE="C:\private\out.hwpx"
$env:HWP_MASTER_ASSEMBLED_FIXTURE="C:\private\out.hwpx"
$env:HWP_MASTER_LAYOUT_FIXTURES="C:\private\layout-pdfs"
```

## 첫 스모크 테스트 (Windows에서)
```powershell
# 1) 아무 .hwp 파일 구조 확인
python scripts\com_backend.py inspect --file 테스트.hwp

# 2) 수식 하나 삽입해 보기
echo [{"op":"move","to":"doc_end"},{"op":"insert_equation","latex":"E=mc^2"}] > ops.json
python scripts\com_backend.py edit --file 테스트.hwp --ops ops.json --save-as 결과.hwpx --export-pdf 검증.pdf

# 3) 검증.pdf 열어서 수식 확인 → 결과.hwpx를 한글로 열어 최종 확인
```
