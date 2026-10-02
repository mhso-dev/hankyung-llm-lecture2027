# 실제 Agent HTTP 통합



OpenAI 모델과 조회 도구가 있는 LangChain `create_agent`를 FastAPI에서 실제 호출합니다.
## 실행 환경 준비



이 노트북은 `labs/part7/ch30-fastapi-serving`을 작업 폴더로 사용합니다. 비밀 키를 출력하지 않습니다.
## 키 존재 확인



상위 폴더의 `.env`를 읽고 키 값은 출력하지 않습니다.
## 실제 ainvoke HTTP 요청



Agent는 운영 시간을 도구로 확인한 뒤 한 문장으로 답합니다.
## 도구 호출 궤적 확인



같은 실제 Agent의 메시지에서 도구 이름, 입력, 도구 출력을 확인합니다.
## 실제 astream HTTP 요청



같은 Agent의 모델 메시지 청크를 SSE token 이벤트로 받습니다.
## 실험 결과 해석



결정적 그래프와 실제 모델 Agent의 출력 성질을 구분합니다.
