import React, { useState, useEffect } from 'react';
import { api } from '../api';
import type { FrameworkElement, AssessmentItem, AssessmentItemUpdate } from '../types';

interface AssessmentDetailProps {
  element: FrameworkElement | null;
}

const maturityLevels = [
  { value: 0, label: '0 - Not Implemented' },
  { value: 1, label: '1 - Initial' },
  { value: 2, label: '2 - Developing' },
  { value: 3, label: '3 - Defined' },
  { value: 4, label: '4 - Managed' },
  { value: 5, label: '5 - Optimized' }
];

export const AssessmentDetail: React.FC<AssessmentDetailProps> = ({ element }) => {
  const [assessmentItem, setAssessmentItem] = useState<AssessmentItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'success' | 'error' | null>(null);
  const [formData, setFormData] = useState({
    current_maturity: 0,
    target_maturity: 3,
    notes: '',
    evidence_links: ['']
  });

  useEffect(() => {
    if (element && element.level === 'subcategory') {
      loadAssessmentItem();
    }
  }, [element]);

  const loadAssessmentItem = async () => {
    if (!element) return;
    
    setLoading(true);
    try {
      const items = await api.getAssessmentItems(1);
      const item = items.find(i => i.framework_element_id === element.id);
      
      if (item) {
        setAssessmentItem(item);
        setFormData({
          current_maturity: item.current_maturity,
          target_maturity: item.target_maturity,
          notes: item.notes || '',
          evidence_links: item.evidence_links?.length > 0 ? item.evidence_links : ['']
        });
      }
    } catch (error) {
      console.error('Error loading assessment item:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!assessmentItem) return;

    setSaving(true);
    setSaveStatus(null);

    try {
      const updateData: AssessmentItemUpdate = {
        current_maturity: formData.current_maturity,
        target_maturity: formData.target_maturity,
        notes: formData.notes,
        evidence_links: formData.evidence_links.filter(link => link.trim() !== '')
      };

      await api.updateAssessmentItem(assessmentItem.id, updateData);
      setSaveStatus('success');
      setTimeout(() => setSaveStatus(null), 3000);
    } catch (error) {
      console.error('Error saving assessment item:', error);
      setSaveStatus('error');
    } finally {
      setSaving(false);
    }
  };

  const handleEvidenceLinkChange = (index: number, value: string) => {
    const newLinks = [...formData.evidence_links];
    newLinks[index] = value;
    setFormData({ ...formData, evidence_links: newLinks });
  };

  const addEvidenceLink = () => {
    setFormData({
      ...formData,
      evidence_links: [...formData.evidence_links, '']
    });
  };

  const removeEvidenceLink = (index: number) => {
    const newLinks = formData.evidence_links.filter((_, i) => i !== index);
    setFormData({
      ...formData,
      evidence_links: newLinks.length > 0 ? newLinks : ['']
    });
  };

  if (!element) {
    return (
      <div className="detail-panel">
        <div className="detail-empty">
          Select a subcategory to view and edit assessment details
        </div>
      </div>
    );
  }

  if (element.level !== 'subcategory') {
    return (
      <div className="detail-panel">
        <div className="detail-empty">
          Please select a subcategory to assess
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="detail-panel">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="detail-panel">
      <div className="detail-content">
        <div className="detail-header">
          <div className="detail-code">{element.code}</div>
          <h2 className="detail-title">{element.title}</h2>
          <p className="detail-description">{element.description}</p>
        </div>

        <div className="assessment-form">
          <div className="maturity-scores">
            <div className="form-group">
              <label htmlFor="current-maturity">Current Maturity Score</label>
              <select
                id="current-maturity"
                value={formData.current_maturity}
                onChange={(e) => setFormData({ ...formData, current_maturity: Number(e.target.value) })}
              >
                {maturityLevels.map((level) => (
                  <option key={level.value} value={level.value}>
                    {level.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="target-maturity">Target Maturity Score</label>
              <select
                id="target-maturity"
                value={formData.target_maturity}
                onChange={(e) => setFormData({ ...formData, target_maturity: Number(e.target.value) })}
              >
                {maturityLevels.map((level) => (
                  <option key={level.value} value={level.value}>
                    {level.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="notes">Notes</label>
            <textarea
              id="notes"
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              placeholder="Add implementation notes, observations, or action items..."
            />
          </div>

          <div className="form-group">
            <label>Evidence Links</label>
            <div className="evidence-list">
              {formData.evidence_links.map((link, index) => (
                <div key={index} className="evidence-item">
                  <input
                    type="text"
                    value={link}
                    onChange={(e) => handleEvidenceLinkChange(index, e.target.value)}
                    placeholder="https://confluence.example.com/... or https://docs.google.com/..."
                  />
                  {formData.evidence_links.length > 1 && (
                    <button
                      type="button"
                      className="btn btn-danger btn-small"
                      onClick={() => removeEvidenceLink(index)}
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button
              type="button"
              className="btn btn-secondary btn-small"
              onClick={addEvidenceLink}
              style={{ marginTop: '0.5rem' }}
            >
              + Add Evidence Link
            </button>
          </div>

          <div className="form-actions">
            <button
              className="btn btn-primary"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save Assessment'}
            </button>
            {saveStatus === 'success' && (
              <div className="save-status success">✓ Saved successfully</div>
            )}
            {saveStatus === 'error' && (
              <div className="save-status error">✗ Error saving. Please try again.</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
