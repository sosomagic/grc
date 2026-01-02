import axios from 'axios';
import type { FrameworkElement, AssessmentItem, AssessmentItemUpdate, SummaryResponse } from './types';

const API_BASE = '/api';

export const api = {
  // Framework elements
  getFrameworkTree: async (framework: string = 'CSF'): Promise<FrameworkElement[]> => {
    const response = await axios.get(`${API_BASE}/framework-elements`, {
      params: { framework }
    });
    return response.data;
  },

  // Assessment items
  getAssessmentItems: async (assessmentId: number = 1): Promise<AssessmentItem[]> => {
    const response = await axios.get(`${API_BASE}/assessment-items`, {
      params: { assessment_id: assessmentId }
    });
    return response.data;
  },

  getAssessmentItem: async (itemId: number): Promise<AssessmentItem> => {
    const response = await axios.get(`${API_BASE}/assessment-items/${itemId}`);
    return response.data;
  },

  updateAssessmentItem: async (
    itemId: number,
    data: AssessmentItemUpdate
  ): Promise<AssessmentItem> => {
    const response = await axios.patch(`${API_BASE}/assessment-items/${itemId}`, data);
    return response.data;
  },

  // Summary
  getSummary: async (assessmentId: number = 1): Promise<SummaryResponse> => {
    const response = await axios.get(`${API_BASE}/summary`, {
      params: { assessment_id: assessmentId }
    });
    return response.data;
  }
};
