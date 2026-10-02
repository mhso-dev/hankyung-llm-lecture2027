"""06절 「시드가 보장하는 범위」 확인 스크립트 (검토 1차 C-B2, 2026-09-16 저장).

노트북 06의 5·6절과 같은 계산(뽑기를 끈 답 1개 + temperature 0.3·1.0 × 시드 11·22·33·44·55 답 10개)을
노트북 밖에서 실행하고, 노트북에 저장된 출력과 글자 단위로 비교한다.
사용(실습 폴더 가상환경에서):
    python 06_seed_platform.py [노트북 경로]
torch 판만 바꿔 비교할 때는 같은 스크립트를 다른 가상환경(예: torch==2.5.1+cpu, transformers==4.56.2)에서 실행한다.
교재 기본 경로 코드가 아니므로 문법 사다리 대상이 아니다.
"""
import hashlib, json, platform, sys, warnings

warnings.filterwarnings("ignore", message="IProgress not found")
import torch, transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

transformers.logging.set_verbosity_error()
NAME, REV = "Qwen/Qwen2.5-0.5B-Instruct", "7ae557604adf67be50417f59c2c2f167def9a775"
tok = AutoTokenizer.from_pretrained(NAME, revision=REV)
model = AutoModelForCausalLM.from_pretrained(NAME, revision=REV)
request = "오프라인 서점의 가을 행사 이름을 한국어 5어절 이내로 하나 제안하세요."
text = tok.apply_chat_template([{"role": "user", "content": request}], tokenize=False, add_generation_prompt=True)
ids = tok.encode(text, return_tensors="pt")
n = len(ids[0])


def new_text(out):
    all_ids = out[0].tolist()
    return tok.decode(all_ids[n:len(all_ids)])


answers = [("greedy", new_text(model.generate(input_ids=ids, max_new_tokens=32, do_sample=False)))]
for temperature in [0.3, 1.0]:
    for seed in [11, 22, 33, 44, 55]:
        set_seed(seed)
        out = model.generate(input_ids=ids, max_new_tokens=32, do_sample=True, temperature=temperature, top_p=0.9)
        answers.append((f"{temperature}|{seed}", new_text(out)))

print("환경:", platform.machine(), platform.python_version(), "torch", torch.__version__, "transformers", transformers.__version__)
print("입력 토큰 수:", n)
for key, answer in answers:
    print(key, "|", answer.replace("\n", " "))
print("답 11개 sha256:", hashlib.sha256(json.dumps(answers, ensure_ascii=False).encode()).hexdigest()[:16])

if len(sys.argv) > 1:
    nb = json.load(open(sys.argv[1], encoding="utf-8"))
    printed = ""
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            for o in cell.get("outputs", []):
                t = o.get("text", "")
                printed += "".join(t) if isinstance(t, list) else t
    same = 0
    for key, answer in answers:
        line = answer.replace("\n", " ")
        if key == "greedy":
            hit = ("뽑기를 끈 답: " + answer) in printed
        else:
            temperature, seed = key.split("|")
            hit = f"{temperature} | {seed} | {line}" in printed
        same += hit
        if not hit:
            print("노트북과 다름:", key)
    print("노트북 출력과 같은 답 수:", same, "/", len(answers))
