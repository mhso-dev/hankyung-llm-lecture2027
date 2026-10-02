# 새 챕터 템플릿

이 폴더는 기존 Ch 8의 Jupyter 화면과 공통 노트북 렌더러를 새 챕터에서도 사용하기 위한 작성 도구입니다. 본문 구성과 검토 기준은 [`textbook/AUTHORING.md`](../AUTHORING.md)를 먼저 확인합니다.

짧은 셀은 실행 단위를 나누는 기준입니다. 새 절은 기본 예시를 충분히 설명한 뒤 다른 상황의 예시와 개념 비교·반례를 주제에 맞게 이어 붙입니다. 옵션은 결과 차이를 이해하는 데 필요한 것부터 설명합니다. 자세한 기준은 집필 안내의 「개념을 여러 예시로 깊게 설명하기」를 따릅니다.

## 첫 절 생성

프로젝트 루트에서 다음 명령을 실행합니다. 아래 Ch11 이름과 절 제목은 형식을 보여 주는 예시이며 실제 커리큘럼에 맞게 바꿉니다. 생성 도구는 Python 3.12로 실행합니다.

```bash
uv run --no-project --python 3.12 python textbook/_template/scaffold.py \
  --root . \
  --part 3 \
  --chapter ch11-evaluation \
  --title "평가 파이프라인" \
  --section 01-평가-준비 \
  --format paired
```

`paired`는 같은 문제의 실패 코드와 수정 코드를 비교하는 절입니다. 반복 측정 결과를 해석하는 절은 `--format experiment`를 사용합니다. 명령은 `chapter.json`, 짧은 `_build.py`, `_src` 본문, 실습 노트북, 집필 점검표를 만듭니다. 기존 챕터나 실습 폴더는 덮어쓰지 않습니다.

프로젝트 밖의 격리된 루트에서 생성할 수도 있습니다. 그 루트에는 먼저 `textbook/_template`과 `textbook/_notebook` 공통 도구를 같은 상대 경로로 복사합니다. `--root /tmp/course-draft`처럼 루트를 지정하면 생성 경로가 그 루트를 벗어나는 요청을 거부합니다.

## 같은 챕터에 절 추가

첫 절을 만든 뒤에는 `--add-section`을 붙입니다.

```bash
uv run --no-project --python 3.12 python textbook/_template/scaffold.py \
  --root . \
  --part 3 \
  --chapter ch11-evaluation \
  --title "평가 파이프라인" \
  --section 02-반복-평가 \
  --format experiment \
  --add-section
```

추가 명령은 새 본문과 노트북을 만들고 `chapter.json`의 절 목록 끝에 등록합니다. `--title`은 명령 형식을 일정하게 유지하기 위해 받지만, 기존 챕터 제목은 바꾸지 않습니다. 같은 절 파일이 있으면 중단합니다.

## 작성, 실행, 빌드

생성된 `[[작성: ...]]` 표시는 집필 위치입니다. 실제 설명과 완성 코드로 모두 바꿉니다. 학생용 노트북은 프로젝트 전용 helper를 import하지 않고 빈 Python 3.12 커널에서 첫 셀부터 실행되어야 합니다.

노트북은 공통 실행기로 새 커널에서 실행합니다. 먼저 실습 폴더의 `pyproject.toml`과 `uv.lock`에 수업 패키지와 Python 3.12를 고정합니다. 아래 경로는 생성한 챕터에 맞게 바꿉니다.

```bash
uv -q run \
  --project labs/part3/ch11-evaluation \
  --with nbclient==0.11.0 \
  --with ipykernel==7.3.0 \
  --with pip \
  --with python-dotenv==1.2.3 \
  python textbook/_notebook/execute.py \
  labs/part3/ch11-evaluation/notebooks/01-평가-준비.ipynb \
  --cwd "$(pwd)"
```

실행이 끝나면 챕터 빌더를 실행합니다.

```bash
uv -q run --project labs/part3/ch11-evaluation --with pillow python textbook/part3/ch11-evaluation/_build.py
```

빌더는 다음 상태에서 출판용 HTML 생성을 거부합니다.

- `chapter.json`, `_src`, 노트북에 `[[작성: ...]]`가 남아 있습니다.
- 노트북이 새 커널 실행 검증을 받지 않았거나 코드·출력이 검증 뒤 바뀌었습니다.
- 노트북 형식과 `chapter.json`의 `paired` 또는 `experiment` 값이 다릅니다.
- 학생용 본문에 강사 노트가 들어 있습니다.

실행 출력과 검증 메타데이터는 생성 시 비어 있습니다. 다른 챕터의 출력이나 검증 해시를 복사하지 않습니다. 초안의 `NotImplementedError`는 미작성 코드를 실행하지 않게 하는 표시이며 학생에게 보여 줄 실패 예제가 아닙니다. 주제에 맞는 완성 코드로 교체합니다.

이후 `verify.py --chapter`, 화면·복사 검사, 시작 화면·배포 묶음 등록, 진행표 갱신은 [집필 안내의 실행·빌드·발행 순서](../AUTHORING.md#실행빌드발행-순서)를 따릅니다. 주제 점검표는 자동 검사 결과와 별도로 실제 셀과 출력을 읽어 작성합니다.
