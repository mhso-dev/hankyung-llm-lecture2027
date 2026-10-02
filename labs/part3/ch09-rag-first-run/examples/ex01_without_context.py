"""01절의 검색 없는 모델 호출입니다.

생성 결과가 달라지고 API를 호출하므로 2026-09-08 보완 과정에서는 다시 실행하지 않았습니다.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from langchain.chat_models import init_chat_model

from rag import DEFAULT_CHAT

model = init_chat_model(DEFAULT_CHAT)
print(model.invoke("미르시립도서관의 정기 휴관일은 언제인가요?").content)
