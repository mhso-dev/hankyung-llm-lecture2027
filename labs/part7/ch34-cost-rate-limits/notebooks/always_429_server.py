"""Ch 34 04절 연습용 서버 — 어떤 요청이 와도 상태 코드 429(요청 제한)만 보냅니다.

실제 제공자의 요청 제한을 흉내 내는 연습용 서버입니다. 모델의 답은 한 번도 보내지 않습니다.
주소 끝이 /chat/completions인 요청(모델에 보내는 요청)만 세어, 응답 머리 practice-count에 센 수를 적습니다.
주소 끝이 /reset인 요청을 받으면 센 수를 0으로 맞춥니다. 주소 끝이 /count인 요청은 세지 않고, 센 수만 알려 줍니다.
노트북 04절이 이 파일을 자식 프로세스로 띄우고, 마지막 셀에서 끕니다.
"""
import sys
from wsgiref.simple_server import make_server

# 모든 응답에 보낼 오류 글입니다(OpenAI 오류 글과 같은 모양의 JSON입니다)
error_text = '{"error": {"message": "연습용 서버는 늘 429를 보냅니다.", "code": "practice_429"}}'
error_body = error_text.encode("utf-8")
json_type = ("content-type", "application/json")

# 모델에 보내는 요청을 받을 때마다 그 주소를 한 줄씩 모읍니다(목록의 길이가 센 수입니다)
request_log = []


# 요청 하나를 받아 수를 세고, 센 수를 머리에 적어 상태 코드 429와 오류 글을 보냅니다(wsgiref가 요청마다 부릅니다)
def app(environ, start_response):
    path = environ["PATH_INFO"]
    if path.endswith("/reset"):
        request_log.clear()
    if path.endswith("/chat/completions"):
        request_log.append(path)
    headers = [json_type, ("practice-count", str(len(request_log)))]
    start_response("429 Too Many Requests", headers)
    return [error_body]


if __name__ == "__main__":
    # 파일을 직접 실행할 때만: 명령 줄의 첫 인자를 포트 번호로 읽어, 이 컴퓨터 안의 주소에서만 요청을 받습니다
    port = int(sys.argv[1])
    server = make_server("127.0.0.1", port, app)
    server.serve_forever()
