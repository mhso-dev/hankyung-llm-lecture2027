from functools import lru_cache

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool


@tool
def lookup_library_hours(day: str) -> str:
    """한빛도서관의 요일별 운영 시간을 조회합니다."""
    hours = {"월요일": "09:00~18:00", "화요일": "09:00~21:00"}
    return hours.get(day, "해당 요일의 운영 시간 정보가 없습니다")


@lru_cache(maxsize=1)
def build_live_agent():
    """환경 변수의 OpenAI 키를 사용하는 실제 도구 호출 Agent를 만듭니다."""
    model = init_chat_model(
        "openai:gpt-5.4-mini",
        temperature=0,
        timeout=30,
    )
    return create_agent(
        model=model,
        tools=[lookup_library_hours],
        system_prompt="도서관 운영 시간 질문은 반드시 도구로 확인한 뒤 한국어 한 문장으로 답하세요.",
    )
