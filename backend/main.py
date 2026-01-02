from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import models
import schemas
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GRC POC API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_tree(elements: List[models.FrameworkElement], parent_id=None):
    """Build hierarchical tree structure"""
    tree = []
    for element in elements:
        if element.parent_id == parent_id:
            node = schemas.FrameworkElement.from_orm(element)
            node_dict = node.model_dump()
            node_dict['children'] = build_tree(elements, element.id)
            tree.append(node_dict)
    return tree


@app.get("/")
def read_root():
    return {"message": "GRC POC API v0.1"}


@app.get("/framework-elements", response_model=List[Dict])
def get_framework_elements(
    framework: str = "CSF",
    db: Session = Depends(get_db)
):
    """Get framework elements as a tree structure. Filter by framework: CSF or Privacy"""
    elements = db.query(models.FrameworkElement).filter(
        models.FrameworkElement.framework == framework
    ).all()
    tree = build_tree(elements)
    return tree


@app.get("/framework-elements/flat", response_model=List[schemas.FrameworkElement])
def get_framework_elements_flat(db: Session = Depends(get_db)):
    """Get all framework elements as flat list"""
    elements = db.query(models.FrameworkElement).all()
    return elements


@app.get("/assessment-items", response_model=List[schemas.AssessmentItemDetail])
def get_assessment_items(
    assessment_id: int = 1,
    db: Session = Depends(get_db)
):
    """Get all assessment items for a specific assessment"""
    items = db.query(models.AssessmentItem).filter(
        models.AssessmentItem.assessment_id == assessment_id
    ).all()
    return items


@app.get("/assessment-items/{item_id}", response_model=schemas.AssessmentItemDetail)
def get_assessment_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific assessment item"""
    item = db.query(models.AssessmentItem).filter(
        models.AssessmentItem.id == item_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Assessment item not found")
    return item


@app.patch("/assessment-items/{item_id}", response_model=schemas.AssessmentItemDetail)
def update_assessment_item(
    item_id: int,
    item_update: schemas.AssessmentItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an assessment item"""
    db_item = db.query(models.AssessmentItem).filter(
        models.AssessmentItem.id == item_id
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Assessment item not found")
    
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/summary", response_model=Dict)
def get_summary(assessment_id: int = 1, db: Session = Depends(get_db)):
    """Get summary statistics by Function"""
    # Get all assessment items with their framework elements
    items = db.query(models.AssessmentItem).filter(
        models.AssessmentItem.assessment_id == assessment_id
    ).all()
    
    # Get all functions
    functions = db.query(models.FrameworkElement).filter(
        models.FrameworkElement.level == "function"
    ).all()
    
    summary = []
    for function in functions:
        # Get all subcategories under this function
        subcategories = []
        for category in function.children:
            subcategories.extend(category.children)
        
        # Get assessment items for these subcategories
        subcategory_ids = [sub.id for sub in subcategories]
        function_items = [
            item for item in items 
            if item.framework_element_id in subcategory_ids
        ]
        
        if function_items:
            avg_current = sum(item.current_maturity for item in function_items) / len(function_items)
            avg_target = sum(item.target_maturity for item in function_items) / len(function_items)
            completed = sum(1 for item in function_items if item.current_maturity > 0)
        else:
            avg_current = 0
            avg_target = 0
            completed = 0
        
        summary.append({
            "function_code": function.code,
            "function_name": function.title,
            "avg_current_maturity": round(avg_current, 2),
            "avg_target_maturity": round(avg_target, 2),
            "total_subcategories": len(subcategory_ids),
            "completed_subcategories": completed
        })
    
    return {
        "assessment_id": assessment_id,
        "summary": summary
    }
