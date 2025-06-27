import requests
import pandas as pd
import re
import time
import logging
import os
import random
from requests.exceptions import RequestException
from typing import Optional, List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("fighter_scraper")

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

def get_random_user_agent() -> str:
    """Return a random user agent from the list."""
    return random.choice(USER_AGENTS)

def extract_page(url: str, issue: int, division: int, page: int, max_retries: int = 5) -> Optional[pd.DataFrame]:
    """
    Extract fighter name, rank, and nationality from FightMatrix rankings page using regex

    Args:
        url (str): URL of the FightMatrix rankings page
        issue (int): Issue number
        division (int): Division number
        page (int): Page number
        max_retries (int): Maximum number of retry attempts

    Returns:
        Optional[pd.DataFrame]: DataFrame with rank, name, and nationality or None if extraction failed
    """
    # Start timing
    start_time = time.time()
    
    # Implement retry with exponential backoff
    retry_count = 0
    while retry_count <= max_retries:
        try:
            # Random delay between requests (1-5 seconds)
            if retry_count > 0:
                delay = random.uniform(2, 10) * (2 ** retry_count)
                logger.info(f"Waiting {delay:.2f} seconds before retry {retry_count}/{max_retries}")
                time.sleep(delay)
            
            # Rotate user agents
            headers = {
                "User-Agent": get_random_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.fightmatrix.com/historical-mma-rankings/",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            
            # Optional: Use proxies if needed
            # proxies = {
            #     "http": "http://your-proxy-here",
            #     "https": "https://your-proxy-here"
            # }
            
            logger.info(f"Requesting data from {url} (attempt {retry_count+1}/{max_retries+1})")
            # response = requests.get(url, headers=headers, proxies=proxies, timeout=30)  # Uncomment to use proxies
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Get the HTML content as text
                html_content = response.text
                logger.debug(f"Received {len(html_content)} bytes of HTML content")
                
                # Define regex patterns
                rank_pattern = r'class="tdRank(?:Alt)?">(\d+)</td>'
                flag_pattern = r'<img src="/images/flag/([a-zA-Z]+)\.png"'
                name_pattern = r'<a name="(.*?)"'
                
                ranks = re.findall(rank_pattern, html_content)
                flags = re.findall(flag_pattern, html_content)
                names = re.findall(name_pattern, html_content)

                logger.debug(f"Found {len(ranks)} ranks, {len(flags)} flags, and {len(names)} names")
                
                # Check if we got any data
                if len(ranks) == 0 and len(flags) == 0 and len(names) == 0:
                    logger.warning("No data found in the response, might be blocked or empty page")
                    if "Access Denied" in html_content or "Forbidden" in html_content:
                        logger.error("Access denied or forbidden response detected")
                        retry_count += 1
                        continue
                    # If it's just an empty page (no fighters for this combination), return empty DataFrame
                    return pd.DataFrame({"rank": [], "flag": [], "name": [], "issue": [], "division": [], "page": []})
                
                # Create DataFrame
                df = pd.DataFrame({"rank": ranks, "flag": flags, "name": names, "issue": [issue] * len(ranks), "division": [division] * len(ranks), "page": [page] * len(ranks)})

                execution_time = time.time() - start_time
                logger.info(f"Extraction for issue {issue}, division {division}, page {page} completed in {execution_time:.2f} seconds with {len(df)} records")
                
                return df
            
            elif response.status_code == 429:  # Too Many Requests
                logger.warning(f"Rate limited (429). Retrying after longer delay.")
                retry_count += 1
                continue
                
            else:
                logger.error(f"Failed to retrieve data: Status code {response.status_code}")
                retry_count += 1
                
        except RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            retry_count += 1
    
    logger.error(f"Max retries ({max_retries}) exceeded for {url}")
    return None

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    logger.info("Starting fighter data extraction")
    
    issues = range(141, 143)
    divisions = [1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15]
    pages = range(1, 31)
    
    # Track overall progress
    total_combinations = len(issues) * len(divisions) * len(pages)
    completed = 0
    failed = 0
    
    for issue in issues:
        for division in divisions:
            for page in pages:
                output_file = f"data/fighter_rankings_{issue}_{division}_{page}.csv"
                
                if os.path.exists(output_file):
                    logger.info(f"Skipping issue {issue}, division {division}, page {page} because it already exists")
                    completed += 1
                    continue
                
                url = f"https://www.fightmatrix.com/historical-mma-rankings/generated-historical-rankings/?RF=FM&Issue={issue}&Division={division}&Page={page}"
                df = extract_page(url, issue, division, page)

                if df is not None:
                    if not df.empty:
                        logger.info(f"Data preview:\n{df.head()}")
                        df.to_csv(output_file, index=False)
                        logger.info(f"Data saved to {output_file}")
                        completed += 1
                    else:
                        logger.info(f"No data found for issue {issue}, division {division}, page {page}")
                        # Create empty file to mark as processed
                        with open(output_file, 'w') as f:
                            f.write("rank,flag,name,issue,division,page\n")
                        completed += 1
                        break
                else:
                    logger.error(f"Failed to extract data for issue {issue}, division {division}, page {page}")
                    failed += 1

    
    logger.info(f"Fighter data extraction completed. {completed}/{total_combinations} successful, {failed} failed")
