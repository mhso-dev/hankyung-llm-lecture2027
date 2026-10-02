type SseEvent = { event: string; id?: string; data: unknown };

function decodeBlock(block: string): SseEvent | null {
  const lines = block.split("\n");
  const event = lines.find((line) => line.startsWith("event:"))?.slice(6).trim();
  const id = lines.find((line) => line.startsWith("id:"))?.slice(3).trim();
  const data = lines.find((line) => line.startsWith("data:"))?.slice(5).trim();
  return event && data ? { event, id, data: JSON.parse(data) } : null;
}

export async function* streamChat(question: string, lastEventId?: string) {
  const headers: Record<string, string> = {
    Authorization: "Bearer local-demo-token",
    "Content-Type": "application/json",
  };
  if (lastEventId) headers["Last-Event-ID"] = lastEventId;
  const response = await fetch("http://127.0.0.1:8000/v1/chat/stream", {
    method: "POST",
    headers,
    body: JSON.stringify({ question, thread_id: "web-01" }),
  });
  if (!response.ok || !response.body) throw new Error(`HTTP ${response.status}`);
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    buffer += value ?? "";
    const blocks = buffer.split(/\r?\n\r?\n/);
    buffer = blocks.pop() ?? "";
    for (const block of blocks) yield decodeBlock(block);
    if (done) {
      const finalEvent = decodeBlock(buffer.trim());
      if (finalEvent) yield finalEvent;
      break;
    }
  }
}
