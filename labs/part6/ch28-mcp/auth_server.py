"""Ch 28 03절 권한 연습 서버 — 접근 토큰으로 부르는 쪽을 확인하고, 쓰기 도구는 관리 범위가 있는 토큰에만 보입니다.

StaticTokenVerifier는 개발·시험용입니다. 접근 토큰이 파일에 글 그대로 적혀 있어, 실제 서비스에서는 쓰지 않습니다.
"""
import sys

from fastmcp import FastMCP
from fastmcp.server.auth import StaticTokenVerifier, require_scopes

# 교재용 가짜 접근 토큰 둘과, 토큰마다 허락한 범위(scope)입니다
tokens = {
    "reader-token-demo": {"client_id": "reader", "scopes": ["read"]},
    "admin-token-demo": {"client_id": "admin", "scopes": ["read", "admin"]},
}
mcp = FastMCP("권한 연습 서버", auth=StaticTokenVerifier(tokens=tokens))

# 규정은 서버 메모리에만 둡니다(파일에 쓰지 않아, 서버를 끝내면 처음 글로 돌아갑니다)
rules = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
}


# 이 줄은 아래 함수를 서버의 도구로 등록합니다(인증을 지난 요청이면 누구에게나 보입니다)
@mcp.tool
def lookup_policy(topic: str):
    """자료실 규정 한 가지를 찾아 알려 줍니다. topic에는 대출이나 운영을 넣습니다."""
    return rules[topic]


# 이 줄은 아래 함수를 서버의 도구로 등록하면서, 범위 admin이 있는 접근 토큰에게만 보이게 합니다
@mcp.tool(auth=require_scopes("admin"))
def update_policy(topic: str, text: str):
    """자료실 규정 한 가지의 글을 새 글로 바꿉니다."""
    rules[topic] = text
    return "규정을 바꿨습니다: " + topic


if __name__ == "__main__":
    # 파일을 직접 실행할 때만: 명령 줄의 첫 인자를 포트 번호로 읽어, 이 컴퓨터 안의 주소에서 HTTP 서버를 엽니다
    port = int(sys.argv[1])
    mcp.run(transport="http", host="127.0.0.1", port=port, show_banner=False)
