/**
 * Article Illustrator - Type Definitions
 * Agentic Workflow: 3 Tools + Guardrail
 */

// ============ Tool 1: segment_and_extract ============

export interface SegmentInput {
  html: string;
}

export interface DataPoint {
  label: string;
  value?: number;
  desc?: string;
}

export interface Relationship {
  from: string;
  to: string;
  relation?: string;
}

export interface StructuredData {
  title?: string;
  dataPoints?: DataPoint[];
  relationships?: Relationship[];
}

export interface SegmentPlan {
  id: string;
  insertAfterSelector: string;
  originalText: string;
  contentSummary: string;
  intent: string;
  structuredData: StructuredData;
  suitableForInfographic: boolean;
  rejectionReason?: string;
}

export interface SegmentOutput {
  segments: SegmentPlan[];
}

// ============ Tool 2: select_template ============

export interface SelectInput {
  segment: SegmentPlan;
  triedTemplates: string[];
}

export interface SelectOutput {
  template: string;
  syntax: string;
  intentAlignment: string;
  dataCompleteness: 'complete' | 'partial';
}

// ============ Tool 3: render_infographic ============

export interface RenderInput {
  syntax: string;
}

export interface RenderOutput {
  success: boolean;
  svg?: string;
  error?: string;
}

// ============ Guardrail: validate_infographic ============

export interface ValidateInput {
  originalIntent: string;
  originalText: string;
  template: string;
  syntax: string;
}

export type FailureReason =
  | 'INTENT_MISMATCH'
  | 'DATA_INCORRECT'
  | 'VISUAL_QUALITY'
  | 'TEMPLATE_UNSUITABLE';

export interface ValidateOutput {
  passed: boolean;
  failureReason?: FailureReason;
  suggestion?: string;
}

// ============ Workflow State ============

export interface ProcessResult {
  success: boolean;
  svg?: string;
  selector: string;
  segmentId?: string;
  template?: string;
}

export interface FailedPlan {
  planId: string;
  error: string;
  retryCount: number;
}

export interface AgentContext {
  originalHtml: string;
  segments: SegmentPlan[];
  currentHtml: string;
  completedSegmentIds: string[];
  failedPlans: FailedPlan[];
}

// ============ Stream Events ============

export type StreamEventType =
  | 'segmenting'
  | 'segments_ready'
  | 'generating'
  | 'render_failed'
  | 'validation_failed'
  | 'success'
  | 'skipped'
  | 'complete'
  | 'error';

export interface StreamEvent {
  type: StreamEventType;
  message?: string;
  segmentId?: string;
  segments?: SegmentPlan[];
  attempt?: number;
  error?: string;
  reason?: FailureReason;
  suggestion?: string;
  template?: string;
  html?: string;
}

// ============ Template Metadata ============

export type TemplateCategory =
  | 'chart'
  | 'list'
  | 'sequence'
  | 'compare'
  | 'hierarchy'
  | 'relation';

export type DataFieldType =
  | 'values'
  | 'lists'
  | 'sequences'
  | 'compares'
  | 'root'
  | 'items'
  | 'nodes';

export interface TemplateMetadata {
  name: string;
  category: TemplateCategory;
  dataField: DataFieldType;
  description: string;
  suitableFor: string[];
  notSuitableFor: string[];
  requiredFields: string[];
  optionalFields: string[];
}
