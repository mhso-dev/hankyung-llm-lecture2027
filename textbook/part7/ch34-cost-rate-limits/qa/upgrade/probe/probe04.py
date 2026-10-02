import os, socket, subprocess, sys, time, json
import httpx
from langchain.chat_models import init_chat_model
from langchain_core.exceptions import ModelRateLimitError
from langchain_core.runnables import RunnableLambda
assert "OPENAI_API_KEY" not in os.environ
port = int(sys.argv[1])
here = os.path.dirname(os.path.abspath(__file__))
def is_open(p):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", p)) == 0
assert not is_open(port)
proc = subprocess.Popen([sys.executable, os.path.join(here, "always_429_server.py"), str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for i in range(100):
    if is_open(port): break
    time.sleep(0.05)
alive = proc.poll() is None
root = "http://127.0.0.1:" + str(port)
base_url = root + "/v1"
res = {"alive": alive}
def reset():
    r = httpx.post(base_url + "/reset")
    return r.status_code, r.headers["practice-count"]
res["reset"] = reset()
default_model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", base_url=base_url, api_key="not-a-real-key")
zero_model = init_chat_model("openai:gpt-5.4-mini", temperature=0, reasoning_effort="none", base_url=base_url, api_key="not-a-real-key", max_retries=0)
res["max_retries"] = [default_model.max_retries, default_model.root_client.max_retries, zero_model.max_retries, zero_model.root_client.max_retries]
def run(runnable, label):
    reset()
    t = time.perf_counter()
    try:
        runnable.invoke("q")
        name = None
    except ModelRateLimitError as error:
        name = type(error).__name__
        cnt = error.response.headers["practice-count"]
        res[label + "_status"] = error.response.status_code
        res[label + "_str"] = str(error)
        res[label + "_mro"] = [c.__name__ for c in type(error).__mro__][:6]
    res[label] = (name, cnt, round(time.perf_counter() - t, 2))
run(default_model, "default")
run(zero_model, "zero")
before = default_model.with_retry(retry_if_exception_type=(ModelRateLimitError,), stop_after_attempt=3)
after = zero_model.with_retry(retry_if_exception_type=(ModelRateLimitError,), stop_after_attempt=3)
res["retry_type"] = type(before).__name__
run(before, "before")
run(after, "after")
active = []; peaks = []; received = []
def ask_and_count(text):
    active.append(text)
    peaks.append(len(active))
    try:
        after.invoke(text)
    except ModelRateLimitError as error:
        received.append(type(error).__name__)
    active.remove(text)
inputs = ["문의 1", "문의 2", "문의 3", "문의 4", "문의 5", "문의 6"]
counter = RunnableLambda(ask_and_count)
for label, cfg in (("batch_none", None), ("batch_2", {"max_concurrency": 2})):
    reset(); active.clear(); peaks.clear(); received.clear()
    t = time.perf_counter()
    out = counter.batch(inputs, config=cfg)
    cnt = httpx.post(root + "/count-peek").headers["practice-count"]  # counts itself
    res[label] = (max(peaks), int(cnt) - 1, len(received), received[:1], out, round(time.perf_counter()-t, 2))
proc.terminate()
res["rc"] = proc.wait(timeout=10)
res["open_after"] = is_open(port)
print(json.dumps(res, ensure_ascii=False))
