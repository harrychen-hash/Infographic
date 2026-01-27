/**
 * Logger for Article Illustrator
 * 记录每个 Tool 的输入、输出和执行时间
 */

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface ToolLog {
  timestamp: string;
  tool: string;
  phase: 'input' | 'output' | 'error';
  duration?: number; // ms
  data: unknown;
}

export interface RunLog {
  runId: string;
  startTime: string;
  endTime?: string;
  status: 'running' | 'completed' | 'failed';
  logs: ToolLog[];
}

// Store logs in memory (can be extended to file/database)
const runLogs: Map<string, RunLog> = new Map();
let currentRunId: string | null = null;

// Callback for real-time log streaming
type LogCallback = (log: ToolLog) => void;
let logCallback: LogCallback | null = null;

/**
 * Set callback for real-time log streaming
 */
export function setLogCallback(callback: LogCallback | null) {
  logCallback = callback;
}

/**
 * Start a new run
 */
export function startRun(): string {
  const runId = `run-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  currentRunId = runId;

  runLogs.set(runId, {
    runId,
    startTime: new Date().toISOString(),
    status: 'running',
    logs: [],
  });

  console.log(`\n${'='.repeat(60)}`);
  console.log(`🚀 [ArticleIllustrator] Run started: ${runId}`);
  console.log(`${'='.repeat(60)}\n`);

  return runId;
}

/**
 * End the current run
 */
export function endRun(success: boolean) {
  if (!currentRunId) return;

  const run = runLogs.get(currentRunId);
  if (run) {
    run.endTime = new Date().toISOString();
    run.status = success ? 'completed' : 'failed';

    const duration = new Date(run.endTime).getTime() - new Date(run.startTime).getTime();

    console.log(`\n${'='.repeat(60)}`);
    console.log(`${success ? '✅' : '❌'} [ArticleIllustrator] Run ${success ? 'completed' : 'failed'}`);
    console.log(`   Duration: ${(duration / 1000).toFixed(2)}s`);
    console.log(`   Total logs: ${run.logs.length}`);
    console.log(`${'='.repeat(60)}\n`);
  }

  currentRunId = null;
}

/**
 * Log tool input
 */
export function logToolInput(tool: string, data: unknown): number {
  const startTime = Date.now();
  const log: ToolLog = {
    timestamp: new Date().toISOString(),
    tool,
    phase: 'input',
    data: truncateData(data),
  };

  addLog(log);

  console.log(`\n📥 [${tool}] INPUT`);
  console.log(`   ${formatData(data)}`);

  return startTime;
}

/**
 * Log tool output
 */
export function logToolOutput(tool: string, data: unknown, startTime: number) {
  const duration = Date.now() - startTime;
  const log: ToolLog = {
    timestamp: new Date().toISOString(),
    tool,
    phase: 'output',
    duration,
    data: truncateData(data),
  };

  addLog(log);

  console.log(`\n📤 [${tool}] OUTPUT (${duration}ms)`);
  console.log(`   ${formatData(data)}`);
}

/**
 * Log tool error
 */
export function logToolError(tool: string, error: unknown, startTime?: number) {
  const duration = startTime ? Date.now() - startTime : undefined;
  const log: ToolLog = {
    timestamp: new Date().toISOString(),
    tool,
    phase: 'error',
    duration,
    data: error instanceof Error ? error.message : String(error),
  };

  addLog(log);

  console.log(`\n❌ [${tool}] ERROR${duration ? ` (${duration}ms)` : ''}`);
  console.log(`   ${error instanceof Error ? error.message : String(error)}`);
}

/**
 * Get all logs for a run
 */
export function getRunLogs(runId: string): RunLog | undefined {
  return runLogs.get(runId);
}

/**
 * Get current run logs
 */
export function getCurrentRunLogs(): RunLog | undefined {
  return currentRunId ? runLogs.get(currentRunId) : undefined;
}

/**
 * Get all runs (for debugging)
 */
export function getAllRuns(): RunLog[] {
  return Array.from(runLogs.values()).slice(-10); // Keep last 10 runs
}

/**
 * Clear old logs (keep last N runs)
 */
export function clearOldLogs(keepCount = 10) {
  const runs = Array.from(runLogs.keys());
  if (runs.length > keepCount) {
    runs.slice(0, runs.length - keepCount).forEach((id) => runLogs.delete(id));
  }
}

// Helper functions

function addLog(log: ToolLog) {
  if (currentRunId) {
    const run = runLogs.get(currentRunId);
    if (run) {
      run.logs.push(log);
    }
  }

  // Stream to callback if set
  if (logCallback) {
    logCallback(log);
  }
}

const DEFAULT_LOG_MAX_LENGTH = 20000;

function getLogMaxLength(): number {
  const raw = process.env.ARTICLE_ILLUSTRATOR_LOG_MAX_LENGTH;
  if (!raw) return DEFAULT_LOG_MAX_LENGTH;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : DEFAULT_LOG_MAX_LENGTH;
}

function truncateData(data: unknown, maxLength = getLogMaxLength()): unknown {
  const str = JSON.stringify(data);
  if (str.length <= maxLength) {
    return data;
  }

  // Return truncated version
  if (typeof data === 'string') {
    return data.slice(0, maxLength) + '... [truncated]';
  }

  if (typeof data === 'object' && data !== null) {
    return {
      _truncated: true,
      _originalLength: str.length,
      preview: str.slice(0, maxLength) + '...',
    };
  }

  return data;
}

function formatData(data: unknown): string {
  if (typeof data === 'string') {
    const lines = data.split('\n');
    if (lines.length > 5) {
      return lines.slice(0, 5).join('\n   ') + `\n   ... (${lines.length - 5} more lines)`;
    }
    return data.length > 200 ? data.slice(0, 200) + '...' : data;
  }

  const str = JSON.stringify(data, null, 2);
  const lines = str.split('\n');
  if (lines.length > 10) {
    return lines.slice(0, 10).join('\n   ') + `\n   ... (${lines.length - 10} more lines)`;
  }
  return str;
}
