import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { CsfTree } from '../components/CsfTree';
import { AssessmentDetail } from '../components/AssessmentDetail';
import type { FrameworkElement } from '../types';

export const CsfBrowser: React.FC = () => {
  const [frameworkTree, setFrameworkTree] = useState<FrameworkElement[]>([]);
  const [selectedElement, setSelectedElement] = useState<FrameworkElement | null>(null);
  const [selectedFramework, setSelectedFramework] = useState<string>('CSF');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFramework();
  }, [selectedFramework]);

  const loadFramework = async () => {
    setLoading(true);
    setError(null);
    setSelectedElement(null);
    try {
      const data = await api.getFrameworkTree(selectedFramework);
      setFrameworkTree(data);
    } catch (err) {
      console.error('Error loading framework:', err);
      setError('Failed to load framework data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="main-content">
        <div className="loading">Loading framework...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="main-content">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div style={{ marginBottom: '1rem' }}>
        <label style={{ marginRight: '0.5rem', fontWeight: 600 }}>Select Framework:</label>
        <select 
          value={selectedFramework} 
          onChange={(e) => setSelectedFramework(e.target.value)}
          style={{ 
            padding: '0.5rem', 
            borderRadius: '4px', 
            border: '1px solid #cbd5e0',
            fontSize: '1rem'
          }}
        >
          <option value="CSF">NIST CSF 2.0</option>
          <option value="Privacy">NIST Privacy Framework</option>
        </select>
      </div>
      <div className="csf-browser">
        <CsfTree
          elements={frameworkTree}
          selectedElement={selectedElement}
          onSelectElement={setSelectedElement}
        />
        <AssessmentDetail element={selectedElement} />
      </div>
    </div>
  );
};
