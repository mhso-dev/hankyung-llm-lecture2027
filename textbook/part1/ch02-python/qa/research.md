# Ch 2 Python 공식 조사 메모

확인일: 2026-09-09  
조사 유형: 구현 참조 및 현재 기준 확인  
범위: Ch 2의 12개 절에서 사용할 Python 3.12 표준 라이브러리, pytest, Pydantic v2, uv의 공식 문서와 PyPI 배포 정보입니다. 아래 예제는 공식 문서의 코드를 복사하지 않고 이 과정의 변수명과 상황으로 새로 작성합니다.

## 기준 버전과 라이선스

| 대상 | Ch 2 고정 버전 | PyPI 확인 결과 | 라이선스 | 집필 판단 |
| --- | --- | --- | --- | --- |
| Python | `==3.12.*` | Python 3.12 문서는 3.12.14 기준 | PSF License 2 | 3.12 문법만 사용합니다. `type` 별칭 문은 3.12에 새로 추가되었습니다. |
| pytest | `9.1.1` | 최신 안정판 9.1.1, 2026-06-19, Python `>=3.10` | MIT | Python 3.12에서 설치할 수 있습니다. |
| Pydantic | `2.13.5` | 최신 안정판 2.13.5, 2026-08-28, Python `>=3.9` | MIT | v1 문법을 섞지 않고 v2의 `model_validate()`를 사용합니다. |
| uv | `0.12.11` | `uv_build` 0.12.11과 같은 릴리스 계열 | MIT OR Apache-2.0 | `uv run`, `uv sync`, `uv build`의 실행 주체입니다. |
| uv_build | `0.12.11` | 최신 안정판 0.12.11, 2026-09-08, Python `>=3.8` | MIT OR Apache-2.0 | 패키지 예제의 build backend로 사용합니다. |

