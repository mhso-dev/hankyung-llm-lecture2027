import { streamChat } from "./stream.ts";

async function main() {
  const normal = [];
  for await (const event of streamChat("재연결 확인 질문")) {
    if (event) normal.push(event);
  }
  const firstId = normal.find((event) => event.event === "token")?.id;
  if (firstId !== "web-01:0") throw new Error(`첫 id 불일치: ${firstId}`);
  if (normal.at(-1)?.event !== "done") throw new Error("done 이벤트가 없습니다");

  const resumed = [];
  for await (const event of streamChat("재연결 확인 질문", firstId)) {
    if (event) resumed.push(event);
  }
  if (resumed[0]?.id !== "web-01:1") throw new Error(`재개 id 불일치: ${resumed[0]?.id}`);

  const failed = [];
  for await (const event of streamChat("오류")) {
    if (event) failed.push(event);
  }
  if (failed[0]?.event !== "error") throw new Error("error 이벤트가 없습니다");

  console.log(JSON.stringify({
    normal: normal.map((event) => event.event),
    firstId,
    resumedFirstId: resumed[0]?.id,
    failed: failed.map((event) => event.event),
  }));
}

main();
