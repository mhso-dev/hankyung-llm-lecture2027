# Ch 16 가드레일 · 안정화 실습

노트북 일곱 개(`notebooks/01~07-*.ipynb`)는 Python 3.12 새 커널에서 절마다 따로 실행할 수 있습니다. 앞 절의 변수는 쓰지 않고, 필요한 자료는 준비 셀에서 파일로 읽습니다. 각 노트북의 첫 코드 셀은 LangChain 1.4.0, langchain-openai 1.6.1, python-dotenv 1.2.3을 설치합니다. 프로젝트 맨 위 `.env`의 `OPENAI_API_KEY`를 읽지만, 키 값은 출력하거나 파일에 저장하지 않습니다.

실습 폴더(`labs/part4/ch16-guardrails`)에서 `uv sync --locked`를 실행하고, 이 폴더의 `.venv` 커널을 고릅니다. 그다음 `notebooks/` 폴더의 노트북을 열어 첫 셀부터 차례로 실행합니다. VS Code와 Jupyter는 노트북이 있는 폴더에서 커널을 시작합니다.

`notebooks/guardrails.py`는 앞에서 배운 함수를 모아 둔 도구 파일입니다. 파일을 열면 코드를 볼 수 있습니다. 노트북과 같은 폴더(`notebooks/`)에 있는 파일이고, 02·03·05·06·07절 노트북이 `from guardrails import …` 한 줄로 가져옵니다. 커널이 `notebooks/` 폴더에서 시작해야 이 파일을 가져올 수 있습니다. 함수 스물다섯마다 이 챕터의 어느 절에서 배웠는지 주석으로 적었습니다(01절 다섯, 02절 둘, 03절 넷, 04절 둘, 05절 여섯, 06절 여섯). 이 파일은 `hashlib`·`json`·`math`·`re`만 씁니다.

실습은 입력과 출처 검사, 개인정보 가리기, 대화 기록 자르기와 요약, 호출 한도와 비용 상한, 다시 부르기·예비 흐름과 감사 기록, 검색 문서 속 지시 끼워 넣기 검사와 한 흐름 잇기 차례로 진행합니다. 개인정보 예와 공격 문서는 모두 이 챕터에서 지어낸 가짜 자료입니다. 실제 사람의 정보나 바깥에서 가져온 공격 문서는 쓰지 않습니다.

`data/retrieved-documents.json`에는 문서 둘(안내 문서 `E01`, 지어낸 공격 문서 `E99`)이 있고, 01·02·04~07절 노트북이 읽기만 합니다. 05·06절은 실습 폴더의 `runs/05-audit.jsonl`·`runs/06-audit.jsonl`에 감사 기록을 여는 방식 `"w"`로 덮어씁니다. `runs/` 폴더가 없으면 노트북이 먼저 만들고, 다시 실행해도 같은 내용이 남습니다. 01~04절과 07절은 파일을 쓰지 않습니다.

노트북 일곱 개를 한 번씩 모두 실행하면 모델 요청은 열네 번이고 임베딩 요청은 없습니다. 절별로는 01·02·03절 한 번씩, 04절 세 번, 05절 두 번(기본 모델 `gpt-5.4-mini` 한 번·예비 모델 `gpt-5.4-nano` 한 번), 06·07절 세 번씩입니다. 나머지 요청은 모두 `gpt-5.4-mini`(`temperature=0`·`reasoning_effort="none"`)에 보냅니다. 노트북마다 요금표로 어림한 실행 요금은 미화 0.01달러 아래이고, 실제 청구 금액과는 다를 수 있습니다. 04절이 정한 요청 하나의 예상 비용 0.002달러는 예약에 쓰는 정한 값이고, 요금 어림이나 청구 금액이 아닙니다.

06절 실험에서는 방어 없이 문서를 넣은 요청과 문서를 구역으로 감싼 요청 모두 모델이 문서 속 지시를 따르지 않았습니다. 그래서 이 실험으로는 구역 감싸기의 효과를 가를 수 없습니다. 06절은 모델을 부르기 전에 말 목록으로 문서를 검사해 의심 문서를 격리하는 흐름을 노트북에서 직접 실행합니다.

`tests/test_guardrails.py`의 테스트 일곱 개는 모델을 부르지 않고 도구 파일 함수만 확인합니다. 실습 폴더에서 `uv run python -m pytest -q tests`로 실행합니다. `pyproject.toml`의 `pythonpath = ["notebooks"]` 설정 덕분에 테스트가 `notebooks/guardrails.py`를 가져옵니다.

교재 저장소 맨 위에서 노트북 일곱 개를 새 커널로 한꺼번에 실행하고 테스트까지 돌릴 때는 아래 명령을 씁니다. `--cwd`로 커널의 작업 폴더를 `notebooks/`로 정해야 도구 파일을 가져옵니다. 명령이 부르는 `textbook/_notebook/execute.py`는 교재 저장소에만 있고 학생 묶음에는 없습니다.

```bash
uv run --project labs/part4/ch16-guardrails \
  --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 \
  python textbook/_notebook/execute.py \
  --cwd labs/part4/ch16-guardrails/notebooks \
  labs/part4/ch16-guardrails/notebooks/*.ipynb

uv run --project labs/part4/ch16-guardrails python -m pytest -q \
  labs/part4/ch16-guardrails/tests
```

07절 「가드레일 실습: 상담 질문 셋에 가리기·예약·감사 기록 붙이기」는 챕터 끝 실습 절입니다(30분 안팎, 따로 내는 과제 없음). 가짜 개인정보가 하나씩 든 상담 질문 셋을 02절 `mask_pii`로 가리고, 04절 `reserve`로 예약한 뒤 `gpt-5.4-mini`에 보내고, 05절 감사 기록과 같은 칸 넷으로 노트북 안 기록 목록에 한 줄씩 남깁니다. 예약에서 멈춘 질문도 사건 `stopped`로 남깁니다. 실행 1은 호출 한도 2, 실행 2는 호출 한도 1이고 모델 요청은 모두 세 번입니다. 앞 절 함수는 `notebooks/guardrails.py`에서 가져오며, 이 노트북은 파일을 쓰지 않고 `runs/`의 감사 기록 파일도 건드리지 않습니다.
