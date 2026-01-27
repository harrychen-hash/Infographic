/**
 * Tool 1: segment_and_extract [LLM]
 * 按意图分段，提取数据，判断是否适合配图
 */

import OpenAI from 'openai';
import type { SegmentPlan, SegmentOutput } from '../types';
import { SEGMENT_SYSTEM_PROMPT } from '../prompts/segment-prompt';
import { TOOL_REGISTRY } from './registry';
import { getOpenAIKey, getOpenAIModel } from '../utils/env';
import { logToolInput, logToolOutput, logToolError } from '../utils/logger';
import { validateOrThrow } from '../utils/schema';

const TOOL_NAME = 'segment_and_extract';

// Lazy initialization to ensure env vars are loaded
let openaiClient: OpenAI | null = null;
function getOpenAI(): OpenAI {
  if (!openaiClient) {
    const apiKey = getOpenAIKey();
    console.log('[segment_and_extract] Initializing OpenAI with key:', apiKey?.substring(0, 10) + '...');
    openaiClient = new OpenAI({
      apiKey,
      // Node 20+ may expose navigator, which the SDK treats as browser-like
      dangerouslyAllowBrowser: true,
    });
  }
  return openaiClient;
}

export async function segmentAndExtract(html: string): Promise<SegmentPlan[]> {
  const requestPayload = {
    model: getOpenAIModel(),
    messages: [
      { role: 'system', content: SEGMENT_SYSTEM_PROMPT },
      { role: 'user', content: html },
    ],
    tools: [
      {
        type: 'function',
        function: {
          name: TOOL_REGISTRY.segment_and_extract.name,
          description: TOOL_REGISTRY.segment_and_extract.description,
          parameters: TOOL_REGISTRY.segment_and_extract.outputSchema.schema,
        },
      },
    ],
    tool_choice: {
      type: 'function',
      function: { name: TOOL_REGISTRY.segment_and_extract.name },
    },
    temperature: 0.3,
  };

  const startTime = logToolInput(TOOL_NAME, {
    htmlLength: html.length,
    htmlPreview: html.slice(0, 300) + (html.length > 300 ? '...' : ''),
    requestPayload,
  });

  try {
    const response = await getOpenAI().chat.completions.create(requestPayload);

    const toolCall = response.choices[0]?.message?.tool_calls?.[0];
    if (!toolCall || toolCall.function?.name !== TOOL_REGISTRY.segment_and_extract.name) {
      throw new Error('Missing tool call for segment_and_extract');
    }

    const args = toolCall.function.arguments
      ? JSON.parse(toolCall.function.arguments)
      : {};

    const result = validateOrThrow<SegmentOutput>(
      TOOL_REGISTRY.segment_and_extract.outputSchema.name,
      TOOL_REGISTRY.segment_and_extract.outputSchema.schema,
      args
    );
    const segments = result.segments || [];

    logToolOutput(
      TOOL_NAME,
      {
        responseRaw: response,
        toolCallRaw: toolCall,
        segmentCount: segments.length,
        suitableCount: segments.filter((s) => s.suitableForInfographic).length,
        segments: segments.map((s) => ({
          id: s.id,
          insertAfterSelector: s.insertAfterSelector,
          intent: s.intent,
          contentSummary: s.contentSummary,
          suitableForInfographic: s.suitableForInfographic,
          rejectionReason: s.rejectionReason,
          structuredData: s.structuredData,
          originalText: s.originalText,
        })),
      },
      startTime
    );

    return segments;
  } catch (error) {
    logToolError(TOOL_NAME, error, startTime);
    throw error;
  }
}
