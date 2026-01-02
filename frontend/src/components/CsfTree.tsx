import React, { useState, useEffect } from 'react';
import type { FrameworkElement } from '../types';

interface TreeNodeProps {
  element: FrameworkElement;
  selectedId: number | null;
  onSelect: (element: FrameworkElement) => void;
  level?: number;
}

const TreeNode: React.FC<TreeNodeProps> = ({ element, selectedId, onSelect, level = 0 }) => {
  const [isExpanded, setIsExpanded] = useState(level < 1);
  const hasChildren = element.children && element.children.length > 0;

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsExpanded(!isExpanded);
  };

  const handleSelect = () => {
    if (element.level === 'subcategory') {
      onSelect(element);
    } else if (hasChildren) {
      setIsExpanded(!isExpanded);
    }
  };

  return (
    <div className="tree-node">
      <div
        className={`tree-item ${element.level} ${selectedId === element.id ? 'selected' : ''}`}
        onClick={handleSelect}
      >
        {hasChildren && (
          <span className="tree-toggle" onClick={handleToggle}>
            {isExpanded ? '▼' : '▶'}
          </span>
        )}
        {!hasChildren && <span className="tree-toggle">•</span>}
        <span>
          <strong>{element.code}</strong> - {element.title}
        </span>
      </div>
      {hasChildren && isExpanded && (
        <div style={{ marginLeft: '1rem' }}>
          {element.children!.map((child) => (
            <TreeNode
              key={child.id}
              element={child}
              selectedId={selectedId}
              onSelect={onSelect}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

interface CsfTreeProps {
  elements: FrameworkElement[];
  selectedElement: FrameworkElement | null;
  onSelectElement: (element: FrameworkElement) => void;
}

export const CsfTree: React.FC<CsfTreeProps> = ({ elements, selectedElement, onSelectElement }) => {
  const frameworkName = elements.length > 0 && elements[0].framework === 'Privacy' 
    ? 'NIST Privacy Framework' 
    : 'NIST CSF 2.0';
  
  return (
    <div className="tree-panel">
      <h2>{frameworkName}</h2>
      <div>
        {elements.map((element) => (
          <TreeNode
            key={element.id}
            element={element}
            selectedId={selectedElement?.id || null}
            onSelect={onSelectElement}
          />
        ))}
      </div>
    </div>
  );
};
