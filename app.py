
import json
import logging
import re

import streamlit as st

from database.db import (
    initialize_db,
    save_lead,
    update_lead_analysis,
    get_recent_leads,
    save_followup_draft,
    get_followup_history,
)

from modules.ai_service import (
    analyze_lead,
    generate_followup_draft,
)


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="LeadFlow AI",
    page_icon="📊",
    layout="wide",
)

# Initialize the database.
try:
    initialize_db()
except Exception:
    logger.exception("Database initialization failed.")
    st.error(
        "LeadFlow AI could not initialize its database. "
        "Please check the application configuration."
    )
    st.stop()


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("📊 LeadFlow AI")

st.subheader(
    "AI-Powered Lead Management & Follow-Up Automation"
)

st.write(
    "Capture customer enquiries, analyse potential leads "
    "using Gemini AI, and manage personalised follow-up drafts "
    "from one dashboard."
)

st.caption(
    "AI-generated results are intended to support human review "
    "and decision-making."
)

st.divider()


# --------------------------------------------------
# CUSTOMER ENQUIRY FORM
# --------------------------------------------------

st.header("Customer Enquiry Form")

with st.form("lead_submission_form", clear_on_submit=True):

    customer_name = st.text_input(
        "Customer Name *",
        placeholder="Enter customer name",
    )

    email = st.text_input(
        "Email Address *",
        placeholder="example@email.com",
    )

    company = st.text_input(
        "Company Name",
        placeholder="Enter company name (optional)",
    )

    enquiry = st.text_area(
        "Customer Enquiry *",
        placeholder="Describe the customer's enquiry...",
        height=150,
    )

    submitted = st.form_submit_button(
        "Submit Enquiry & Analyse with AI",
        use_container_width=True,
    )

    if submitted:

        # ------------------------------------------
        # INPUT VALIDATION
        # ------------------------------------------

        customer_name = customer_name.strip()
        email = email.strip()
        company = company.strip()
        enquiry = enquiry.strip()

        if not customer_name:

            st.error("Please enter the customer's name.")

        elif not email:

            st.error("Please enter an email address.")

        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email,
        ):

            st.error("Please enter a valid email address.")

        elif not enquiry:

            st.error("Please enter the customer's enquiry.")

        else:

            lead_id = None

            # ------------------------------------------
            # STEP 1: SAVE THE CUSTOMER ENQUIRY
            # ------------------------------------------

            try:

                lead_id = save_lead(
                    customer_name,
                    email,
                    company,
                    enquiry,
                )

                st.success(
                    f"Enquiry saved successfully! Lead ID: {lead_id}"
                )

            except Exception:

                logger.exception("Unable to save customer enquiry.")

                st.error(
                    "Unable to save the customer enquiry. "
                    "Please try again."
                )

            # ------------------------------------------
            # STEP 2: ANALYSE THE SAVED ENQUIRY
            # ------------------------------------------

            if lead_id is not None:

                try:

                    with st.spinner(
                        "Gemini AI is analysing the customer enquiry..."
                    ):

                        analysis = analyze_lead(
                            customer_name,
                            company,
                            enquiry,
                        )

                        # ----------------------------------
                        # STEP 3: SAVE AI ANALYSIS
                        # ----------------------------------

                        update_lead_analysis(
                            lead_id,
                            analysis,
                        )

                    st.success(
                        "Gemini AI analysis completed and saved successfully!"
                    )

                    st.subheader("AI Analysis Result")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Lead Priority",
                            analysis["priority"],
                        )

                    with col2:

                        st.metric(
                            "Lead Category",
                            analysis["category"],
                        )

                    st.write("**AI Summary**")
                    st.write(analysis["summary"])

                    st.write("**Customer Intent**")
                    st.write(analysis["intent"])

                    st.write("**AI Reasoning**")
                    st.write(analysis["reasoning"])

                    st.write("**Missing Information**")

                    missing_information = analysis.get(
                        "missing_information",
                        [],
                    )

                    if missing_information:

                        for item in missing_information:
                            st.write(f"- {item}")

                    else:

                        st.write(
                            "No missing information identified."
                        )

                except Exception:

                    logger.exception(
                        "AI analysis failed for Lead ID %s.",
                        lead_id,
                    )

                    st.warning(
                        f"Lead #{lead_id} was saved successfully, "
                        "but AI analysis could not be completed. "
                        "You can retry the analysis from the dashboard."
                    )


