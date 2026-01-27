/**
 * Tool 2: select_template [LLM]
 * 根据段落内容选择最佳模板，生成 DSL 语法
 */

import OpenAI from 'openai';
import type { SegmentPlan, SelectOutput } from '../types';
import { SELECT_SYSTEM_PROMPT } from '../prompts/select-prompt';
import { TEMPLATES } from '../utils/templates';
import { TOOL_REGISTRY } from './registry';
import { getOpenAIKey, getOpenAIModel } from '../utils/env';
import { logToolInput, logToolOutput, logToolError } from '../utils/logger';
import { validateOrThrow } from '../utils/schema';

const TOOL_NAME = 'select_template';

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

export interface SelectInput {
  segment: SegmentPlan;
  triedTemplates: string[];
}

export async function selectTemplate(input: SelectInput): Promise<SelectOutput> {
  const requestPayload = {
    model: getOpenAIModel(),
    messages: [
      { role: 'system', content: SELECT_SYSTEM_PROMPT },
      { role: 'user', content: JSON.stringify(input) },
    ],
    tools: [
      {
        type: 'function',
        function: {
          name: TOOL_REGISTRY.select_template.name,
          description: TOOL_REGISTRY.select_template.description,
          parameters: TOOL_REGISTRY.select_template.outputSchema.schema,
        },
      },
    ],
    tool_choice: {
      type: 'function',
      function: { name: TOOL_REGISTRY.select_template.name },
    },
    temperature: 0.3,
  };

  const startTime = logToolInput(TOOL_NAME, {
    segmentId: input.segment.id,
    intent: input.segment.intent,
    triedTemplates: input.triedTemplates,
    requestPayload,
  });

  try {
    const response = await getOpenAI().chat.completions.create(requestPayload);

    const toolCall = response.choices[0]?.message?.tool_calls?.[0];
    if (!toolCall || toolCall.function?.name !== TOOL_REGISTRY.select_template.name) {
      throw new Error('Missing tool call for select_template');
    }

    const args = toolCall.function.arguments
      ? JSON.parse(toolCall.function.arguments)
      : {};

    const result = validateOrThrow<SelectOutput>(
      TOOL_REGISTRY.select_template.outputSchema.name,
      TOOL_REGISTRY.select_template.outputSchema.schema,
      args
    );

    // Validate required fields
    if (!result.template || !result.syntax) {
      throw new Error('Missing required fields: template or syntax');
    }

    const templateMeta =
      TEMPLATES.find((t) => t.name === result.template) || null;

    logToolOutput(
      TOOL_NAME,
      {
        responseRaw: response,
        toolCallRaw: toolCall,
        template: result.template,
        intentAlignment: result.intentAlignment,
        dataCompleteness: result.dataCompleteness,
        syntax: result.syntax,
        templateMeta: templateMeta
          ? {
              category: templateMeta.category,
              dataField: templateMeta.dataField,
              description: templateMeta.description,
              requiredFields: templateMeta.requiredFields,
              optionalFields: templateMeta.optionalFields,
            }
          : null,
      },
      startTime
    );

    return result;
  } catch (error) {
    logToolError(TOOL_NAME, error, startTime);
    throw error;
  }
}
