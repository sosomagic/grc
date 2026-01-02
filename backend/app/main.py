from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db, init_db
from app.models import FrameworkElement, AssessmentItem, SecurityAssessment
from app.schemas import (
    FrameworkElementTree,
    AssessmentItem as AssessmentItemSchema,
    AssessmentItemUpdate,
    FunctionSummary
)
from app.init_data import initialize_data

app = FastAPI(title="GRC POC API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()
    db = next(get_db())
    try:
        initialize_data(db)
    finally:
        db.close()


def build_tree(elements: List[FrameworkElement], parent_id=None) -> List[dict]:
    """Build hierarchical tree structure"""
    tree = []
    for element in elements:
        if element.parent_id == parent_id:
            node = {
                "id": element.id,
                "code": element.code,
                "title": element.title,
                "description": element.description,
                "level": element.level,
                "parent_id": element.parent_id,
                "children": build_tree(elements, element.id)
            }
            tree.append(node)
    return tree


@app.get("/")
def read_root():
    return {"message": "GRC POC API v0.1"}


@app.get("/framework-elements", response_model=List[FrameworkElementTree])
def get_framework_elements(db: Session = Depends(get_db)):
    """Get all framework elements in tree structure"""
    elements = db.query(FrameworkElement).all()
    tree = build_tree(elements)
    return tree


@app.get("/assessment-items", response_model=List[AssessmentItemSchema])
def get_assessment_items(
    assessment_id: int = 1,
    db: Session = Depends(get_db)
):
    """Get all assessment items for an assessment"""
    items = db.query(AssessmentItem).filter(
        AssessmentItem.assessment_id == assessment_id
    ).all()
    return items


@app.get("/assessment-items/{item_id}", response_model=AssessmentItemSchema)
def get_assessment_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific assessment item"""
    item = db.query(AssessmentItem).filter(AssessmentItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assessment item not found")
    return item


@app.patch("/assessment-items/{item_id}", response_model=AssessmentItemSchema)
def update_assessment_item(
    item_id: int,
    item_update: AssessmentItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an assessment item"""
    item = db.query(AssessmentItem).filter(AssessmentItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assessment item not found")
    
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item


@app.get("/assessment-summary", response_model=List[FunctionSummary])
def get_assessment_summary(
    assessment_id: int = 1,
    db: Session = Depends(get_db)
):
    """Get summary statistics by function"""
    
    # Get all functions
    functions = db.query(FrameworkElement).filter(
        FrameworkElement.level == "function"
    ).all()
    
    summaries = []
    
    for function in functions:
        # Get all subcategories under this function
        subcategories = []
        categories = db.query(FrameworkElement).filter(
            FrameworkElement.parent_id == function.id,
            FrameworkElement.level == "category"
        ).all()
        
        for category in categories:
            subs = db.query(FrameworkElement).filter(
                FrameworkElement.parent_id == category.id,
                FrameworkElement.level == "subcategory"
            ).all()
            subcategories.extend(subs)
        
        if not subcategories:
            continue
        
        # Get assessment items for these subcategories
        subcategory_ids = [s.id for s in subcategories]
        items = db.query(AssessmentItem).filter(
            AssessmentItem.assessment_id == assessment_id,
            AssessmentItem.framework_element_id.in_(subcategory_ids)
        ).all()
        
        if not items:
            continue
        
        # Calculate averages
        total_current = sum(item.current_maturity for item in items)
        total_target = sum(item.target_maturity for item in items)
        avg_current = total_current / len(items) if items else 0
        avg_target = total_target / len(items) if items else 0
        
        # Count completed (current_maturity > 0)
        completed = sum(1 for item in items if item.current_maturity > 0)
        
        summaries.append(FunctionSummary(
            function_code=function.code,
            function_title=function.title,
            avg_current=round(avg_current, 2),
            avg_target=round(avg_target, 2),
            total_subcategories=len(items),
            completed_subcategories=completed
        ))
    
    return summaries


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