- PyPI: [pytest 9.1.1](https://pypi.org/project/pytest/), [Pydantic 2.13.5](https://pypi.org/project/pydantic/), [uv_build 0.12.11](https://pypi.org/project/uv-build/).
- Python 라이선스: [PSF License 2](https://docs.python.org/3.12/license.html). Python 문서의 코드 예제는 별도 Zero-Clause BSD로도 제공되지만, 이 챕터는 원문을 재현하지 않습니다. [문서 저작권·라이선스 안내](https://docs.python.org/3.12/library/asyncio.html)

## 절별 공식 근거와 집필 기준

### 01 변수와 자료형

- Python 자습서는 숫자·문자열·리스트를 기본 출발점으로 제시합니다. 변수는 값 그 자체가 아니라 값을 가리키는 이름이라는 범위에서 설명하고, 출력으로 타입과 값을 함께 확인합니다. [Python 자습서 3장](https://docs.python.org/3.12/tutorial/introduction.html)
- 변경 가능한 `list`와 변경할 수 없는 `tuple`을 같은 값의 묶음으로 비교합니다. 목록 메서드는 원본 목록을 바꾸며, `pop()`은 제거한 값을 반환합니다. [자료 구조 자습서](https://docs.python.org/3.12/tutorial/datastructures.html)

### 02 조건문과 반복문

- `if`에는 0개 이상의 `elif`와 선택적인 `else`가 올 수 있습니다. `for`는 시퀀스나 반복 가능한 객체의 항목을 순서대로 처리하는 방식으로 설명합니다. [제어 흐름 자습서](https://docs.python.org/3.12/tutorial/controlflow.html)
- `range()`의 끝값은 포함되지 않으며, `break`와 `continue`는 반복 흐름을 바꿉니다. 초보 예제에서는 조건과 반복 횟수가 출력에서 보이게 합니다. [제어 흐름 자습서](https://docs.python.org/3.12/tutorial/controlflow.html)

### 03 자료구조

- 목록, 튜플, 집합, 사전은 같은 데이터를 다른 방식으로 저장한다는 질문으로 구분합니다. 목록의 `remove()`는 값이 없으면 `ValueError`, `pop()`은 잘못된 위치나 빈 목록에서 `IndexError`를 일으키므로 예외 절과 연결할 수 있습니다. [자료 구조 자습서](https://docs.python.org/3.12/tutorial/datastructures.html)

### 04 함수

- 함수는 `def`로 정의하고, 인자·반환값·지역 이름의 범위를 짧은 셀에서 확인합니다. 기본 인자값은 함수 정의 시 한 번만 평가되므로, 변경 가능한 기본값을 피해야 합니다. 기본값이 필요하면 `None`을 두고 함수 안에서 새 목록을 만듭니다. [함수 정의 자습서](https://docs.python.org/3.12/tutorial/controlflow.html#defining-functions), [기본 인자값](https://docs.python.org/3.12/tutorial/controlflow.html#default-argument-values)

### 05 파일과 예외

- 텍스트 파일은 `with open(path, encoding="utf-8")` 형태로 열고, 파일을 닫는 일을 `with`가 맡는다는 흐름을 보여 줍니다. 인코딩을 생략하면 플랫폼 기본값을 따르므로 UTF-8을 명시하는 편이 권장됩니다. `w` 모드는 기존 파일을 비우고, `a`는 끝에 추가합니다. [입출력 자습서](https://docs.python.org/3.12/tutorial/inputoutput.html#reading-and-writing-files)
- 문법 오류와 실행 중 예외를 구분합니다. `try`의 `except`는 예상한 구체 예외만 처리하고, 정리 작업에는 `finally`를 사용합니다. 사용자 정의 예외는 보통 `Exception`을 상속합니다. [오류와 예외 자습서](https://docs.python.org/3.12/tutorial/errors.html)

### 06 클래스

- 클래스는 데이터와 기능을 함께 묶어 새 객체 유형을 정의합니다. 인스턴스의 속성은 상태를, 메서드는 상태를 다루는 동작을 표현합니다. 이 절의 예제는 상속보다 생성자·인스턴스 속성·메서드에 집중합니다. [클래스 자습서](https://docs.python.org/3.12/tutorial/classes.html)

### 07 모듈과 타입 힌트

- 모듈은 Python 정의와 문장이 들어 있는 `.py` 파일이며, 파일명에서 `.py`를 뺀 이름으로 가져옵니다. `import *`는 권장하지 않는다는 공식 자습서의 안내에 따라, 학습 예제는 필요한 이름을 명시적으로 가져옵니다. [모듈 자습서](https://docs.python.org/3.12/tutorial/modules.html)
- 타입 힌트는 Python 실행기가 강제하지 않습니다. 타입 검사기·IDE·린터가 해석하는 약속이며, 런타임 입력 검증은 Pydantic 절에서 별도로 다룹니다. Python 3.12의 `type` 문은 타입 별칭을 만드는 문법입니다. [typing 모듈](https://docs.python.org/3.12/library/typing.html)

### 08 pytest

- fixture는 반복해서 쓸 준비 작업을 정의하고, 테스트 함수가 이름으로 요청하면 pytest가 값을 제공합니다. 기본 scope는 `function`이며 테스트가 끝나면 정리됩니다. [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- `monkeypatch`로 환경 변수·속성·사전 항목을 테스트 동안 바꿀 수 있습니다. 표준 라이브러리 원본이 아니라 **검사 대상 모듈이 참조하는 이름**을 패치합니다. pytest 자체가 쓰는 내장 함수의 전역 패치는 피합니다. [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

### 09 데코레이터와 컨텍스트 매니저

- 이 절은 함수 호출 전후에 동작을 더하는 데코레이터와 `with` 블록의 시작·종료 처리를 분리해 설명합니다. 파일 예제의 `with`는 컨텍스트 관리자의 실제 사용 사례로 다시 연결합니다. 세부 프로토콜 설명은 후속 확장으로 두고, 실행 예제는 `contextlib.contextmanager`나 사용자 정의 객체 중 하나만 사용합니다. [contextlib 모듈](https://docs.python.org/3.12/library/contextlib.html), [함수 정의 자습서](https://docs.python.org/3.12/tutorial/controlflow.html)

### 10 Pydantic v2

- Pydantic의 기본 모드는 가능한 값 변환을 시도합니다. 예를 들어 문자열 `"123"`은 `int` 필드로 변환될 수 있습니다. `model_validate(..., strict=True)`를 쓰면 변환 대신 검증 오류를 냅니다. [Pydantic strict mode](https://pydantic.dev/docs/validation/2.12/concepts/strict_mode/)
- 엄격성은 호출 단위, `Field(strict=True)`인 필드 단위, `ConfigDict(strict=True)`인 모델 단위로 설정할 수 있습니다. JSON 입력의 엄격성은 Python 객체 입력보다 일부 타입에서 느슨할 수 있으므로, 동일한 예제로 둘을 같은 규칙이라고 설명하지 않습니다. [Pydantic strict mode](https://pydantic.dev/docs/validation/2.12/concepts/strict_mode/)

### 11 패키징과 테스트 격리

- `uv_build`는 소스 트리를 source distribution과 wheel로 변환하는 build backend입니다. 공식 권장 선언은 아래와 같습니다. 상한을 함께 두어 이후 릴리스가 빌드를 바꾸지 않게 합니다. [uv build backend](https://docs.astral.sh/uv/concepts/build-backend/)

  ```toml
  [build-system]
  requires = ["uv_build>=0.12.11,<0.13"]
  build-backend = "uv_build"
  ```

- 현재 Ch 2 실습 환경의 `[tool.uv] package = false`와 `uv-build` 일반 의존성만으로는 위 backend가 켜지지 않습니다. 패키징을 보일 별도 예제 프로젝트의 `pyproject.toml`에 `[build-system]`을 넣고 `uv build`로 확인해야 합니다. `uv_build`는 순수 Python 코드만 지원합니다. [uv build backend](https://docs.astral.sh/uv/concepts/build-backend/)
- 테스트 격리는 fixture의 기본 함수 scope와 `monkeypatch`의 자동 복원을 이용해 설명합니다. 실제 네트워크나 개인 환경 변수에 의존하는 테스트는 만들지 않습니다. [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

### 12 async와 await

- `asyncio`는 `async`/`await` 문법으로 동시 실행 코드를 작성하는 표준 라이브러리입니다. 이벤트 루프는 한 번에 한 Task를 협력적으로 실행하므로, Task가 `await`로 기다리는 동안 다른 Task가 실행됩니다. [asyncio 개요](https://docs.python.org/3.12/library/asyncio.html), [코루틴과 Task](https://docs.python.org/3.12/library/asyncio-task.html)
- 코루틴 안에서 일반 차단 I/O 함수를 직접 호출하면 이벤트 루프가 멈춥니다. `asyncio.to_thread(func, ...)`는 그 함수를 별도 스레드에서 실행하고 await 가능한 코루틴을 반환합니다. 이는 보통 I/O 결합 작업에 맞으며, GIL 때문에 일반적인 CPU 결합 작업의 병렬화 수단으로 설명하면 안 됩니다. [asyncio.to_thread](https://docs.python.org/3.12/library/asyncio-task.html#asyncio.to_thread)

## 버전·범위 주의

- Python 공식 3.12 문서는 확인 시점에 3.12.14를 표시하지만, 실습 환경의 요구 조건은 `==3.12.*`입니다. 실제 실행 기록에는 사용한 patch 버전을 `python --version` 출력으로 남겨야 합니다.
- Pydantic의 strict mode 문서는 현재 2.12 경로로 제공됩니다. 설치 고정값은 2.13.5이므로, 수록 전 노트북에서 `model_validate(strict=True)`, `Field(strict=True)`, `ConfigDict(strict=True)`를 2.13.5로 실행해 API 호환을 확인합니다.
- 이 문서는 공식 문서와 PyPI만 사용했습니다. 보조 블로그·튜토리얼이나 외부 저장소 예제는 사용하지 않았습니다.
