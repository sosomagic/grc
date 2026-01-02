# GRC POC - NIST CSF 2.0 Assessment System

A lightweight, local web application for managing NIST Cybersecurity Framework (CSF) 2.0 assessments. Track maturity scores, notes, and evidence across the CSF hierarchy.

## Features

- **CSF Browser**: Navigate the complete NIST CSF 2.0 hierarchy (Functions → Categories → Subcategories)
- **Assessment Management**: Record current and target maturity scores (0-5 scale)
- **Evidence Tracking**: Link to external documentation (Confluence, Google Docs, etc.)
- **Summary Dashboard**: View average maturity by Function with completion statistics
- **Local-first**: SQLite database, no authentication, single assessment

## Architecture

### Backend
- **Python 3.11+** with FastAPI
- **SQLite** database via SQLAlchemy
- RESTful API with endpoints for framework browsing and assessment management

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **React Router** for navigation
- Responsive, modern UI with no external component libraries

## Project Structure

```
grc_poc/
├── backend/
│   ├── main.py           # FastAPI application & endpoints
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database connection
│   ├── config.py         # Configuration settings
│   ├── seed_db.py        # Database seeding script
│   ├── seed_data.json    # NIST CSF 2.0 framework data
│   └── requirements.txt  # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── components/   # React components
    │   ├── pages/        # Page components
    │   ├── api.ts        # API client
    │   ├── types.ts      # TypeScript types
    │   └── App.tsx       # Main app component
    ├── package.json
    └── vite.config.ts
```

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database with NIST CSF 2.0 data:
```bash
python seed_db.py
```

5. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Usage

### CSF Browser Page
1. Browse the NIST CSF 2.0 hierarchy in the left panel
2. Click on any subcategory to view details
3. Edit maturity scores (0-5 scale):
   - **0**: Not Implemented
   - **1**: Initial
   - **2**: Developing
   - **3**: Defined
   - **4**: Managed
   - **5**: Optimized
4. Add notes and evidence links
5. Click "Save Assessment" to persist changes

### Summary Page
- View average maturity scores by Function
- Track completion percentage
- Compare current vs. target maturity levels

## API Endpoints

- `GET /framework-elements` - Get complete framework tree
- `GET /assessment-items?assessment_id=1` - Get all assessment items
- `GET /assessment-items/{id}` - Get specific assessment item
- `PATCH /assessment-items/{id}` - Update assessment item
- `GET /summary?assessment_id=1` - Get summary statistics

## Database Schema

### FrameworkElement
- Stores NIST CSF 2.0 structure
- Hierarchical: Functions → Categories → Subcategories

### SecurityAssessment
- Single assessment: "CSF 2026 Internal"

### AssessmentItem
- Links subcategories to assessments
- Stores maturity scores, notes, and evidence

## Out of Scope (v0.1)

- Risk register / findings management
- File upload capabilities
- User authentication / multi-user support
- Multiple assessments
- Third-party integrations

## Development

### Build for Production

Backend:
```bash
# No build needed, deploy with uvicorn or gunicorn
```

Frontend:
```bash
npm run build
# Outputs to frontend/dist/
```

### Adding More Framework Data

Edit `backend/seed_data.json` and `backend/seed_db.py` to add more categories and subcategories, then re-run:
```bash
python seed_db.py
```

## License

This is a proof-of-concept project. Adjust licensing as needed for your organization.

## Support

For issues or questions, please contact your development team.
# grc
