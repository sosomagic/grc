from sqlalchemy.orm import Session
from app.models import FrameworkElement, SecurityAssessment, AssessmentItem


def get_nist_csf_data():
    """
    NIST CSF 2.0 Framework Data
    Functions → Categories → Subcategories
    """
    return [
        # IDENTIFY Function
        {
            "code": "ID",
            "title": "Identify",
            "description": "Develop an organizational understanding to manage cybersecurity risk to systems, people, assets, data, and capabilities.",
            "level": "function",
            "parent_id": None,
            "children": [
                {
                    "code": "ID.AM",
                    "title": "Asset Management",
                    "description": "The data, personnel, devices, systems, and facilities that enable the organization to achieve business purposes are identified and managed consistent with their relative importance to organizational objectives and the organization's risk strategy.",
                    "level": "category",
                    "children": [
                        {
                            "code": "ID.AM-01",
                            "title": "Inventories",
                            "description": "Inventories of hardware managed by the organization are maintained",
                            "level": "subcategory"
                        },
                        {
                            "code": "ID.AM-02",
                            "title": "Software Inventory",
                            "description": "Inventories of software, services, and systems managed by the organization are maintained",
                            "level": "subcategory"
                        },
                        {
                            "code": "ID.AM-03",
                            "title": "Data Flow Mapping",
                            "description": "Representations of the organization's authorized network communication and internal and external network data flows are maintained",
                            "level": "subcategory"
                        }
                    ]
                },
                {
                    "code": "ID.RA",
                    "title": "Risk Assessment",
                    "description": "The organization understands the cybersecurity risk to organizational operations, organizational assets, and individuals.",
                    "level": "category",
                    "children": [
                        {
                            "code": "ID.RA-01",
                            "title": "Asset Vulnerabilities",
                            "description": "Asset vulnerabilities are identified and documented",
                            "level": "subcategory"
                        },
                        {
                            "code": "ID.RA-02",
                            "title": "Threat Intelligence",
                            "description": "Cyber threat intelligence is received from information sharing forums and sources",
                            "level": "subcategory"
                        }
                    ]
                }
            ]
        },
        # PROTECT Function
        {
            "code": "PR",
            "title": "Protect",
            "description": "Develop and implement appropriate safeguards to ensure delivery of critical infrastructure services.",
            "level": "function",
            "parent_id": None,
            "children": [
                {
                    "code": "PR.AC",
                    "title": "Identity Management, Authentication and Access Control",
                    "description": "Access to physical and logical assets and associated facilities is limited to authorized users, processes, and devices.",
                    "level": "category",
                    "children": [
                        {
                            "code": "PR.AC-01",
                            "title": "Identity Management",
                            "description": "Identities and credentials are issued, managed, verified, revoked, and audited for authorized devices, users and processes",
                            "level": "subcategory"
                        },
                        {
                            "code": "PR.AC-03",
                            "title": "Remote Access",
                            "description": "Remote access is managed",
                            "level": "subcategory"
                        }
                    ]
                },
                {
                    "code": "PR.DS",
                    "title": "Data Security",
                    "description": "Information and records (data) are managed consistent with the organization's risk strategy to protect the confidentiality, integrity, and availability of information.",
                    "level": "category",
                    "children": [
                        {
                            "code": "PR.DS-01",
                            "title": "Data-at-rest",
                            "description": "Data-at-rest is protected",
                            "level": "subcategory"
                        },
                        {
                            "code": "PR.DS-02",
                            "title": "Data-in-transit",
                            "description": "Data-in-transit is protected",
                            "level": "subcategory"
                        }
                    ]
                }
            ]
        },
        # DETECT Function
        {
            "code": "DE",
            "title": "Detect",
            "description": "Develop and implement appropriate activities to identify the occurrence of a cybersecurity event.",
            "level": "function",
            "parent_id": None,
            "children": [
                {
                    "code": "DE.AE",
                    "title": "Anomalies and Events",
                    "description": "Anomalous activity is detected and the potential impact of events is understood.",
                    "level": "category",
                    "children": [
                        {
                            "code": "DE.AE-02",
                            "title": "Event Analysis",
                            "description": "Detected events are analyzed to understand attack targets and methods",
                            "level": "subcategory"
                        }
                    ]
                },
                {
                    "code": "DE.CM",
                    "title": "Security Continuous Monitoring",
                    "description": "The information system and assets are monitored to identify cybersecurity events and verify the effectiveness of protective measures.",
                    "level": "category",
                    "children": [
                        {
                            "code": "DE.CM-01",
                            "title": "Network Monitoring",
                            "description": "Networks and network services are monitored to find potentially adverse events",
                            "level": "subcategory"
                        }
                    ]
                }
            ]
        },
        # RESPOND Function
        {
            "code": "RS",
            "title": "Respond",
            "description": "Develop and implement appropriate activities to take action regarding a detected cybersecurity incident.",
            "level": "function",
            "parent_id": None,
            "children": [
                {
                    "code": "RS.MA",
                    "title": "Incident Management",
                    "description": "Organizational response activities are coordinated with internal and external stakeholders.",
                    "level": "category",
                    "children": [
                        {
                            "code": "RS.MA-01",
                            "title": "Incident Response Plan",
                            "description": "The incident response plan is executed in coordination with relevant third parties once an incident is declared",
                            "level": "subcategory"
                        }
                    ]
                }
            ]
        },
        # RECOVER Function
        {
            "code": "RC",
            "title": "Recover",
            "description": "Develop and implement appropriate activities to maintain plans for resilience and to restore capabilities or services that were impaired due to a cybersecurity incident.",
            "level": "function",
            "parent_id": None,
            "children": [
                {
                    "code": "RC.RP",
                    "title": "Recovery Planning",
                    "description": "Recovery processes and procedures are executed and maintained to ensure restoration of systems or assets affected by cybersecurity incidents.",
                    "level": "category",
                    "children": [
                        {
                            "code": "RC.RP-01",
                            "title": "Recovery Plan",
                            "description": "The recovery portion of the incident response plan is executed once initiated from the incident response process",
                            "level": "subcategory"
                        }
                    ]
                }
            ]
        }
    ]


