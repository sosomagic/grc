from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base


class FrameworkElement(Base):
    __tablename__ = "framework_elements"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # e.g., "ID.AM-01"
    title = Column(String)
    description = Column(Text)
    level = Column(String)  # "function" | "category" | "subcategory"
    framework = Column(String, default="CSF")  # "CSF" | "Privacy"
    parent_id = Column(Integer, ForeignKey("framework_elements.id"), nullable=True)
    
    # Relationships
    parent = relationship("FrameworkElement", remote_side=[id], backref="children")
    assessment_items = relationship("AssessmentItem", back_populates="framework_element")


class SecurityAssessment(Base):
    __tablename__ = "security_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    
    # Relationships
    assessment_items = relationship("AssessmentItem", back_populates="assessment")


class AssessmentItem(Base):
    __tablename__ = "assessment_items"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("security_assessments.id"))
    framework_element_id = Column(Integer, ForeignKey("framework_elements.id"))
    current_maturity = Column(Integer, default=0)  # 0-5
    target_maturity = Column(Integer, default=0)   # 0-5
    notes = Column(Text)
    evidence_links = Column(JSON)  # Array of URLs as JSON
    
    # Relationships
    assessment = relationship("SecurityAssessment", back_populates="assessment_items")
    framework_element = relationship("FrameworkElement", back_populates="assessment_items")
