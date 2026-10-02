"""Ch 34 04절 연습용 서버 — 어떤 요청이 와도 상태 코드 429(요청 제한)만 보냅니다.

실제 제공자의 요청 제한을 흉내 내는 연습용 서버입니다. 모델의 답은 한 번도 보내지 않습니다.
받은 요청 수를 세어, 응답 머리 practice-count에 적어 보냅니다.
주소 끝이 /reset인 요청은 세지 않고, 그때까지 센 수를 0으로 되돌립니다.
노트북 04절이 이 파일을 자식 프로세스로 띄우고, 마지막 셀에서 끕니다.
"""
import sys
from wsgiref.simple_server import make_server

# 서버가 보낼 오류 글입니다(OpenAI 오류 글과 같은 모양의 JSON)
error_text = '{"error": {"message": "연습용 서버는 늘 429를 보냅니다.", "type": "requests", "code": "rate_limit_exceeded"}}'
error_body = error_text.encode("utf-8")

# 받은 요청의 주소를 한 줄씩 모읍니다(목록의 길이가 받은 요청 수입니다)
request_log = []


# 요청 하나를 받아, 센 수를 머리에 적고 상태 코드 429와 오류 글을 보냅니다
def app(environ, start_response):
    path = environ["PATH_INFO"]
    if path.endswith("/reset"):
        request_log.clear()
    else:
        request_log.append(path)
    headers = [("content-type", "application/json"), ("practice-count", str(len(request_log)))]
    start_response("429 Too Many Requests", headers)
    return [error_body]


if __name__ == "__main__":
    # 파일을 직접 실행할 때만: 명령 줄의 첫 인자를 포트 번호로 읽어, 이 컴퓨터 안의 주소에서만 요청을 받습니다
    port = int(sys.argv[1])
    server = make_server("127.0.0.1", port, app)
    server.serve_forever()
