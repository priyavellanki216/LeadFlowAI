# LeadFlow AI
### AI-Powered Lead Management & Follow-Up Automation System

LeadFlow AI is a Python-based application that uses Google's Gemini API to analyse customer enquiries, identify potential business opportunities, prioritise leads, and generate personalised follow-up email drafts.

The application combines a Streamlit interface, SQLite database, and AI-powered workflows to help organise customer enquiries and support consistent follow-up management.

## Project Overview

Managing customer enquiries manually can make it difficult to understand customer requirements, identify promising opportunities, and prepare relevant follow-ups.

LeadFlow AI addresses this workflow through a central application that allows users to:

- Capture and store customer enquiries.
- Analyse enquiries using Google Gemini.
- Identify customer intent and enquiry category.
- Assign Hot, Warm, or Cold lead priorities.
- Explain priority decisions using enquiry evidence.
- Identify missing customer information.
- Generate personalised follow-up email drafts.
- Search, filter, edit, and manage leads through a dashboard.
- Maintain a history of generated follow-up drafts.

**Important:** AI-generated content is provided as a draft for human review. The application does not automatically send emails.

## Key Features

### 1. Customer Enquiry Management

- Capture customer name, email address, company, and enquiry.
- Validate required fields and basic email format.
- Store submitted enquiries in SQLite.
- Preserve submitted leads even when AI analysis is unsuccessful.

### 2. AI-Powered Lead Analysis

Gemini analyses the original customer enquiry and produces structured information:

- **Category:** Software, Healthcare Technology, Automation, Pricing, Support, or Other.
- **Summary:** A concise description of the customer's requirements.
- **Intent:** The customer's apparent interest or business objective.
- **Priority:** Hot, Warm, or Cold.
- **Reasoning:** Evidence supporting the assigned priority.
- **Missing information:** Details that may need clarification.

The application validates the generated response against a Pydantic schema before using it.

### 3. Personalised Follow-Up Draft Generation

- Generate context-aware follow-up email drafts.
- Use the original enquiry and available AI analysis as context.
- Include a relevant subject line and professional email structure.
- Avoid unsupported product claims, prices, timelines, or commitments.
- Save generated drafts in the database.
- Regenerate drafts when required.
- Preserve earlier drafts through follow-up history.

Generated drafts are displayed for human review and are not automatically emailed.

### 4. Lead Dashboard and Management

- Display stored customer enquiries.
- Search leads by customer name, email, or company.
- Filter leads by priority, category, and status.
- View customer information and AI analysis.
- Edit customer information.
- Manage lead statuses:
  - New
  - Contacted
  - Qualified
  - Converted
  - Lost
- Review saved follow-up drafts and previous draft history.

### 5. AI Failure Handling and Reliability

- Separate lead persistence from AI analysis.
- Preserve submitted enquiries when AI analysis fails.
- Retry eligible API requests using configured retry handling.
- Use a fallback model for eligible API failures.
- Validate AI-generated JSON and required fields.
- Handle follow-up generation failures without treating an unsaved draft as successful.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| Generative AI | Google Gemini API |
| Gemini SDK | google-genai |
| Data validation | Pydantic |
| Database | SQLite |
| Data processing | Pandas |
| Environment configuration | python-dotenv |
| Automated testing | Pytest |
| Development environment | Visual Studio Code |

## Project Structure

```text
LeadFlowAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   └── db.py
│
├── modules/
│   ├── __init__.py
│   ├── ai_service.py
│   └── lead_service.py
│
├── prompts/
│   └── prompt_log.md
│
└── tests/
    ├── test_database.py
    ├── test_ai_service.py
    └── test_lead_service.py
```

The `.env` file, Python virtual environment, and local SQLite database are maintained locally and excluded from Git.

## Installation and Setup

### Prerequisites

- Python 3.12 or a compatible Python 3 version.
- A Google Gemini API key.
- Internet access for Gemini API requests.
- Git.
- Windows PowerShell or another terminal.

### 1. Clone the repository

```powershell
git clone https://github.com/priyavellanki216/LeadFlowAI.git
cd LeadFlowAI
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own Gemini API key.

**Security:** Never commit `.env` or expose API credentials in source code, documentation, screenshots, or public repositories.

### 5. Run the application

```powershell
python -m streamlit run app.py
```

Open the local Streamlit URL displayed in your terminal.

## Application Workflow

1. Enter customer details and the original enquiry.
2. Submit the enquiry through the Streamlit interface.
3. Validate and save the lead in SQLite.
4. Send the enquiry to Gemini for analysis.
5. Validate and persist the structured AI analysis.
6. Review the category, summary, intent, priority, reasoning, and missing information.
7. Generate a personalised follow-up email draft.
8. Save and review the generated draft.
9. Search, filter, edit, and update the lead's status through the dashboard.

## Prompt Engineering and Iterative Improvement

Prompt engineering is a central part of this project.

The implementation uses separate prompts for lead analysis and follow-up email generation.

Key design decisions include:

- Grounding analysis in the customer's original enquiry.
- Treating customer-provided text as untrusted input.
- Instructing the model not to follow embedded instructions.
- Restricting categories and priority values.
- Requiring evidence-based priority reasoning.
- Preventing invented budgets, product features, prices, timelines, or guarantees.
- Keeping internal lead priority and AI reasoning out of customer-facing emails.
- Requiring concise, professionally structured follow-up drafts.

The prompt development history, refinements, and evaluation notes are documented in:

`prompts/prompt_log.md`

## Automated Testing

The project includes automated tests for the core application components.

Run the complete test suite from the project root:

```powershell
python -m pytest tests -v
```

Compile-check the main application modules:

```powershell
python -m py_compile app.py database\db.py modules\ai_service.py modules\lead_service.py
```

The automated tests cover the database, AI service, and lead-processing functionality. Tests should be run in the configured Python environment with the project's dependencies installed.

## Error Handling and Data Integrity

LeadFlow AI is designed to preserve important customer information even when an external AI request fails.

The lead-processing workflow:

1. Saves the customer enquiry.
2. Attempts AI analysis.
3. Validates the returned response.
4. Stores the analysis separately.
5. Reports AI or persistence failures without silently treating them as successful operations.

This separation helps prevent an AI service failure from automatically discarding an already submitted lead.

## Security and Responsible AI Considerations

- API credentials are loaded through environment variables.
- `.env` is excluded from Git tracking.
- The local database is excluded from the public repository.
- Customer enquiries are treated as untrusted input in AI prompts.
- Structured AI responses are validated before use.
- AI-generated customer communication requires human review.
- The application does not automatically send emails.

## Current Limitations

- AI functionality depends on Gemini API availability and valid credentials.
- AI-generated analysis may require human review.
- Follow-up emails are generated and stored as drafts; automatic email delivery is not implemented.
- The application currently uses a local SQLite database.
- The project is a development prototype and is not presented as a production-deployed service.

## Project Links

**GitHub Repository:**  
https://github.com/priyavellanki216/LeadFlowAI

**Prompt Documentation:**  
`prompts/prompt_log.md`

**Technology:** Python, Streamlit, SQLite, Google Gemini API

## Project Objective

LeadFlow AI demonstrates the practical application of generative AI, prompt engineering, Python development, structured response validation, database integration, and workflow automation to address a real-world business problem.

The goal is to make customer enquiry management more organised and help users prepare relevant, context-aware follow-ups while keeping important decisions under human review.

---

**Developed as an AI application project by Lakshmi Priya.**
