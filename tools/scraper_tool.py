from crewai.tools import tool
import httpx
from bs4 import BeautifulSoup

class PlaywrightScraperTool:
    @tool("Scrape Webpage Content")
    def scrape_url(url: str) -> str:
        """Scrapes the raw text content from a given URL."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = httpx.get(url, headers=headers, timeout=30.0, follow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                for script in soup(["script", "style"]):
                    script.extract()
                return soup.get_text(separator="\n", strip=True)[:10000]
            else:
                return f"Failed to fetch URL. Status code: {response.status_code}"
        except Exception as e:
            return f"Error scraping URL: {str(e)}"