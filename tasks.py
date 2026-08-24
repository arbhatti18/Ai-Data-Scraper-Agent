from crewai import Task

def create_scraping_task(agent, target_url: str) -> Task:
    return Task(
        description=f"Thoroughly scrape the content, business profiles, and contact details from the target directory URL: {target_url}.",
        expected_output="Raw text content containing business directories, company names, and contact information.",
        agent=agent
    )

def create_extraction_task(agent, target_icp: str) -> Task:
    return Task(
        description=f"Analyze the scraped data and extract structured B2B leads that strictly match the Ideal Customer Profile (ICP): {target_icp}. Extract Company Name, Lead Name, Email, and Job Role.",
        expected_output="A structured list of extracted leads with company name, lead name, email, and role.",
        agent=agent
    )

def create_validation_task(agent) -> Task:
    return Task(
        description="Verify and validate the extracted leads, check email formats, ensure data accuracy, and format them for final storage.",
        expected_output="A fully validated list of clean B2B leads ready for use.",
        agent=agent
    )