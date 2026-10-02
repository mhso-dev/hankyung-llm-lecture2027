# 2026-09-29 Ch 30 01절 품질 개선: 이 파일은 Ch 30~34 노트북을 옛 마감 글로 고치는 보조 스크립트입니다.
# Ch 30 개선본은 textbook/part7/ch30-fastapi-serving/qa/upgrade/author_NN.py가 씁니다. 이 파일을 실행하면 개선본을 옛 글로 덮어쓰므로, 아래 줄에서 실행을 막습니다.
# 내용은 고치지 않았습니다(이 설명 세 줄과 아래 한 줄만 더함). 옮기거나 지울지는 사용자·강사가 정합니다.
raise SystemExit('옛 Part 7 보조 스크립트(part7_final_repairs.py)입니다. 실행하면 Ch 30 개선본을 옛 글로 덮어씁니다. 개선본은 각 챕터 qa/upgrade/author_NN.py를 쓰세요.')
from pathlib import Path
import json

def notebook(ch, prefix):
    path = next((Path('labs/part7') / ch / 'notebooks').glob(prefix + '-*'))
    return path, json.loads(path.read_text())

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')

p, n = notebook('ch30-fastapi-serving', '09')
n['cells'][5]['source'] = ['### API 연결에 필요한 환경 변수 확인\n\n`find_dotenv(usecwd=True)`는 현재 폴더부터 상위 폴더에서 `.env`를 찾고, `load_dotenv()`는 환경 변수를 읽습니다. `os.getenv()`로 키 설정 여부를 읽고 `bool()`로 참·거짓만 출력합니다. `assert has_key`는 키가 없으면 중단합니다. 이 셀은 모델이나 HTTP 경로를 호출하지 않습니다.\n']
notes = {
    7: '`TestClient(app)`는 같은 프로세스 안에서 FastAPI 요청 처리를 시험하는 클라이언트입니다. `post()`에 경로, 인증 헤더, JSON 본문을 넘기면 해당 경로가 실행됩니다. `/v1/chat/live`의 내부 Agent는 실제 모델을 호출하므로 외부 모델 API 연결이 필요합니다. 반환된 HTTP 상태 코드와 답 문자열을 함께 확인합니다.',
    9: '`build_live_agent()`는 호출 객체를 준비하고 `await live_agent.ainvoke(...)`가 별도의 실제 실행을 시작합니다. `tool_calls`에는 모델이 요청한 도구 이름과 인수가 있고, `ToolMessage`에는 실행한 도구의 결과가 있습니다. 앞 HTTP 호출의 저장 궤적을 읽는 셀이 아니라 같은 질문으로 별도 실행한 궤적을 확인하는 셀입니다.',
    11: 'SSE는 이벤트 이름과 데이터를 텍스트 블록으로 보내는 형식입니다. 아래에서는 `event: token` 블록을 고르고 `data:` 뒤의 JSON을 읽어 `token` 문자열을 연결합니다. TestClient에서 완성된 응답을 받아 해석하므로 화면에 조각이 실시간으로 보이는 지연을 측정하지 않습니다.',
}
for i, note in notes.items():
    old = ''.join(n['cells'][i]['source'])
    if note not in old:
        n['cells'][i]['source'] = (old + '\n\n' + note + '\n').splitlines(keepends=True)
save(p, n)

p = next(Path('textbook/part7/ch33-cicd/_src').glob('04-*'))
s = p.read_text().replace('오류율과 p95 지연을 각 시간 구간에서 계산할 수 있습니다.', '각 시간 구간의 오류율을 계산하고 제공된 p95 지연과 함께 경보 조건을 판정할 수 있습니다.')
s = s.replace('오류율과 p95 지연을 계산하고,', '오류율을 계산하고 이미 집계된 p95 지연을 읽어,')
s = s.replace('예제는 각 분의 두 값을 계산한 뒤', '예제는 각 분의 오류율을 계산하고 자료에 저장된 p95 지연을 읽은 뒤')
s = s.replace('4분의 고정 메트릭을 읽고 각 분의 오류율을 계산합니다.', '4분의 고정 메트릭을 읽고 각 분의 오류율을 계산합니다. p95 지연은 자료에 미리 집계된 값을 사용하며 원시 요청 시간으로 다시 계산하지 않습니다.')
p.write_text(s)
p, n = notebook('ch33-cicd', '04')
s = ''.join(n['cells'][3]['source']).replace('예제는 각 분의 두 값을 계산한 뒤', '예제는 각 분의 오류율을 계산하고 자료에 저장된 p95 지연을 읽은 뒤')
n['cells'][3]['source'] = s.splitlines(keepends=True)
save(p, n)

boundary = '이 실습의 v1과 v2 식별자는 고정 문자열 stable-v1과 regressed-v2를 SHA-256으로 해시해 만든 모의 값입니다. 실제 Docker 이미지 ID나 레지스트리 다이제스트를 조회한 값이 아닙니다. 기록의 digest 필드에는 이 모의 값을 넣어 롤백 이력 형식과 상태 전환을 확인합니다. 운영에서는 앞 절에서 확인한 실제 이미지 식별자를 전달해야 합니다.'
p = next(Path('textbook/part7/ch33-cicd/_src').glob('05-*'))
s = p.read_text().replace('이 절은 그 신호와 기록을 연결해 이전 결과물을 선택하고, 선택 뒤 서비스 응답을 다시 확인합니다.', '이 절은 그 판단 방식과 기록 형식을 참고하여 별도의 모의 식별자로 복구 절차를 실행합니다. 앞 절의 실제 이미지 ID 기록을 읽는 실습은 아닙니다.')
s = s.replace('이 실습은 두 다이제스트의 로컬 이력과 경보 종료 코드를 연결합니다.', boundary)
s = s.replace('안정 버전 v1과 회귀가 있는 버전 v2의 다이제스트를 차례로 로컬 이력에 배포합니다.', '안정 버전 v1과 회귀가 있는 버전 v2의 모의 식별자를 차례로 로컬 배포 이력에 기록합니다.')
p.write_text(s)
p, n = notebook('ch33-cicd', '05')
s = ''.join(n['cells'][0]['source']).replace('두 리비전을 배포한 뒤 경보를 근거로 이전 다이제스트를 다시 활성화합니다.', '두 리비전의 모의 배포를 기록한 뒤 경보를 근거로 이전 식별자를 다시 활성화합니다.')
n['cells'][0]['source'] = (s + '\n\n' + boundary + '\n').splitlines(keepends=True)
for i in (3, 7):
    s = ''.join(n['cells'][i]['source']).replace('다이제스트', '모의 식별자')
    n['cells'][i]['source'] = s.splitlines(keepends=True)
save(p, n)
print('Part7 final notebook and observation boundaries repaired')
