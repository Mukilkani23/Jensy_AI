import httpx
from bs4 import BeautifulSoup


async def scrape_college_curriculum(url: str) -> dict:
    """
    Scrape curriculum/syllabus from an autonomous college website.
    Returns structured curriculum data.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract college name
        title = soup.find("title")
        college_name = title.get_text(strip=True) if title else "Unknown College"

        # Try to find curriculum/syllabus tables
        tables = soup.find_all("table")
        curriculum_data = {
            "college_name": college_name,
            "source_url": url,
            "semesters": {}
        }

        # Look for syllabus-related links
        syllabus_links = []
        for link in soup.find_all("a", href=True):
            text = link.get_text(strip=True).lower()
            if any(kw in text for kw in ["syllabus", "curriculum", "regulation", "scheme"]):
                href = link["href"]
                if not href.startswith("http"):
                    from urllib.parse import urljoin
                    href = urljoin(url, href)
                syllabus_links.append({"text": link.get_text(strip=True), "url": href})

        curriculum_data["syllabus_links"] = syllabus_links

        # Extract table data if available
        for i, table in enumerate(tables[:5]):  # Limit to first 5 tables
            rows = table.find_all("tr")
            table_data = []
            for row in rows:
                cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                if cells:
                    table_data.append(cells)
            if table_data:
                curriculum_data["semesters"][f"table_{i+1}"] = table_data

        return curriculum_data

    except httpx.HTTPError as e:
        raise Exception(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise Exception(f"Scraping error: {str(e)}")

