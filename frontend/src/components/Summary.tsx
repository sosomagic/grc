import React, { useState, useEffect } from 'react';
import { api } from '../api';
import type { FunctionSummary, SummaryResponse } from '../types';

export const Summary: React.FC = () => {
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getSummary(1);
      setSummary(data);
    } catch (err) {
      console.error('Error loading summary:', err);
      setError('Failed to load summary data');
    } finally {
      setLoading(false);
    }
  };

  const getMaturityClass = (score: number): string => {
    if (score < 2) return 'low';
    if (score < 4) return 'medium';
    return 'high';
  };

  const getCompletionPercentage = (completed: number, total: number): number => {
    return total > 0 ? Math.round((completed / total) * 100) : 0;
  };

  if (loading) {
    return (
      <div className="main-content">
        <div className="loading">Loading summary...</div>
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

  if (!summary) {
    return (
      <div className="main-content">
        <div className="error">No summary data available</div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="summary-container">
        <div className="summary-header">
          <h2>Assessment Summary</h2>
          <p>Overview of NIST CSF 2.0 maturity by Function</p>
        </div>

        <div className="summary-table">
          <table>
            <thead>
              <tr>
                <th>Function</th>
                <th>Avg Current Maturity</th>
                <th>Avg Target Maturity</th>
                <th>Subcategories</th>
                <th>Completion</th>
              </tr>
            </thead>
            <tbody>
              {summary.summary.map((func: FunctionSummary) => {
                const completionPct = getCompletionPercentage(
                  func.completed_subcategories,
                  func.total_subcategories
                );
                return (
                  <tr key={func.function_code}>
                    <td>
                      <div className="function-code">{func.function_code}</div>
                      <div style={{ fontSize: '0.9rem', color: '#4a5568' }}>
                        {func.function_name}
                      </div>
                    </td>
                    <td>
                      <span className={`maturity-score ${getMaturityClass(func.avg_current_maturity)}`}>
                        {func.avg_current_maturity.toFixed(1)}
                      </span>
                    </td>
                    <td>
                      <span className={`maturity-score ${getMaturityClass(func.avg_target_maturity)}`}>
                        {func.avg_target_maturity.toFixed(1)}
                      </span>
                    </td>
                    <td>
                      {func.completed_subcategories} / {func.total_subcategories}
                    </td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div className="progress-bar" style={{ flex: 1 }}>
                          <div
                            className="progress-fill"
                            style={{ width: `${completionPct}%` }}
                          />
                        </div>
                        <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>
                          {completionPct}%
                        </span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
