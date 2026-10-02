# Ch32 실행 검증

- 실행일: 2026-09-11
- 환경: macOS arm64, Python 3.12.13, Docker Desktop 4.71.0, Engine 29.4.1, Compose 5.1.3
- 패키지: uv 0.12.13, FastAPI 0.135.1, psycopg 3.3.2, Uvicorn 0.41.0, PostgreSQL 17.11, pgvector 0.8.6

## 실제 결과

- 01절: 최적화 이미지의 레이어 기록을 읽고 임시 컨테이너의 `/tmp/lesson.txt` 변경을 `docker diff`에서 확인했습니다. 같은 이미지의 새 컨테이너에는 해당 파일이 없었습니다.
- 02절: runtime에서 Python 3.12가 실행되고 uv 명령은 없었습니다. 잘못된 target `buidler`는 실패했고 `builder` target에는 실행 가능한 uvicorn이 있었습니다.
- 03절: 기준 이미지는 418,111,662바이트, 최적화 이미지는 57,560,686바이트였습니다. 감소율은 86.2%이며 두 이미지에서 같은 health 결과를 확인했습니다.
- 04절: app과 db가 healthy가 되었고 `/ready`는 ready, `/vector-count`는 1을 반환했습니다. DB에서 pgvector 0.8.6과 `course_vectors_embedding_hnsw`를 확인했습니다.
- 05절: 잘못된 DB 호스트에서는 `/health`가 200이고 `/ready`가 503이었습니다. 정상 스택에서는 app과 db가 healthy였고 `/ready`도 200이었습니다. 최근 로그에 요청 경로가 있으면서 공개 예제 비밀번호 문자열은 없었습니다. app의 Compose healthcheck는 liveness만 검사하므로 readiness를 별도 HTTP 호출로 검증했습니다.

## 실행 범위와 정리

- 공통 실행기로 5개 노트북, 코드 셀 23개를 새 커널에서 실행했습니다. 가장 긴 코드 셀은 13줄입니다.
- Docker 자원은 `ch32-` 이미지와 `ch32-course-stack` 프로젝트, `ch32-unready` 임시 컨테이너로 한정했습니다.
- Compose 실습이 만든 컨테이너, 네트워크와 `pgdata` 볼륨은 각 노트북 끝에서 삭제했습니다. 학습용 이미지 태그만 로컬 Docker에 남았습니다.
- Excalidraw MCP를 사용할 수 없어 같은 명세에서 SVG와 Excalidraw JSON 원본을 생성했습니다.
- 화면 검사는 1280px와 390px에서 6개 HTML 모두 본문 크기, 대비, 잘림, 화면 밖 요소, SVG 경계, 가로 넘침, 이미지, 복사와 실패 블록 검사를 통과했습니다.

## 해석 제한과 확인 필요 항목

크기와 캐시 수치는 현재 arm64 로컬 환경의 한 차례 실행 결과입니다. 레지스트리 압축 전송량과 다른 CPU 플랫폼의 크기를 나타내지 않습니다. 공개 예제 시크릿은 운영 값이 아닙니다. 별도 모델의 한국어 감사와 독립 기술 검토를 완료했습니다.

## 통합 재검증

노트북 폴더를 작업 위치로 지정해 다섯 노트북을 모두 새 커널에서 다시 실행했습니다. 준비 셀이 상위 폴더에서 실습 파일을 찾습니다. 비밀번호는 URI 문자열에 삽입하지 않고 psycopg의 별도 인자로 전달합니다. `@:/%`를 포함한 공개 시험 비밀번호로 실제 PostgreSQL 인증과 SELECT 1을 확인했습니다. 도식은 `_gen_figures.py`의 같은 요소 목록에서 SVG와 상자·텍스트·화살표가 있는 Excalidraw JSON으로 재생성했습니다.