def insert_framework_element(db: Session, element_data: dict, parent_id: int = None):
    """Recursively insert framework elements"""
    children_data = element_data.pop("children", [])
    
    element = FrameworkElement(
        code=element_data["code"],
        title=element_data["title"],
        description=element_data.get("description"),
        level=element_data["level"],
        parent_id=parent_id
    )
    db.add(element)
    db.flush()
    
    for child_data in children_data:
        insert_framework_element(db, child_data, element.id)
    
    return element


def initialize_data(db: Session):
    """Initialize database with NIST CSF 2.0 data and default assessment"""
    
    # Check if data already exists
    existing = db.query(FrameworkElement).first()
    if existing:
        print("Database already initialized")
        return
    
    print("Initializing NIST CSF 2.0 data...")
    
    # Insert framework elements
    csf_data = get_nist_csf_data()
    for function_data in csf_data:
        insert_framework_element(db, function_data)
    
    # Create default assessment
    assessment = SecurityAssessment(
        name="CSF 2026 Internal",
        description="Internal cybersecurity framework assessment for 2026"
    )
    db.add(assessment)
    db.flush()
    
    # Create assessment items for all subcategories
    subcategories = db.query(FrameworkElement).filter(
        FrameworkElement.level == "subcategory"
    ).all()
    
    for subcategory in subcategories:
        item = AssessmentItem(
            assessment_id=assessment.id,
            framework_element_id=subcategory.id,
            current_maturity=0,
            target_maturity=3,
            notes="",
            evidence_links=""
        )
        db.add(item)
    
    db.commit()
    print(f"Initialized {len(subcategories)} subcategories and 1 assessment")
