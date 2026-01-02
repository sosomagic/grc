import json
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Create tables
models.Base.metadata.create_all(bind=engine)


def load_framework(db, file_path, framework_name):
    """Load a framework from JSON file"""
    with open(file_path, 'r') as f:
        framework_data = json.load(f)
    
    print(f"\nLoading {framework_name}...")
    
    # Create functions
    functions_map = {}
    for func_data in framework_data['functions']:
        func = models.FrameworkElement(
            code=func_data['code'],
            title=func_data['title'],
            description=func_data['description'],
            level='function',
            framework=framework_name,
            parent_id=None
        )
        db.add(func)
        db.flush()
        functions_map[func.code] = func.id
        print(f"  ✓ Function: {func.code} - {func.title}")
    
    # Create categories
    categories_map = {}
    for cat_data in framework_data['categories']:
        category = models.FrameworkElement(
            code=cat_data['code'],
            title=cat_data['title'],
            description=cat_data['description'],
            level='category',
            framework=framework_name,
            parent_id=functions_map[cat_data['function']]
        )
        db.add(category)
        db.flush()
        categories_map[cat_data['code']] = category.id
        print(f"    ✓ Category: {cat_data['code']} - {cat_data['title']}")
    
    # Create subcategories
    subcategory_count = 0
    for sub_data in framework_data['subcategories']:
        subcategory = models.FrameworkElement(
            code=sub_data['code'],
            title=sub_data['title'],
            description=sub_data['title'],
            level='subcategory',
            framework=framework_name,
            parent_id=categories_map[sub_data['category']]
        )
        db.add(subcategory)
        subcategory_count += 1
    
    db.commit()
    print(f"  ✓ Created {subcategory_count} subcategories")
    
    return {
        'functions': len(framework_data['functions']),
        'categories': len(framework_data['categories']),
        'subcategories': subcategory_count
    }


def load_seed_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing = db.query(models.FrameworkElement).first()
        if existing:
            print("Data already exists. Skipping seed.")
            return
        
        # Load NIST CSF 2.0
        csf_stats = load_framework(db, 'seed_data.json', 'CSF')
        
        # Load NIST Privacy Framework
        privacy_stats = load_framework(db, 'privacy_framework.json', 'Privacy')
        
        # Create default assessments
        csf_assessment = models.SecurityAssessment(
            name="CSF 2026 Internal",
            description="Internal NIST CSF 2.0 assessment for 2026"
        )
        db.add(csf_assessment)
        
        privacy_assessment = models.SecurityAssessment(
            name="Privacy Framework 2026 Internal",
            description="Internal NIST Privacy Framework assessment for 2026"
        )
        db.add(privacy_assessment)
        db.commit()
        
        print(f"\n✓ Created assessments")
        
        # Create assessment items for CSF subcategories
        csf_subcategories = db.query(models.FrameworkElement).filter(
            models.FrameworkElement.level == 'subcategory',
            models.FrameworkElement.framework == 'CSF'
        ).all()
        
        for subcategory in csf_subcategories:
            item = models.AssessmentItem(
                assessment_id=csf_assessment.id,
                framework_element_id=subcategory.id,
                current_maturity=0,
                target_maturity=3,
                notes="",
                evidence_links=[]
            )
            db.add(item)
        
        # Create assessment items for Privacy subcategories
        privacy_subcategories = db.query(models.FrameworkElement).filter(
            models.FrameworkElement.level == 'subcategory',
            models.FrameworkElement.framework == 'Privacy'
        ).all()
        
        for subcategory in privacy_subcategories:
            item = models.AssessmentItem(
                assessment_id=privacy_assessment.id,
                framework_element_id=subcategory.id,
                current_maturity=0,
                target_maturity=3,
                notes="",
                evidence_links=[]
            )
            db.add(item)
        
        db.commit()
        
        print(f"✓ Created {len(csf_subcategories)} CSF assessment items")
        print(f"✓ Created {len(privacy_subcategories)} Privacy assessment items")
        
        print(f"\n{'='*70}")
        print(f"SUCCESS! Complete frameworks loaded:")
        print(f"\n  NIST CSF 2.0:")
        print(f"    • {csf_stats['functions']} Functions")
        print(f"    • {csf_stats['categories']} Categories")
        print(f"    • {csf_stats['subcategories']} Subcategories")
        print(f"\n  NIST Privacy Framework:")
        print(f"    • {privacy_stats['functions']} Functions")
        print(f"    • {privacy_stats['categories']} Categories")
        print(f"    • {privacy_stats['subcategories']} Subcategories")
        print(f"{'='*70}")
        
    except Exception as e:
        print(f"Error loading seed data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_seed_data()
