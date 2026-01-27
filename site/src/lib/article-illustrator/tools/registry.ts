import { TEMPLATE_NAMES } from '../utils/templates';

export const TOOL_REGISTRY = {
  segment_and_extract: {
    name: 'segment_and_extract',
    description:
      '按“意图单元”分段并抽取结构化数据：识别每个意图的摘要、原文片段、结构化数据点与关系；判断是否适合配图；并给出插入位置（必须指向该意图覆盖的最后一个自然段落/文本块之后）。',
    inputSchema: {
      type: 'object',
      properties: {
        html: { type: 'string', description: '原始文章 HTML 字符串' },
      },
      required: ['html'],
      additionalProperties: false,
    },
    outputSchema: {
      name: 'segment_and_extract_output',
      description: '分段与结构化数据提取结果',
      strict: true,
      schema: {
        type: 'object',
        properties: {
          segments: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                insertAfterSelector: { type: 'string' },
                originalText: { type: 'string' },
                contentSummary: { type: 'string' },
                intent: { type: 'string' },
                structuredData: {
                  type: 'object',
                  properties: {
                    title: { type: 'string' },
                    dataPoints: {
                      type: 'array',
                      items: {
                        type: 'object',
                        properties: {
                          label: { type: 'string' },
                          value: {
                            anyOf: [{ type: 'number' }, { type: 'string' }],
                          },
                          desc: { type: 'string' },
                        },
                        required: ['label'],
                        additionalProperties: false,
                      },
                    },
                    relationships: {
                      type: 'array',
                      items: {
                        type: 'object',
                        properties: {
                          from: { type: 'string' },
                          to: { type: 'string' },
                          relation: { type: 'string' },
                        },
                        required: ['from', 'to'],
                        additionalProperties: false,
                      },
                    },
                  },
                  required: [],
                  additionalProperties: false,
                },
                suitableForInfographic: { type: 'boolean' },
                rejectionReason: { type: 'string' },
              },
              required: [
                'id',
                'insertAfterSelector',
                'originalText',
                'contentSummary',
                'intent',
                'structuredData',
                'suitableForInfographic',
              ],
              additionalProperties: false,
            },
          },
        },
        required: ['segments'],
        additionalProperties: false,
      },
    },
  },
  select_template: {
    name: 'select_template',
    description:
      '根据意图与结构化数据选择最合适的模板，生成对应的 AntV Infographic DSL；需说明意图匹配与数据完整性，并避免重复使用已尝试失败的模板。',
    inputSchema: {
      type: 'object',
      properties: {
        segment: { type: 'object' },
        triedTemplates: {
          type: 'array',
          items: { type: 'string' },
        },
      },
      required: ['segment', 'triedTemplates'],
      additionalProperties: false,
    },
    outputSchema: {
      name: 'select_template_output',
      description: '模板选择与 DSL 语法结果',
      strict: true,
      schema: {
        type: 'object',
        properties: {
          template: { type: 'string', enum: TEMPLATE_NAMES },
          syntax: { type: 'string' },
          intentAlignment: { type: 'string' },
          dataCompleteness: {
            type: 'string',
            enum: ['complete', 'partial'],
          },
        },
        required: ['template', 'syntax', 'intentAlignment', 'dataCompleteness'],
        additionalProperties: false,
      },
    },
  },
  render_infographic: {
    name: 'render_infographic',
    description:
      '使用 AntV Infographic SSR 将 DSL 渲染为 SVG；输入为 DSL 字符串，输出为 SVG 或错误信息。',
    inputSchema: {
      type: 'object',
      properties: {
        syntax: { type: 'string' },
      },
      required: ['syntax'],
      additionalProperties: false,
    },
    outputSchema: {
      name: 'render_infographic_output',
      description: 'SVG 渲染结果',
      strict: true,
      schema: {
        type: 'object',
        properties: {
          success: { type: 'boolean' },
          svg: { type: 'string' },
          error: { type: 'string' },
        },
        required: ['success'],
        additionalProperties: false,
      },
    },
  },
  validate_infographic: {
    name: 'validate_infographic',
    description:
      '审核生成图表是否与原文意图一致、数据准确、视觉可读、模板适配；给出通过/失败及可操作建议。',
    inputSchema: {
      type: 'object',
      properties: {
        originalIntent: { type: 'string' },
        originalText: { type: 'string' },
        template: { type: 'string' },
        syntax: { type: 'string' },
      },
      required: ['originalIntent', 'originalText', 'template', 'syntax'],
      additionalProperties: false,
    },
    outputSchema: {
      name: 'validate_infographic_output',
      description: '验证结果',
      strict: true,
      schema: {
        type: 'object',
        properties: {
          passed: { type: 'boolean' },
          failureReason: {
            type: 'string',
            enum: [
              'INTENT_MISMATCH',
              'DATA_INCORRECT',
              'VISUAL_QUALITY',
              'TEMPLATE_UNSUITABLE',
            ],
          },
          suggestion: { type: 'string' },
        },
        required: ['passed'],
        additionalProperties: false,
      },
    },
  },
} as const;
