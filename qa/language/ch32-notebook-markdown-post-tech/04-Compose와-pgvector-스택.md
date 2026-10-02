<!-- cell 0 -->
# Compose와 pgvector 스택

Docker Desktop의 실습 전용 이미지와 스택만 사용해 결과를 확인합니다.

<!-- cell 1 -->
## 실행 환경 준비

이 노트북 전용 Compose 프로젝트의 기존 자원을 먼저 정리합니다.

<!-- cell 2 -->
## 설정 검증

Compose 파일을 정규화해 app과 db 서비스가 있는지 확인합니다.

<!-- cell 3 -->
## 실패 재현

스택이 없을 때 호스트의 API 주소는 연결을 거부합니다.

<!-- cell 4 -->
## 수정

DB healthcheck가 통과한 뒤 app을 시작하도록 Compose 스택을 실행합니다.

<!-- cell 5 -->
## pgvector와 인덱스 확인

데이터베이스 안에서 확장 버전과 HNSW 인덱스를 직접 조회합니다.
