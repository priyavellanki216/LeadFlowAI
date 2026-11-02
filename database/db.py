
import json
import sqlite3
from pathlib import Path


# Database file location
DB_PATH = Path(__file__).resolve().parent / "leads.db"


def get_connection():
    """Create and return a database connection."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_db():
    """Create database tables and safely update existing databases."""

    connection = get_connection()

    try:
        # Create the leads table if it does not exist.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                company TEXT,
                enquiry TEXT NOT NULL,
                category TEXT DEFAULT 'Unclassified',
                priority TEXT DEFAULT 'Unclassified',
                ai_summary TEXT,
                ai_reasoning TEXT,
                followup_draft TEXT,
                status TEXT DEFAULT 'New',
                follow_up_date TEXT,
                created_at TEXT DEFAULT
                    (datetime('now', 'localtime'))
            )
        """)

        # Check existing columns before modifying the table.
        existing_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(leads)"
            ).fetchall()
        }

        # Add AI intent column if it does not exist.
        if "ai_intent" not in existing_columns:
            connection.execute("""
                ALTER TABLE leads
                ADD COLUMN ai_intent TEXT
            """)

        # Add missing information column if it does not exist.
        if "missing_information" not in existing_columns:
            connection.execute("""
                ALTER TABLE leads
                ADD COLUMN missing_information TEXT
            """)

        # Create follow-up history table.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS follow_up_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                draft TEXT NOT NULL,
                action TEXT DEFAULT 'Draft created',
                created_at TEXT DEFAULT
                    (datetime('now', 'localtime')),
                FOREIGN KEY (lead_id)
                    REFERENCES leads(id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_lead(customer_name, email, company, enquiry):
    """Save a new customer enquiry in the database."""

    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO leads (
                customer_name,
                email,
                company,
                enquiry
            )
            VALUES (?, ?, ?, ?)
        """, (
            customer_name,
            email,
            company,
            enquiry
        ))

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def update_lead_analysis(lead_id, analysis):
    """Save Gemini AI analysis against an existing lead."""

    required_fields = {
        "category",
        "summary",
        "intent",
        "priority",
        "reasoning",
        "missing_information"
    }

    if not isinstance(analysis, dict):
        raise ValueError("AI analysis must be a dictionary.")

    if not required_fields.issubset(analysis.keys()):
        raise ValueError("AI analysis is missing required fields.")

    if not isinstance(analysis["missing_information"], list):
        raise ValueError(
            "Missing information must be provided as a list."
        )

    # Convert the missing-information list into JSON text.
    missing_information_json = json.dumps(
        analysis["missing_information"],
        ensure_ascii=False
    )

    connection = get_connection()

    try:
        cursor = connection.execute("""
            UPDATE leads
            SET
                category = ?,
                priority = ?,
                ai_summary = ?,
                ai_reasoning = ?,
                ai_intent = ?,
                missing_information = ?
            WHERE id = ?
        """, (
            analysis["category"],
            analysis["priority"],
            analysis["summary"],
            analysis["reasoning"],
            analysis["intent"],
            missing_information_json,
            lead_id
        ))

        if cursor.rowcount == 0:
            raise ValueError(
                f"No lead found with ID {lead_id}."
            )

        connection.commit()

        return True

    finally:
        connection.close()


def get_recent_leads():
    """Retrieve all leads with AI analysis, newest first."""

    connection = get_connection()

    try:
        leads = connection.execute("""
            SELECT
                id,
                customer_name,
                email,
                company,
                enquiry,
                category,
                priority,
                ai_summary,
                ai_reasoning,
                ai_intent,
                missing_information,
                followup_draft,
                status,
                follow_up_date,
                created_at
            FROM leads
            ORDER BY id DESC
        """).fetchall()

        return leads

    finally:
        connection.close()


def save_followup_draft(lead_id, draft):
    """
    Save a generated follow-up draft to the lead record
    and create an entry in follow-up history.
    """

    if not draft or not draft.strip():
        raise ValueError("Follow-up draft cannot be empty.")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Update the latest follow-up draft for this lead
        cursor.execute(
            """
            UPDATE leads
            SET followup_draft = ?
            WHERE id = ?
            """,
            (draft.strip(), lead_id)
        )

        # Check whether the lead exists
        if cursor.rowcount == 0:
            raise ValueError(
                f"No lead found with ID {lead_id}."
            )

        # Record this generated draft in history
        cursor.execute(
            """
            INSERT INTO follow_up_history
            (lead_id, draft, action)
            VALUES (?, ?, ?)
            """,
            (lead_id, draft.strip(), "Draft created")
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_followup_history(lead_id):
    """
    Retrieve follow-up history for a specific lead,
    with the newest entry first.
    """

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, lead_id, draft, action, created_at
            FROM follow_up_history
            WHERE lead_id = ?
            ORDER BY id DESC
            """,
            (lead_id,)
        )

        history = cursor.fetchall()

        return history

    finally:
        conn.close()
