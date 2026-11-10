# 소설을 영화 시나리오로 각색하기

소설이나 중편을 **장편 영화 시나리오**로 옮길 때 쓰는 스킬입니다. 스킬은 AI에 작업 순서와 검토 기준을 알려주는 지침 파일입니다. 이 스킬을 쓰면 AI가 원작을 검토하고 장면과 삭제 후보를 제안합니다. 중요한 결정은 작가가 내립니다.

예를 들어 내가 쓴 소설에서 주인공의 불안이 독백으로만 드러난다면, AI에 그 감정을 보여줄 행동을 제안해 달라고 할 수 있습니다. 소설에서 같은 정보를 전하는 두 인물을 합치고 싶다면, 어떤 장면이 사라지고 결말이 어떻게 바뀌는지 확인한 다음 결정할 수 있습니다. 각 장면에 `[C07]` 같은 원작 장 번호가 남아서 수정 이유를 되짚기 쉽습니다.

## 시작하기

아래에서 쓰는 도구에 맞는 방법 하나를 선택합니다. 명령은 기존 `adapting-novels-to-screenplays` 폴더가 없는 디렉터리에서 실행합니다.

**Codex**에서 특정 작품에만 설치하려면 작품 폴더에서 실행합니다.

```bash
git clone --branch ko https://github.com/H13m0n/adapting-novels-to-screenplays.git
mkdir -p .agents/skills
cp -R adapting-novels-to-screenplays/adapting-novels-to-screenplays .agents/skills/
```

**Claude Code**에서 내 프로젝트 전반에 설치하려면 다음 명령을 실행합니다.

```bash
git clone --branch ko https://github.com/H13m0n/adapting-novels-to-screenplays.git
mkdir -p ~/.claude/skills
cp -R adapting-novels-to-screenplays/adapting-novels-to-screenplays ~/.claude/skills/
```

**Claude 웹 또는 데스크톱**에서는 [한국어 브랜치](https://github.com/H13m0n/adapting-novels-to-screenplays/tree/ko)를 내려받고, 내부의 `adapting-novels-to-screenplays` 폴더만 ZIP으로 묶어 **Customize → Skills → Upload a skill**에서 올립니다. 스킬 업로드와 코드 실행을 사용할 수 있는 환경인지 먼저 확인합니다.

원작 PDF, EPUB, DOCX 또는 텍스트 파일을 작업 폴더에 넣거나 첨부하고, 이렇게 요청합니다.

> 내가 쓴 이 소설을 한국어 장편 영화로 각색해 줘. 먼저 원작 검토 보고서를 보여주고 내가 결정할 때까지 기다려 줘.

Python 3가 필요합니다. PDF 읽기에는 `pypdf`, EPUB 읽기에는 `beautifulsoup4`, DOCX 읽기에는 별도로 설치하는 `pandoc`, PDF 출력에는 `reportlab`을 사용합니다. 필요한 패키지가 없다면 사용하는 작업 환경에 설치합니다. 예를 들어 PDF 읽기와 출력을 모두 하려면 `python3 -m pip install pypdf reportlab`을 실행합니다. 텍스트로 읽히는 원작의 `제1장`, `제 2 장`, `3장` 같은 표기는 장 제목으로 인식합니다. 스캔한 PDF는 텍스트로 추출할 수 있는지 먼저 확인합니다.

## 진행 순서

| 단계 | 확인하거나 받는 것 |
|---|---|
| 0. 접수 | 원작에서 텍스트를 추출하고 장별로 정리합니다. |
| 1. 원작 검토 | 이야기의 뼈대, 장르, 분량, 결말을 검토한 뒤 방향을 승인합니다. |
| 2. 설계 | 인물 설정집, 분위기의 참고작, 영화의 형식을 결정합니다. |
| 3. 삭제와 통합 | 삭제·압축·통합할 대목과 그 영향을 보고 승인합니다. |
| 4. 장면 개요 | 장면 순서, 출처가 된 원작 장, 복선과 회수 계획을 검토합니다. |
| 5. 집필 | 처음 10페이지를 검토한 뒤 여러 장면씩 이어갑니다. |
| 6. 퇴고 | 대사를 소리 내 읽고 서브텍스트, 장면 전환, 복선과 회수를 점검합니다. |
| 7. 전달 | Fountain과 PDF 원고, 인물 설정집, 변경 기록, 로그라인, 한 페이지 줄거리, 다시 볼 장면 목록, 상태 파일을 받습니다. |

다음에 이어서 작업하려면 `adaptation-state.json`, `script.fountain`, `character-bible.md`를 함께 첨부합니다. 상태 파일에는 어디까지 썼는지, 작가가 어떤 결정을 내렸는지가 들어 있습니다.

## 한국어 원고와 PDF

Fountain은 시나리오를 저장하는 텍스트 형식입니다. 한글 장면 제목 앞에는 점, 인물명 앞에는 `@`를 붙입니다. `Title:`, `Credit:`, `Author:`, `Source:` 같은 표지 키는 영어로 쓰고 값은 한국어로 적습니다.

```fountain
Title: 밤의 복도
Author: 홍길동

.병원 복도 - 밤 #1#

지연이 닫힌 병실 문 앞에 선다.

@지연
아직 안 늦었죠?
```

작업 폴더에 보조 스크립트를 `adapt.py`라는 이름으로 복사한 뒤 PDF를 내보냅니다. 한글 원고에는 `--font`로 한글 TrueType 글꼴 파일을 지정해야 합니다. 지정한 글꼴은 PDF에 포함됩니다. 아래 예시 경로를 실제 글꼴 파일 경로로 바꿉니다.

```bash
python3 adapt.py render script.fountain script.pdf --font /path/to/korean-font.ttf
```

한국어 PDF를 내보낼 수 있는 편집기에서 Fountain 원고를 열어 저장하는 방법도 있습니다. 페이지당 단어 수와 자동 `NOLAN`·카메라 표현 검사는 영어 기준이므로, 한국어 원고는 지문을 읽고 PDF의 글자, 줄바꿈, 분량을 직접 확인합니다.

## 원본과 라이선스

이 한국어판은 [Alma Kamberi의 원본 스킬](https://github.com/almakamberi/adapting-novels-to-screenplays)을 바탕으로 만들었습니다. 원본 작법 지침은 크리스토퍼 놀런, 마틴 스코세이지, 루스 프라워 잡발라의 공개 발언을 참고합니다. [MIT 라이선스](LICENSE)를 따릅니다.
