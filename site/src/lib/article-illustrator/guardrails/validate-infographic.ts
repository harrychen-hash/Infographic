/**
 * Guardrail: validate_infographic
 * 验证生成的图表是否符合要求
 */

import OpenAI from 'openai';
import type { SegmentPlan, ValidateOutput } from '../types';
import { VALIDATE_SYSTEM_PROMPT } from '../prompts/validate-prompt';
import { TOOL_REGISTRY } from '../tools/registry';
import { getOpenAIKey, getOpenAIModel } from '../utils/env';
import { logToolInput, logToolOutput, logToolError } from '../utils/logger';
import { validateOrThrow } from '../utils/schema';

const TOOL_NAME = 'validate_infographic';

// Lazy initialization to ensure env vars are loaded
let openaiClient: OpenAI | null = null;
function getOpenAI(): OpenAI {
  if (!openaiClient) {
    openaiClient = new OpenAI({
      apiKey: getOpenAIKey(),
      // Node 20+ may expose navigator, which the SDK treats as browser-like
      dangerouslyAllowBrowser: true,
    });
  }
  return openaiClient;
}

export interface ValidateInput {
  originalIntent: string;
  originalText: string;
  template: string;
  syntax: string;
}

export async function validateInfographic(
  segment: SegmentPlan,
  template: string,
  syntax: string
): Promise<ValidateOutput> {
  const input: ValidateInput = {
    originalIntent: segment.intent,
    originalText: segment.originalText,
    template,
    syntax,
  };

  const requestPayload = {
    model: getOpenAIModel(),
    messages: [
      { role: 'system', content: VALIDATE_SYSTEM_PROMPT },
      { role: 'user', content: JSON.stringify(input) },
    ],
    tools: [
      {
        type: 'function',
        function: {
          name: TOOL_REGISTRY.validate_infographic.name,
          description: TOOL_REGISTRY.validate_infographic.description,
          parameters: TOOL_REGISTRY.validate_infographic.outputSchema.schema,
        },
      },
    ],
    tool_choice: {
      type: 'function',
      function: { name: TOOL_REGISTRY.validate_infographic.name },
    },
    temperature: 0.2,
  };

  const startTime = logToolInput(TOOL_NAME, {
    segmentId: segment.id,
    intent: segment.intent,
    template,
    syntaxLength: syntax.length,
    requestPayload,
  });

  try {
    const response = await getOpenAI().chat.completions.create(requestPayload);

    const toolCall = response.choices[0]?.message?.tool_calls?.[0];
    if (!toolCall || toolCall.function?.name !== TOOL_REGISTRY.validate_infographic.name) {
      const result = {
        passed: false,
        failureReason: 'VISUAL_QUALITY' as const,
        suggestion: 'Missing tool call for validate_infographic',
      };
      logToolOutput(TOOL_NAME, result, startTime);
      return result;
    }

    const args = toolCall.function.arguments
      ? JSON.parse(toolCall.function.arguments)
      : {};

    const result = validateOrThrow<ValidateOutput>(
      TOOL_REGISTRY.validate_infographic.outputSchema.name,
      TOOL_REGISTRY.validate_infographic.outputSchema.schema,
      args
    );

    // Ensure required fields
    if (typeof result.passed !== 'boolean') {
      const fallback = {
        passed: false,
        failureReason: 'VISUAL_QUALITY' as const,
        suggestion: 'Invalid validation response format',
      };
      logToolOutput(TOOL_NAME, fallback, startTime);
      return fallback;
    }

    logToolOutput(
      TOOL_NAME,
      {
        responseRaw: response,
        toolCallRaw: toolCall,
        passed: result.passed,
        failureReason: result.failureReason,
        suggestion: result.suggestion,
      },
      startTime
    );

    return result;
  } catch (error) {
    logToolError(TOOL_NAME, error, startTime);

    // On error, be conservative and reject
    return {
      passed: false,
      failureReason: 'VISUAL_QUALITY',
      suggestion: `Validation failed with error: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}
