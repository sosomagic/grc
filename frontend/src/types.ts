export interface FrameworkElement {
  id: number;
  code: string;
  title: string;
  description: string;
  level: 'function' | 'category' | 'subcategory';
  framework: string;
  parent_id: number | null;
  children?: FrameworkElement[];
}

export interface AssessmentItem {
  id: number;
  assessment_id: number;
  framework_element_id: number;
  current_maturity: number;
  target_maturity: number;
  notes: string;
  evidence_links: string[];
  framework_element?: FrameworkElement;
}

export interface AssessmentItemUpdate {
  current_maturity?: number;
  target_maturity?: number;
  notes?: string;
  evidence_links?: string[];
}

export interface FunctionSummary {
  function_code: string;
  function_name: string;
  avg_current_maturity: number;
  avg_target_maturity: number;
  total_subcategories: number;
  completed_subcategories: number;
}

export interface SummaryResponse {
  assessment_id: number;
  summary: FunctionSummary[];
}
