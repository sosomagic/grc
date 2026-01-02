from pydantic import BaseModel
from typing import Optional, List


class FrameworkElementBase(BaseModel):
    code: str
    title: str
    description: str
    level: str
    framework: str = "CSF"
    parent_id: Optional[int] = None


class FrameworkElementCreate(FrameworkElementBase):
    pass


class FrameworkElement(FrameworkElementBase):
    id: int
    
    class Config:
        from_attributes = True


class FrameworkElementTree(FrameworkElement):
    children: List['FrameworkElementTree'] = []


class AssessmentItemBase(BaseModel):
    current_maturity: int = 0
    target_maturity: int = 0
    notes: Optional[str] = None
    evidence_links: Optional[List[str]] = None


class AssessmentItemCreate(AssessmentItemBase):
    assessment_id: int
    framework_element_id: int


class AssessmentItemUpdate(BaseModel):
    current_maturity: Optional[int] = None
    target_maturity: Optional[int] = None
    notes: Optional[str] = None
    evidence_links: Optional[List[str]] = None


class AssessmentItem(AssessmentItemBase):
    id: int
    assessment_id: int
    framework_element_id: int
    
    class Config:
        from_attributes = True


class AssessmentItemDetail(AssessmentItem):
    framework_element: FrameworkElement


class SecurityAssessmentBase(BaseModel):
    name: str
    description: str


class SecurityAssessment(SecurityAssessmentBase):
    id: int
    
    class Config:
        from_attributes = True
