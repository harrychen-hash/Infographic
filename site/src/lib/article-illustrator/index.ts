/**
 * Article Illustrator - Main Workflow Entry
 * Agentic Workflow: 3 Tools + Guardrail
 */

import type {
  SegmentPlan,
  ProcessResult,
  StreamEvent,
  FailureReason,
} from './types';
import { segmentAndExtract } from './tools/segment-and-extract';
import { selectTemplate } from './tools/select-template';
import { renderInfographicViaTool } from './tools/render-infographic';
import { validateInfographic } from './guardrails/validate-infographic';
import { insertSvgAfter, getInfographicStyles } from './utils/html-utils';
import {
  startRun,
  endRun,
  setLogCallback,
  getCurrentRunLogs,
  type ToolLog,
} from './utils/logger';

const MAX_RETRIES = 3;

/**
 * Main entry point: Illustrate an article with infographics
 * @param html - The article HTML content
 * @param onEvent - Callback for streaming events
 * @param onLog - Callback for detailed tool logs
 * @returns Updated HTML with embedded infographics
 */
export async function illustrateArticle(
  html: string,
  onEvent?: (event: StreamEvent) => void,
  onLog?: (log: ToolLog) => void
): Promise<string> {
  const emit = (event: StreamEvent) => {
    onEvent?.(event);
  };

  // Start a new run and set up log streaming
  const runId = startRun();
  if (onLog) {
    setLogCallback(onLog);
  }

  try {
    // Step 1: [LLM] Segment and extract data from article
    emit({ type: 'segmenting', message: '正在分析文章结构...' });

    const segments = await segmentAndExtract(html);

    emit({
      type: 'segments_ready',
      message: `发现 ${segments.length} 个可配图段落`,
      segments,
    });

    // Filter segments suitable for infographic
    const suitableSegments = segments.filter((s) => s.suitableForInfographic);

    if (suitableSegments.length === 0) {
      emit({
        type: 'complete',
        message: '没有找到适合配图的段落',
        html,
      });
      return html;
    }

    // Step 2: Process each segment in parallel
    const results = await Promise.all(
      suitableSegments.map((segment) =>
        processSegmentWithRetry(segment, emit)
      )
    );

    // Step 3: Merge successful SVGs into HTML
    let finalHtml = html;
    let insertedCount = 0;

    // Sort by selector to insert in order (bottom-up to preserve positions)
    const successfulResults = results
      .filter((r): r is ProcessResult & { svg: string } => r.success && !!r.svg)
      .reverse(); // Reverse to insert from bottom to top

    for (const result of successfulResults) {
      finalHtml = insertSvgAfter(finalHtml, result.selector, result.svg);
      insertedCount++;
    }

    // Add styles if any infographics were inserted
    if (insertedCount > 0) {
      finalHtml = getInfographicStyles() + finalHtml;
    }

    emit({
      type: 'complete',
      message: `成功生成 ${insertedCount} 个信息图`,
      html: finalHtml,
    });

    // End run successfully
    endRun(true);
    setLogCallback(null);

    return finalHtml;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    emit({
      type: 'error',
      message: '处理失败',
      error: errorMessage,
    });

    // End run with failure
    endRun(false);
    setLogCallback(null);

    throw error;
  }
}

/**
 * Get logs from the current or previous run
 */
export function getRunLogs() {
  return getCurrentRunLogs();
}

/**
 * Process a single segment with retry mechanism
 */
async function processSegmentWithRetry(
  segment: SegmentPlan,
  emit: (event: StreamEvent) => void
): Promise<ProcessResult> {
  const triedTemplates: string[] = [];

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    emit({
      type: 'generating',
      message: `正在为"${segment.contentSummary}"生成图表 (尝试 ${attempt}/${MAX_RETRIES})`,
      segmentId: segment.id,
      attempt,
    });

    try {
      // [LLM] Tool 2: Select template and generate syntax
      const selection = await selectTemplate({
        segment,
        triedTemplates,
      });

      triedTemplates.push(selection.template);

      // [Deterministic] Tool 3: Render infographic
      const renderResult = await renderInfographicViaTool(selection.syntax);

      if (!renderResult.success) {
        emit({
          type: 'render_failed',
          message: `渲染失败: ${renderResult.error}`,
          segmentId: segment.id,
          error: renderResult.error,
          attempt,
        });
        continue; // Try next template
      }

      // [Guardrail] Validate the generated infographic
      const validation = await validateInfographic(
        segment,
        selection.template,
        selection.syntax
      );

      if (validation.passed) {
        emit({
          type: 'success',
          message: `成功生成 ${selection.template}`,
          segmentId: segment.id,
          template: selection.template,
        });

        return {
          success: true,
          svg: renderResult.svg,
          selector: segment.insertAfterSelector,
          segmentId: segment.id,
          template: selection.template,
        };
      }

      // Validation failed
      emit({
        type: 'validation_failed',
        message: `验证失败: ${validation.suggestion}`,
        segmentId: segment.id,
        reason: validation.failureReason as FailureReason,
        suggestion: validation.suggestion,
        template: selection.template,
        attempt,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      emit({
        type: 'render_failed',
        message: `处理出错: ${errorMessage}`,
        segmentId: segment.id,
        error: errorMessage,
        attempt,
      });
    }
  }

  // All retries exhausted
  emit({
    type: 'skipped',
    message: `跳过段落"${segment.contentSummary}"（${MAX_RETRIES}次尝试均失败）`,
    segmentId: segment.id,
  });

  return {
    success: false,
    selector: segment.insertAfterSelector,
    segmentId: segment.id,
  };
}

// Re-export types for convenience
export * from './types';
