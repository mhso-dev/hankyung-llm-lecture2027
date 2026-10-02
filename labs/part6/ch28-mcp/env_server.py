"""Ch 28 03절 환경 확인 서버 — 이 서버 프로세스가 받은 환경 변수를 알려 주는 연습 서버입니다.

03절 Before·After에서 서버에 무엇이 넘어갔는지 보려고 만든 서버입니다.
실제 서버에는 환경 변수를 알려 주는 도구를 두지 않습니다.
"""
import os

from fastmcp import FastMCP

mcp = FastMCP("환경 확인 서버")


# 이 줄은 아래 함수를 서버의 도구로 등록합니다
@mcp.tool
def env_names():
    """이 서버 프로세스가 받은 환경 변수의 이름을 한 줄에 하나씩, 차례대로 알려 줍니다."""
    names = sorted(os.environ)
    return "\n".join(names)


# 이 줄은 아래 함수를 서버의 도구로 등록합니다
@mcp.tool
def env_value(name: str):
    """환경 변수 이름 하나를 받아, 이 서버 프로세스가 그 이름으로 받은 값을 알려 줍니다. 없으면 「없음」입니다."""
    if name in os.environ:
        return os.environ[name]
    return "없음"


if __name__ == "__main__":
    # 파일을 직접 실행할 때만: 표준 입력·출력으로 요청을 주고받는 stdio 서버로 엽니다
    mcp.run(transport="stdio")
