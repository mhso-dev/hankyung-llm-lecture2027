# 실행 방식 참고 자료

확인일: 2026-09-08. 학생용 코드는 기존 챕터의 선택 라이브러리를 직접 사용하며, 아래 자료는 실행·표시 도구의 근거입니다.

- [nbclient 실행](https://nbclient.readthedocs.io/en/latest/client.html): 새 커널, 작업 폴더, 오류 시 중단, 출력 저장.
- [nbformat](https://nbformat.readthedocs.io/en/latest/): 셀 source·execution_count·outputs 구조.
- [IPython %pip](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip): 현재 커널에 패키지를 설치합니다.
- [python-dotenv](https://bbc2.github.io/python-dotenv/reference/): find_dotenv(usecwd=True)는 현재 폴더에서 상위 폴더를 찾습니다.
- [GPT-5.4 mini](https://openai.com/index/introducing-gpt-5-4-mini-and-nano/): 표준 입력 100만 토큰당 0.75달러, 출력 4.50달러.
- [text-embedding-3-small](https://developers.openai.com/api/docs/models/text-embedding-3-small): 입력 100만 토큰당 0.02달러.

검증 도구에서 확인한 버전: nbclient 0.11.0, nbformat 5.11.1, ipykernel 7.3.0. 비용은 실행 규모 산정을 위한 확인일 기준 값이며 실제 청구 금액은 계정 사용 내역으로 확인합니다.

## LangChain 호출 통일 확인

2026-09-08에 LangChain 1.4.0·langchain-openai 1.6.0의 공식 문서와 해당 버전 소스를 확인했습니다.

- [모델 생성과 호출](https://docs.langchain.com/oss/python/langchain/models): `init_chat_model("openai:gpt-5.4-mini")`와 `invoke()`.
- [메시지](https://docs.langchain.com/oss/python/langchain/messages): `AIMessage.text`와 선택 항목인 `usage_metadata`의 `input_tokens`·`output_tokens`·`total_tokens`.
- [OpenAI 임베딩](https://docs.langchain.com/oss/python/integrations/embeddings/openai): `OpenAIEmbeddings.embed_documents()`와 `embed_query()`.
- [임베딩 API 반환형](https://reference.langchain.com/python/langchain-openai/embeddings/base/OpenAIEmbeddings): `dimensions` 지원 범위와 벡터 반환형. 이 메서드의 공개 반환값에는 API 토큰 사용량이 없습니다.
