from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class FrameworkElement(Base):
    __tablename__ = "framework_elements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    level = Column(String(20), nullable=False)  # function, category, subcategory
    parent_id = Column(Integer, ForeignKey("framework_elements.id"), nullable=True)

    parent = relationship("FrameworkElement", remote_side=[id], backref="children")
    assessment_items = relationship("AssessmentItem", back_populates="framework_element")


class SecurityAssessment(Base):
    __tablename__ = "security_assessments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    assessment_items = relationship("AssessmentItem", back_populates="assessment")


class AssessmentItem(Base):
    __tablename__ = "assessment_items"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("security_assessments.id"), nullable=False)
    framework_element_id = Column(Integer, ForeignKey("framework_elements.id"), nullable=False)
    current_maturity = Column(Integer, default=0)  # 0-5
    target_maturity = Column(Integer, default=0)  # 0-5
    notes = Column(Text)
    evidence_links = Column(Text)  # JSON array as text

    assessment = relationship("SecurityAssessment", back_populates="assessment_items")
    framework_element = relationship("FrameworkElement", back_populates="assessment_items")
