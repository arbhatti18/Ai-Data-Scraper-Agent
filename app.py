import os
import pandas as pd
import streamlit as st
from crewai import Crew, Process
from supabase import create_client, Client
from agents import (
    get_gemini_llm,
    create_scraper_agent,
    create_extractor_agent,
    create_validator_agent,
)
from tasks import (
    create_scraping_task,
    create_extraction_task,
    create_validation_task,
)

# ============================================================
# SUPABASE CONFIGURATION
# ============================================================
SUPABASE_URL = "https://ctwerdxxyozbalmfhzgx.supabase.co"
SUPABASE_KEY = "sb_publishable_OiiCgBKD0l2o5Wp49CLWbA_C9Yk-ONe"

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_saved_leads():
    """Read saved leads from Supabase database."""
    try:
        supabase = get_supabase_client()
        response = supabase.table("b2b_leads").select("*").execute()
        data = response.data
        
        if not data:
            return pd.DataFrame()
            
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Supabase Database Error: {str(e)}")
        return pd.DataFrame()


# ============================================================
# STREAMLIT PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AI Lead Generator",
    page_icon="🎯",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================
st.title("🎯 AI Lead Generator")
st.caption("Gemini + CrewAI Multi-Agent Lead Generation System (Powered by Supabase)")


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="AIzaSy...",
        help="Your Gemini API key is used only for this session."
    )

    target_url = st.text_input(
        "Target Web Directory URL",
        placeholder="https://example.com/directory"
    )

    target_icp = st.text_input(
        "ICP Persona",
        value="CTO, Founders, Sales Heads"
    )

    st.divider()
    st.info("🔐 Connected to Supabase Cloud Database.")


# ============================================================
# MAIN EXTRACTION
# ============================================================
st.subheader("🚀 Lead Extraction")

if st.button(
    "Start Extraction",
    type="primary",
    use_container_width=True
):
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key.")
    elif not target_url:
        st.warning("⚠️ Please enter the target directory URL.")
    elif not target_url.startswith(("http://", "https://")):
        st.warning("⚠️ Please enter a valid URL starting with http:// or https://")
    else:
        try:
            # Fixed: Using the dynamic sidebar api_key instead of hardcoded string
            os.environ["GEMINI_API_KEY"] = api_key

            with st.spinner("Initializing Gemini..."):
                llm = get_gemini_llm(api_key)

            with st.spinner("Creating AI agents..."):
                scraper = create_scraper_agent(llm)
                extractor = create_extractor_agent(llm)
                validator = create_validator_agent(llm)

            scraping_task = create_scraping_task(scraper, target_url)
            extraction_task = create_extraction_task(extractor, target_icp)
            validation_task = create_validation_task(validator)

            crew = Crew(
                agents=[scraper, extractor, validator],
                tasks=[scraping_task, extraction_task, validation_task],
                process=Process.sequential,
                verbose=True
            )

            with st.spinner("🤖 AI agents are scraping, extracting and validating leads..."):
                result = crew.kickoff()

            st.success("✅ Lead extraction completed!")
            st.subheader("📊 Extraction Result")

            if hasattr(result, "raw"):
                st.write(result.raw)
            else:
                st.write(result)

        except Exception as e:
            st.error(f"❌ Execution Error: {str(e)}")


# ============================================================
# DATABASE SECTION (SUPABASE)
# ============================================================
st.divider()
st.subheader("📁 Saved Leads (Supabase)")

if st.button(
    "View Saved Leads",
    use_container_width=True
):
    df = get_saved_leads()

    if df.empty:
        st.warning("No saved leads found in Supabase yet.")
    else:
        st.success(f"Found {len(df)} saved leads from Supabase.")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv_data = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Leads as CSV",
            data=csv_data,
            file_name="validated_leads.csv",
            mime="text/csv",
            use_container_width=True
        )