st.divider()


# --------------------------------------------------
# LEAD DASHBOARD
# --------------------------------------------------

st.header("Submitted Customer Enquiries")

try:

    leads = get_recent_leads()

except Exception:

    logger.exception("Unable to retrieve customer enquiries.")

    st.error(
        "Unable to load the customer enquiry dashboard. "
        "Please refresh the application."
    )

    leads = None


if leads is not None and leads:

    st.write(
        f"Total enquiries received: **{len(leads)}**"
    )

    # ----------------------------------------------
    # DASHBOARD SUMMARY METRICS
    # ----------------------------------------------

    hot_count = sum(
        1 for lead in leads
        if lead["priority"] == "Hot"
    )

    warm_count = sum(
        1 for lead in leads
        if lead["priority"] == "Warm"
    )

    cold_count = sum(
        1 for lead in leads
        if lead["priority"] == "Cold"
    )

    unclassified_count = sum(
        1 for lead in leads
        if lead["priority"] not in ("Hot", "Warm", "Cold")
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🔥 Hot Leads", hot_count)
    col2.metric("🟡 Warm Leads", warm_count)
    col3.metric("🔵 Cold Leads", cold_count)
    col4.metric("⚪ Unclassified", unclassified_count)

    st.divider()

    # ----------------------------------------------
    # INDIVIDUAL LEAD DETAILS
    # ----------------------------------------------

    for lead in leads:

        lead_id = lead["id"]

        priority = lead["priority"] or "Unclassified"

        with st.expander(
            f"Lead #{lead_id} – "
            f"{lead['customer_name']} – {priority}"
        ):

            st.write("**Customer:**", lead["customer_name"])

            st.write("**Email:**", lead["email"])

            st.write(
                "**Company:**",
                lead["company"] or "Not provided",
            )

            st.write("**Original Enquiry:**")
            st.write(lead["enquiry"])

            st.divider()

            # ------------------------------------------
            # AI LEAD ANALYSIS
            # ------------------------------------------

            st.subheader("AI Lead Analysis")

            st.write(
                "**Category:**",
                lead["category"] or "Not analysed",
            )

            st.write("**Priority:**", priority)

            # Check whether AI analysis is available.
            if lead["ai_summary"]:

                st.write("**AI Summary:**")
                st.write(lead["ai_summary"])

                st.write("**Customer Intent:**")

                st.write(
                    lead["ai_intent"] or "Not available"
                )

                st.write("**AI Reasoning:**")

                st.write(
                    lead["ai_reasoning"] or "Not available"
                )

                st.write("**Missing Information:**")

                if lead["missing_information"]:

                    try:

                        missing_items = json.loads(
                            lead["missing_information"]
                        )

                        if isinstance(missing_items, list):

                            for item in missing_items:
                                st.write(f"- {item}")

                        else:

                            st.write(
                                "Stored missing-information data "
                                "has an unexpected format."
                            )

                    except (json.JSONDecodeError, TypeError):

                        st.write(
                            "Stored missing-information data "
                            "could not be displayed."
                        )

                else:

                    st.write(
                        "No missing information recorded."
                    )

                # --------------------------------------
                # AI FOLLOW-UP GENERATION
                # --------------------------------------

                st.divider()

                st.subheader("✉️ AI Follow-Up Automation")

                st.caption(
                    "Generate a personalised follow-up email "
                    "using the customer's original enquiry "
                    "and AI analysis."
                )

                existing_draft = lead["followup_draft"]

                generate_button_label = (
                    "Regenerate Follow-Up Draft"
                    if existing_draft
                    else "Generate Follow-Up Draft"
                )

                if st.button(
                    generate_button_label,
                    key=f"generate_followup_{lead_id}",
                    use_container_width=True,
                ):

                    followup_draft = None

                    # ----------------------------------
                    # STEP 1: GENERATE THE DRAFT
                    # ----------------------------------

                    try:

                        with st.spinner(
                            "Gemini AI is generating a personalised "
                            "follow-up email..."
                        ):

                            followup_draft = generate_followup_draft(
                                customer_name=lead["customer_name"],
                                company=lead["company"] or "",
                                enquiry=lead["enquiry"],
                                ai_summary=lead["ai_summary"],
                                intent=lead["ai_intent"] or "",
                                priority=priority,
                            )

                    except Exception:

                        logger.exception(
                            "Follow-up generation failed for Lead ID %s.",
                            lead_id,
                        )

                        st.error(
                            "Unable to generate the follow-up draft. "
                            "Please try again later. "
                            "Your previously saved draft remains available."
                        )

                    # ----------------------------------
                    # STEP 2: SAVE THE GENERATED DRAFT
                    # ----------------------------------

                    if followup_draft is not None:

                        try:

                            save_followup_draft(
                                lead_id,
                                followup_draft,
                            )

                            st.success(
                                "Follow-up draft generated and saved successfully!"
                            )

                            # Refresh the dashboard after successful saving.
                            st.rerun()

                        except Exception:

                            logger.exception(
                                "Unable to save follow-up draft "
                                "for Lead ID %s.",
                                lead_id,
                            )

                            st.error(
                                "The follow-up draft could not be saved. "
                                "Please try again. "
                                "Your previously saved draft remains available."
                            )

                # --------------------------------------
                # DISPLAY THE LATEST SAVED DRAFT
                # --------------------------------------

                if existing_draft:

                    st.write("**Latest Saved Follow-Up Draft**")

                    st.caption(
                        "This is an AI-generated draft for human review. "
                        "It has not been sent to the customer."
                    )

                    st.text_area(
                        "Generated Email",
                        value=existing_draft,
                        height=250,
                        disabled=True,
                        key=f"saved_followup_{lead_id}",
                    )

                else:

                    st.info(
                        "No follow-up draft has been generated "
                        "for this lead yet."
                    )

                # --------------------------------------
                # FOLLOW-UP HISTORY
                # --------------------------------------

                try:

                    history = get_followup_history(lead_id)

                    with st.expander(
                        f"View Follow-Up History ({len(history)})"
                    ):

                        if history:

                            for index, item in enumerate(
                                history,
                                start=1,
                            ):

                                st.write(
                                    f"**History Entry {index}**"
                                )

                                st.caption(
                                    f"Action: {item['action']} | "
                                    f"Created: {item['created_at']}"
                                )

                                st.text_area(
                                    f"Saved Draft {index}",
                                    value=item["draft"],
                                    height=200,
                                    disabled=True,
                                    key=(
                                        f"history_{lead_id}_"
                                        f"{item['id']}"
                                    ),
                                )

                                if index < len(history):
                                    st.divider()

                        else:

                            st.info(
                                "No follow-up history is available "
                                "for this lead."
                            )

                except Exception:

                    logger.exception(
                        "Unable to retrieve follow-up history "
                        "for Lead ID %s.",
                        lead_id,
                    )

                    st.warning(
                        "Unable to retrieve follow-up history "
                        "for this lead."
                    )

            else:

                # --------------------------------------
                # RETRY AI ANALYSIS
                # --------------------------------------

                st.info(
                    "AI analysis is not available for this lead yet. "
                    "Follow-up generation will become available "
                    "after successful analysis."
                )

                if st.button(
                    f"Retry AI Analysis for Lead #{lead_id}",
                    key=f"retry_ai_{lead_id}",
                ):

                    try:

                        with st.spinner(
                            "Gemini AI is analysing this saved enquiry..."
                        ):

                            analysis = analyze_lead(
                                lead["customer_name"],
                                lead["company"] or "",
                                lead["enquiry"],
                            )

                            update_lead_analysis(
                                lead_id,
                                analysis,
                            )

                        st.success(
                            "AI analysis completed and saved successfully!"
                        )

                        # Refresh the dashboard to show updated analysis.
                        st.rerun()

                    except Exception:

                        logger.exception(
                            "AI analysis retry failed for Lead ID %s.",
                            lead_id,
                        )

                        st.error(
                            "AI analysis is still unavailable. "
                            "Your saved enquiry has not been lost. "
                            "Please try again later."
                        )

            st.divider()

            st.write(
                "**Status:**",
                lead["status"] or "Not specified",
            )

            st.write(
                "**Created:**",
                lead["created_at"],
            )


elif leads is not None:

    st.info(
        "No customer enquiries have been submitted yet. "
        "Use the form above to add your first lead."
    )


# --------------------------------------------------
# APPLICATION FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "LeadFlow AI | Gemini-Powered Lead Management | "
    "AI-Assisted Workflow Automation"
)
