import {useMemo, useRef, useState} from 'react';
import type {StreamEvent} from 'lib/article-illustrator/types';
import type {ToolLog} from 'lib/article-illustrator/utils/logger';

type SSEPayload =
  | {type: 'event'; data: StreamEvent}
  | {type: 'log'; data: ToolLog};

function isLikelyHtml(text: string) {
  return /<\w+[\s>]/.test(text);
}

function escapeHtml(text: string) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function toHtml(input: string) {
  const trimmed = input.trim();
  if (!trimmed) return '';
  if (isLikelyHtml(trimmed)) return trimmed;
  const paragraphs = trimmed
    .split(/\n{2,}/)
    .map((block) =>
      `<p>${escapeHtml(block.trim()).replace(/\n/g, '<br/>')}</p>`
    )
    .join('');
  return `<article>${paragraphs}</article>`;
}

export default function IllustratePage() {
  const [input, setInput] = useState('');
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [logs, setLogs] = useState<ToolLog[]>([]);
  const [outputHtml, setOutputHtml] = useState('');
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const previewHtml = useMemo(() => {
    if (outputHtml) return outputHtml;
    return '<div class="placeholder">等待输出…</div>';
  }, [outputHtml]);

  const runAgent = async () => {
    const html = toHtml(input);
    if (!html) {
      setError('请输入文本或 HTML');
      return;
    }

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setRunning(true);
    setError(null);
    setEvents([]);
    setLogs([]);
    setOutputHtml('');

    try {
      const response = await fetch('/api/illustrate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({html, includeLogs: true}),
        signal: controller.signal,
      });

      if (!response.ok || !response.body) {
        throw new Error(`请求失败: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';

      while (true) {
        const {value, done} = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, {stream: true});

        const parts = buffer.split(/\n\n/);
        buffer = parts.pop() || '';

        for (const part of parts) {
          const lines = part.split(/\n/);
          const dataLines = lines
            .filter((line) => line.startsWith('data: '))
            .map((line) => line.slice(6));
          if (dataLines.length === 0) continue;

          const payloadText = dataLines.join('\n');
          let payload: SSEPayload | null = null;
          try {
            payload = JSON.parse(payloadText) as SSEPayload;
          } catch {
            continue;
          }

          if (payload.type === 'log') {
            setLogs((prev) => [...prev, payload.data]);
            continue;
          }

          setEvents((prev) => [...prev, payload.data]);
          if (payload.data.type === 'complete' && payload.data.html) {
            setOutputHtml(payload.data.html);
          }
          if (payload.data.type === 'error' && payload.data.error) {
            setError(payload.data.error);
          }
        }
      }
    } catch (err) {
      if ((err as Error).name === 'AbortError') return;
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="page">
      <header className="header">
        <div className="title">Article Illustrator</div>
        <div className="subtitle">粘贴文本 → 运行 → 右侧实时渲染</div>
      </header>

      <section className="main">
        <div className="panel left">
          <div className="panel-title">输入文本 / HTML</div>
          <textarea
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="粘贴文章文本或 HTML…"
          />
          <button className="button" onClick={runAgent} disabled={running}>
            {running ? '运行中…' : '运行'}
          </button>
          {error && <div className="error">{error}</div>}
        </div>

        <div className="panel right">
          <div className="panel-title">输出预览（流式）</div>
          <div className="events">
            {events.length === 0 && (
              <div className="event-muted">等待事件…</div>
            )}
            {events.map((event, index) => (
              <div key={`${event.type}-${index}`} className="event">
                <span className="event-type">{event.type}</span>
                <span className="event-message">{event.message || ''}</span>
              </div>
            ))}
          </div>
          <div
            className="preview"
            dangerouslySetInnerHTML={{__html: previewHtml}}
          />
        </div>
      </section>

      <section className="logs">
        <div className="panel-title">完整日志</div>
        <pre className="log-output">
          {logs.map((log, index) => {
            const entry = {
              ...log,
              data: log.data,
            };
            return (
              JSON.stringify(entry, null, 2) +
              (index === logs.length - 1 ? '' : '\n\n')
            );
          })}
        </pre>
      </section>

      <style jsx>{`
        .page {
          min-height: 100vh;
          padding: 24px;
          background: #f5f7fb;
          color: #0f172a;
        }
        .header {
          margin-bottom: 16px;
        }
        .title {
          font-size: 20px;
          font-weight: 700;
        }
        .subtitle {
          color: #64748b;
          margin-top: 4px;
        }
        .main {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
          margin-bottom: 16px;
        }
        .panel {
          background: #ffffff;
          border-radius: 12px;
          box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08);
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 12px;
          min-height: 420px;
        }
        .panel-title {
          font-weight: 600;
          color: #1e293b;
        }
        .input {
          flex: 1;
          width: 100%;
          resize: vertical;
          min-height: 240px;
          padding: 12px;
          border-radius: 10px;
          border: 1px solid #dce3f0;
          font-size: 14px;
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
            'Liberation Mono', 'Courier New', monospace;
        }
        .button {
          align-self: flex-start;
          background: #2563eb;
          color: #ffffff;
          padding: 10px 18px;
          border-radius: 10px;
          border: none;
          font-weight: 600;
          cursor: pointer;
        }
        .button:disabled {
          background: #93c5fd;
          cursor: not-allowed;
        }
        .error {
          color: #dc2626;
          background: #fee2e2;
          padding: 8px 12px;
          border-radius: 8px;
        }
        .events {
          display: flex;
          flex-direction: column;
          gap: 6px;
          font-size: 13px;
        }
        .event {
          display: flex;
          gap: 8px;
          align-items: baseline;
        }
        .event-type {
          font-weight: 600;
          color: #0f172a;
          min-width: 110px;
        }
        .event-message {
          color: #334155;
        }
        .event-muted {
          color: #94a3b8;
        }
        .preview {
          flex: 1;
          border: 1px solid #e2e8f0;
          border-radius: 10px;
          padding: 12px;
          overflow: auto;
          background: #f8fafc;
        }
        .placeholder {
          color: #94a3b8;
        }
        .logs {
          background: #ffffff;
          border-radius: 12px;
          box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08);
          padding: 16px;
        }
        .log-output {
          white-space: pre-wrap;
          font-size: 12px;
          line-height: 1.5;
          background: #0b1120;
          color: #e2e8f0;
          padding: 12px;
          border-radius: 10px;
          max-height: 360px;
          overflow: auto;
        }
        @media (max-width: 960px) {
          .main {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}
