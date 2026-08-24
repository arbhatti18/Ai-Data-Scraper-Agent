from crewai.tools import tool
from supabase import create_client

SUPABASE_URL = "https://ctwerdxxyozbalmfhzgx.supabase.co"
SUPABASE_KEY = "sb_publishable_OiiCgBKD0l2o5Wp49CLWbA_C9Yk-ONe"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class LeadStorageTool:
    @tool("Save Validated Lead to Database")
    def save_lead(company_name: str, lead_name: str, email: str, role: str, status: str) -> str:
        """Saves the validated B2B lead to the Supabase database table 'b2b_leads'."""
        try:
            data = {
                "company_name": company_name,
                "lead_name": lead_name,
                "email": email,
                "role": role,
                "status": status
            }
            supabase.table("b2b_leads").insert(data).execute()
            return f"Successfully saved lead for {company_name} to Supabase!"
        except Exception as e:
            return f"Error saving lead to Supabase: {str(e)}"