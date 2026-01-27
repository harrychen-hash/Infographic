/**
 * Tool 3: render_infographic [Deterministic]
 * 调用 AntV Infographic SSR 渲染 SVG
 */

import OpenAI from 'openai';
import type { RenderInput, RenderOutput } from '../types';
import { RENDER_TOOL_PROMPT } from '../prompts/render-prompt';
import { TOOL_REGISTRY } from './registry';
import { getOpenAIKey, getOpenAIModel } from '../utils/env';
import { logToolInput, logToolOutput, logToolError } from '../utils/logger';
import { validateOrThrow } from '../utils/schema';

const TOOL_NAME = 'render_infographic';
const TOOL_CALL_NAME = 'render_infographic_call';

// Dynamic import for SSR module (only available in Node.js environment)
// The SSR module is exported from @antv/infographic but types may not be fully resolved
async function getSSRRenderer() {
  // @ts-expect-error - SSR module exists at runtime but types may not be resolved in dev
  const { renderToString } = await import('@antv/infographic/ssr');
  return renderToString as (
    options: string,
    init?: { width?: number; height?: number }
  ) => Promise<string>;
}

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

export async function renderInfographicViaTool(
  syntax: string
): Promise<RenderOutput> {
  const requestPayload = {
    model: getOpenAIModel(),
    messages: [
      { role: 'system', content: RENDER_TOOL_PROMPT },
      { role: 'user', content: JSON.stringify({ syntax }) },
    ],
    tools: [
      {
        type: 'function',
        function: {
          name: TOOL_REGISTRY.render_infographic.name,
          description: TOOL_REGISTRY.render_infographic.description,
          parameters: TOOL_REGISTRY.render_infographic.inputSchema,
        },
      },
    ],
    tool_choice: {
      type: 'function',
      function: { name: TOOL_REGISTRY.render_infographic.name },
    },
    temperature: 0,
  };

  const startTime = logToolInput(TOOL_CALL_NAME, {
    model: getOpenAIModel(),
    syntaxLength: syntax.length,
    requestPayload,
  });

  try {
    const response = await getOpenAI().chat.completions.create(requestPayload);

    const toolCall = response.choices[0]?.message?.tool_calls?.[0];
    if (!toolCall || toolCall.function?.name !== TOOL_REGISTRY.render_infographic.name) {
      throw new Error('Missing tool call for render_infographic');
    }

    const args = toolCall.function.arguments
      ? JSON.parse(toolCall.function.arguments)
      : {};

    const validated = validateOrThrow<RenderInput>(
      TOOL_REGISTRY.render_infographic.name,
      TOOL_REGISTRY.render_infographic.inputSchema,
      args
    );

    logToolOutput(
      TOOL_CALL_NAME,
      {
        responseRaw: response,
        toolCallRaw: toolCall,
        toolCall: {
          name: toolCall.function.name,
          arguments: validated,
        },
      },
      startTime
    );

    return renderInfographic(validated.syntax);
  } catch (error) {
    logToolError(TOOL_CALL_NAME, error, startTime);
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

export async function renderInfographic(syntax: string): Promise<RenderOutput> {
  const renderOptions = { width: 800, height: 600 };
  const startTime = logToolInput(TOOL_NAME, {
    syntax,
    renderOptions,
  });

  try {
    // Validate syntax is not empty
    if (!syntax || syntax.trim().length === 0) {
      const result = { success: false, error: 'Empty syntax provided' };
      logToolOutput(TOOL_NAME, result, startTime);
      return result;
    }

    // Validate syntax starts with 'infographic'
    if (!syntax.trim().startsWith('infographic')) {
      const result = { success: false, error: 'Invalid syntax: must start with "infographic"' };
      logToolOutput(TOOL_NAME, result, startTime);
      return result;
    }

    const renderToString = await getSSRRenderer();

    const svg = await renderToString(syntax, renderOptions);

    if (!svg || svg.trim().length === 0) {
      const result = { success: false, error: 'Render returned empty SVG' };
      logToolOutput(TOOL_NAME, result, startTime);
      return result;
    }

    const result = { success: true, svg };
    logToolOutput(
      TOOL_NAME,
      {
        success: true,
        svgLength: svg.length,
        renderOptions,
      },
      startTime
    );

    return result;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    logToolError(TOOL_NAME, error, startTime);

    return {
      success: false,
      error: errorMessage,
    };
  }
}
