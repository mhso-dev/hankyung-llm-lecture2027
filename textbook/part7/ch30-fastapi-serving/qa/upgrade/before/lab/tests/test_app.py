from fastapi.testclient import TestClient

from agent_service.app import app


client = TestClient(app)
AUTH = {"Authorization": "Bearer local-demo-token"}


def test_health_and_validation() -> None:
    assert client.get("/health").json() == {"status": "ok"}
    response = client.post("/v1/chat", headers=AUTH, json={"question": "", "thread_id": "x"})
    assert response.status_code == 422


def test_chat_calls_agent() -> None:
    response = client.post(
        "/v1/chat", headers=AUTH, json={"question": "안녕하세요", "thread_id": "t-1"}
    )
    assert response.status_code == 200
    assert response.json()["answer"] == "질문을 확인했습니다: 안녕하세요"


def test_auth_and_cors() -> None:
    assert client.post("/v1/chat", json={"question": "a", "thread_id": "t"}).status_code == 401
    response = client.options(
        "/v1/chat",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"},
    )
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_stream_done_and_error_events() -> None:
    ok = client.post(
        "/v1/chat/stream", headers=AUTH, json={"question": "두 단어", "thread_id": "s-1"}
    )
    assert "event: token" in ok.text and "event: done" in ok.text
    failed = client.post(
        "/v1/chat/stream", headers=AUTH, json={"question": "오류", "thread_id": "s-2"}
    )
    assert failed.status_code == 200
    assert "event: error" in failed.text and "stream_failed" in failed.text
    assert "교육용 스트림 오류" not in failed.text


def test_invalid_last_event_id_is_rejected_before_stream() -> None:
    response = client.post(
        "/v1/chat/stream",
        headers={**AUTH, "Last-Event-ID": "s-1:not-a-number"},
        json={"question": "질문", "thread_id": "s-1"},
    )
    assert response.status_code == 400


def test_openapi_contract() -> None:
    schema = client.get("/openapi.json").json()
    assert schema["info"]["version"] == "1.0.0"
    assert "/v1/chat" in schema["paths"]
