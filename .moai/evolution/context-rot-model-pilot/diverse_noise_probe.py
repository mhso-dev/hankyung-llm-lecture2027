"""Exploratory comparison; preserve every run, including no-degradation results."""
from pathlib import Path
import hashlib
import json
import random
import re
from datetime import datetime, timezone
from dotenv import load_dotenv
import tiktoken
from langchain.chat_models import init_chat_model

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')
encoder = tiktoken.get_encoding('cl100k_base')
question = '미르시립도서관의 B-742 모임에 적용되는 최대 대출 기간은 며칠인가요? 기간을 숫자와 일로 쓰고, 연결에 사용한 모임·공간·규정 코드를 모두 제시하세요.'
instruction = '제공한 자료만 근거로 답하세요. 관련 코드가 정확히 일치하는 문서를 연결하세요. 근거가 없으면 모른다고 답하세요.'
evidence = [
    '[모임 안내 B-742] 미르시립도서관 B-742 모임의 지정 공간은 R-518입니다. 지정 공간의 대출 규정을 따릅니다.',
    '[공간 운영 R-518] R-518 공간에 적용되는 대출 규정은 P-361입니다. 다른 공간의 규정은 적용하지 않습니다.',
    '[대출 규정 P-361] P-361을 적용하는 모임의 최대 대출 기간은 17일입니다. 대출 기간 연장은 제공하지 않습니다.',
]
rng = random.Random(20260909)
names = ['별빛', '푸른', '한빛', '누리', '새봄', '가람', '미르', '한울']
subjects = ['독서 토론', '글쓰기', '어린이 동화', '지역 역사', '외국어 읽기', '과학 독서', '시 낭독']
# Unique identifiers keep all distractor facts compatible with the target chain.
noise = []
for i in range(500):
    branch = f'{names[i % len(names)]}분관'
    days = rng.choice([3, 5, 7, 10, 14, 21, 28])
    room = 1000 + i
    meeting = 2000 + i
    policy = 3000 + i
    noise.append([
        f'[행사 공지 B-{meeting}] {branch}의 {subjects[i % len(subjects)]} 모임은 R-{room}에서 진행합니다. 신청은 매월 {i % 25 + 1}일까지이며 준비물은 필기구입니다.',
        f'[공간 안내 R-{room}] {branch} R-{room}의 수용 인원은 {i % 30 + 8}명입니다. 이 공간은 P-{policy} 규정을 따르며 야간 이용은 사전 예약이 필요합니다.',
        f'[이용 규정 P-{policy}] {branch}의 P-{policy} 대출 기간은 {days}일입니다. 예약 취소는 시작 {i % 4 + 1}시간 전까지 가능합니다. 자료 반납함은 1층 안내데스크 옆에 있습니다.',
        f'[운영 메모 N-{i}] {branch}는 {i % 12 + 1}월에 서가 점검을 실시합니다. 문의는 안내데스크에서 접수하며 우천 시 야외 프로그램은 실내로 이동합니다.',
    ][i % 4])

def prompt_for(count):
    selected = noise[:count]
    chunks = [selected[i * count // 4:(i + 1) * count // 4] for i in range(4)]
    docs = []
    for i, chunk in enumerate(chunks):
        docs.extend(chunk)
        if i < 3:
            docs.append(evidence[i])
    context = '\n\n'.join(docs)
    return f'자료:\n{context}\n\n질문: {question}'

# Fix the three sizes before any model call. No adapting to whether answers fail.
counts = {}
for label, cap in [('short', 700), ('medium', 4500), ('long', 12000)]:
    count = 0
    while count < len(noise) and len(encoder.encode(instruction + prompt_for(count + 1))) <= cap:
        count += 1
    counts[label] = count
prompts = {label: prompt_for(count) for label, count in counts.items()}
for prompt in prompts.values():
    assert all(prompt.count(doc) == 1 for doc in evidence)
    assert len(encoder.encode(instruction + prompt)) + 350 < 16385
manifest = {
    'date': datetime.now(timezone.utc).isoformat(),
    'seed': 20260909,
    'question': question,
    'instruction': instruction,
    'evidence': evidence,
    'noise_counts': counts,
    'local_cl100k_tokens': {label: len(encoder.encode(instruction + prompt)) for label, prompt in prompts.items()},
    'prompts': prompts,
    'prompt_sha256': {label: hashlib.sha256(prompt.encode()).hexdigest() for label, prompt in prompts.items()},
    'models': ['gpt-3.5-turbo', 'gpt-4.1-nano'],
    'repetitions': 3,
    'temperature': 0,
    'max_tokens': 300,
}
(HERE / 'diverse-noise-inputs.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print('Fixed conditions:', counts, manifest['local_cl100k_tokens'], flush=True)
output = HERE / 'diverse-noise-results.jsonl'
if output.exists():
    raise RuntimeError('Existing results must be preserved; choose a new run file')
with output.open('w') as stream:
    for model_name in manifest['models']:
        model = init_chat_model(f'openai:{model_name}', temperature=0, max_tokens=300, timeout=60, max_retries=1)
        for trial in range(1, 4):
            for label, prompt in prompts.items():
                try:
                    result = model.invoke([('system', instruction), ('user', prompt)])
                    answer = result.text
                    record = {'model': model_name, 'trial': trial, 'length': label,
                              'answer': answer, 'usage': result.usage_metadata,
                              'duration_answer': bool(re.search(r'(?<!\d)17\s*일', answer)),
                              'all_source_codes': all(code in answer for code in ['B-742', 'R-518', 'P-361']),
                              'finish_reason': result.response_metadata.get('finish_reason'),
                              'served_model': result.response_metadata.get('model_name'),
                              'prompt_sha256': manifest['prompt_sha256'][label]}
                except Exception as exc:
                    # Record type only; do not print provider error bodies or credentials.
                    record = {'model': model_name, 'trial': trial, 'length': label, 'error_type': type(exc).__name__}
                stream.write(json.dumps(record, ensure_ascii=False) + '\n')
                stream.flush()
                print(model_name, label, trial, record.get('duration_answer'), record.get('all_source_codes'), record.get('error_type', ''), flush=True)
