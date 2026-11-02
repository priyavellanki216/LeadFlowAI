# LeadFlow AI

**AI-Powered Lead Management & Follow-Up Automation System**

LeadFlow AI is a Python-based business automation application that helps capture customer enquiries, analyse potential leads using Google's Gemini AI, and generate personalised follow-up email drafts.

The application combines a Streamlit dashboard, an SQLite database, and Gemini-powered AI workflows to organise customer enquiries and support follow-up activities.

## Project Overview

Managing customer enquiries manually can make it difficult to organise incoming leads, understand customer requirements, and prepare timely follow-ups.

LeadFlow AI addresses this workflow by providing a central application to:

- Capture and store customer enquiries.
- Analyse enquiries using Gemini AI.
- Classify leads by category and priority.
- Identify customer intent and missing information.
- Generate personalised follow-up email drafts.
- Save generated drafts and maintain follow-up history.
- Review customer enquiries and AI analysis through a dashboard.

AI-generated content is intended for human review. The application does not automatically send emails to customers.

## Features

### 1. Customer Enquiry Management
- Capture customer name, email address, company name, and enquiry.
- Validate required fields and basic email format.
- Store submitted enquiries in an SQLite database.
- Preserve submitted enquiries independently of AI analysis.

### 2. AI-Powered Lead Analysis
- Analyse customer enquiries using Google's Gemini API.
- Identify lead category and priority.
- Generate an enquiry summary.
- Identify customer intent.
- Explain the AI assessment.
- Identify missing information that may need clarification.
- Retry AI analysis for previously saved enquiries.

### 3. AI Follow-Up Draft Generation
- Generate personalised follow-up email drafts using Gemini AI.
- Use the original customer enquiry and available AI analysis as context.
- Save generated drafts in the database.
- Regenerate drafts when required.
- Preserve earlier drafts through follow-up history.
- Display drafts for human review.

### 4. Lead Dashboard
- Display submitted customer enquiries.
- Show total enquiry count.
- Summarise Hot, Warm, Cold, and Unclassified leads.
- Display individual customer information and AI analysis.
- Review saved follow-up drafts and their history.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| AI Integration | Google Gemini API |
| AI SDK | google-genai |
| Database | SQLite |
| Data Processing | Pandas |
| Environment Configuration | python-dotenv |
| Development Environment | Visual Studio Code |

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
│   └── ai_service.py
│
├── prompts/
│   └── prompt_log.md
│
├── test_ai.py
├── test_db_analysis.py
├── test_followup.py
├── test_followup_db.py
├── test_ai_failure.py
├── test_followup_failure.py
├── test_gemini.py
├── test_gemini_alternative.py
├── verify_db.py
└── verify_leads.py
```

The `.env` file, virtual environment, and SQLite database are created and maintained locally. They are excluded from the public repository.

## Prerequisites

- Python 3.12 or compatible Python 3 version.
- A Google Gemini API key.
- Visual Studio Code or another Python development environment.
- Internet connectivity for Gemini API requests.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/priyavellanki216/LeadFlowAI
cd LeadFlowAI
```

Replace `https://github.com/priyavellanki216/LeadFlowAI` with the actual repository URL after publishing the project.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root directory:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own Gemini API key.

**Security:** Never commit your `.env` file or expose your API key in source code, screenshots, documentation, or public repositories.

### 5. Run the application

```powershell
python -m streamlit run app.py
```

Streamlit will display a local application address in the terminal. Open that address in your browser.

## Application Workflow

1. Enter customer information and the original enquiry.
2. Submit the enquiry through the Streamlit form.
3. The application validates and saves the enquiry in SQLite.
4. Gemini AI analyses the saved enquiry.
5. The AI analysis is stored against the corresponding lead.
6. Review the lead information, category, priority, summary, intent, reasoning, and missing information.
7. Generate a personalised follow-up email draft.
8. Save the draft and its history in SQLite.
9. Review previous drafts and regenerate when needed.

## Testing and Verification

The project includes individual scripts used during development to verify:

- Gemini API connectivity.
- AI lead analysis.
- Database initialization and lead persistence.
- AI analysis storage and retrieval.
- Follow-up draft generation.
- Follow-up draft storage and history retrieval.
- Lead preservation during a simulated AI analysis failure.
- Previous draft and history preservation during a simulated follow-up generation failure.

The failure-handling scripts use controlled simulated exceptions. They verify the relevant database-preservation behaviour and should not be interpreted as live Gemini outage tests.

To run an individual verification script:

```powershell
python test_ai_failure.py
```

Use the relevant test filename for other verification scripts.

## Prompt Engineering Documentation

The `prompts/prompt_log.md` file records the prompts used during development, significant refinements, observed AI responses, and evaluation notes.

It documents the iterative process used to improve AI-generated lead analysis and follow-up drafts, including efforts to reduce unsupported claims and keep generated content grounded in the customer's original enquiry.

## Limitations

- AI analysis and follow-up generation depend on Gemini API availability.
- AI-generated classifications and content may require human review.
- Email drafts are generated and stored; automatic email delivery is not implemented.
- The application currently uses a local SQLite database.
- The project is designed as a development prototype and is not presented as a production-deployed service.

## Security

- API credentials are loaded through environment variables.
- `.env` is excluded from Git tracking.
- The local SQLite database is excluded from the public repository.
- AI-generated follow-up drafts require human review before use.

## Project Objective

LeadFlow AI demonstrates how generative AI, prompt engineering, Python application development, and database integration can be combined to improve a practical business workflow.

**Project:** LeadFlow AI  
**Domain:** Technology / Business Automation  
**AI Platform:** Google Gemini  
**Interface:** Streamlit
