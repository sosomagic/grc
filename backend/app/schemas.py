from pydantic import BaseModel
from typing import Optional, List


class FrameworkElementBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    level: str
    parent_id: Optional[int] = None


class FrameworkElementCreate(FrameworkElementBase):
    pass


class FrameworkElement(FrameworkElementBase):
    id: int

    class Config:
        from_attributes = True


class FrameworkElementTree(FrameworkElement):
    children: List['FrameworkElementTree'] = []

    class Config:
        from_attributes = True


class SecurityAssessmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class SecurityAssessmentCreate(SecurityAssessmentBase):
    pass


class SecurityAssessment(SecurityAssessmentBase):
    id: int

    class Config:
        from_attributes = True


class AssessmentItemBase(BaseModel):
    assessment_id: int
    framework_element_id: int
    current_maturity: int = 0
    target_maturity: int = 0
    notes: Optional[str] = None
    evidence_links: Optional[str] = None


class AssessmentItemCreate(AssessmentItemBase):
    pass


class AssessmentItemUpdate(BaseModel):
    current_maturity: Optional[int] = None
    target_maturity: Optional[int] = None
    notes: Optional[str] = None
    evidence_links: Optional[str] = None


class AssessmentItem(AssessmentItemBase):
    id: int
    framework_element: FrameworkElement

    class Config:
        from_attributes = True


class FunctionSummary(BaseModel):
    function_code: str
    function_title: str
    avg_current: float
    avg_target: float
    total_subcategories: int
    completed_subcategories: int
