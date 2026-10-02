"""Ch28 학생용 읽기 전용 MCP 서버."""

from fastmcp import FastMCP


POLICIES = {
    "대출": "일반 도서는 1인 5권까지 14일 동안 대출할 수 있습니다.",
    "운영": "평일은 09:00~20:00, 토요일은 10:00~17:00에 운영합니다.",
    "연체": "연체한 일수만큼 새 대출이 제한됩니다.",
}

mcp = FastMCP(
    "교육센터 자료실",
    instructions="공개된 자료실 규정을 읽기 전용으로 제공합니다.",
)


@mcp.tool(tags={"public", "read"})
def lookup_policy(topic: str) -> str:
    """자료실 규정을 조회합니다. topic은 대출, 운영, 연체 중 하나입니다."""
    if topic not in POLICIES:
        raise ValueError("topic은 대출, 운영, 연체 중 하나여야 합니다.")
    return POLICIES[topic]


@mcp.resource("policy://handbook")
def policy_handbook() -> str:
    """공개된 자료실 규정 전체를 제공합니다."""
    return "\n".join(f"{topic}: {text}" for topic, text in POLICIES.items())


@mcp.prompt
def explain_policy(topic: str) -> str:
    """선택한 규정을 초보자에게 설명하는 요청문을 만듭니다."""
    return f"{topic} 규정을 근거 문장과 함께 두 문장으로 설명해 주세요."


if __name__ == "__main__":
    mcp.run(transport="stdio")
