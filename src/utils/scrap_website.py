"""
Web Scraper for News Headlines from:
- panamabankingnews.com
- elfinancierocr.com
This scraper extracts news headlines from both websites using BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup
import time
import csv
import json
from urllib.parse import urljoin, urlparse
import logging
from typing import List, Dict, Optional
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"../../data/raw/news_headlines_{timestamp}.csv"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_scraper.log'),
        logging.StreamHandler()
    ]
)

class NewsScraper:
    def __init__(self, delay: float = 1.0):
        """
        Initialize the news scraper.        
        Args:
            delay: Delay between requests in seconds (be respectful to servers)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse webpage content.        
        Args:
            url: URL to fetch            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logging.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Add delay between requests
            time.sleep(self.delay)
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None
    
    def scrape_panama_banking_news(self, base_url: str = "https://panamabankingnews.com/") -> List[Dict]:
        """
        Scrape headlines from panamabankingnews.com        
        Args:
            base_url: Base URL of the website            
        Returns:
            List of dictionaries containing headline data
        """
        headlines = []
        posting_date = 'NA'
        # Get the main page
        soup = self.get_page_content(base_url)
        if not soup:
            return headlines
        
        # Extract headlines from main content area
        main_content = soup.find('div', class_='col-md-8')
        if main_content:
            # Look for article titles in various possible containers
            article_selectors = [
                'h2 a',           # Main article titles
                'h3 a',           # Secondary article titles
                '.entry-title a', # Entry titles
                'article h2 a',   # Article headers
                'article h3 a',   # Article sub-headers
                '.post-title a',  # Post titles
                '.article-title a' # Article title class
            ]
            
            for selector in article_selectors:
                elements = main_content.select(selector)
                for element in elements:
                    title = element.get_text(strip=True)
                    link = element.get('href', '')
                    
                    if title:
                        # Convert relative URLs to absolute
                        full_url = urljoin(base_url, link)
                        posting_date = element.parent.parent.find('span', class_='mg-blog-date').get_text(strip=True)                        
                        headline_data = {
                            'title': title,
                            'url': full_url,
                            'source': 'Panama Banking News',
                            'posting_date': posting_date
                        }
                        
                        # Avoid duplicates
                        if headline_data not in headlines:
                            headlines.append(headline_data)
                            logging.info(f"Found headline: {title[:100]}...")
        
        # Look for navigation links to get additional pages
        nav_links = soup.find('div', class_='nav-links')
        if nav_links:
            page_links = nav_links.find_all('a')
            # Limit to first 10 pages 
            for link in page_links[:10]:  
                page_url = link.get('href')
                if page_url and page_url != base_url:
                    page_url = urljoin(base_url, page_url)
                    logging.info(f"Scraping additional page: {page_url}")
                    
                    page_soup = self.get_page_content(page_url)
                    if page_soup:
                        page_content = page_soup.find('div', class_='col-md-8')
                        if page_content:
                            for selector in article_selectors:
                                elements = page_content.select(selector)
                                for element in elements:
                                    title = element.get_text(strip=True)
                                    link = element.get('href', '')
                                    posting_date = element.parent.parent.find('span', class_='mg-blog-date').get_text(strip=True)                                                           
                                    if title:
                                        full_url = urljoin(base_url, link)
                                        headline_data = {
                                            'title': title,
                                            'url': full_url,
                                            'source': 'Panama Banking News',
                                            'posting_date': posting_date
                                        }
                                        
                                        if headline_data not in headlines:
                                            headlines.append(headline_data)
        
        logging.info(f"Scraped {len(headlines)} headlines from Panama Banking News")
        return headlines
    
    def scrape_el_financiero(self, base_url: str = "https://www.elfinancierocr.com") -> List[Dict]:
        """
        Scrape headlines from elfinancierocr.com        
        Args:
            base_url: Base URL of the website            
        Returns:
            List of dictionaries containing headline data
        """
        headlines = []
                
        # Define specific URLs to scrape
        urls_to_scrape = [
            base_url + "/negocios/",
            base_url + "/finanzas/",
            base_url + "/economia-y-politica/"
        ]        
        
        # Target classes for headlines as specified
        headline_classes = [
            'md-promo-headline',
            'lg-promo-headline',
            'sm-promo-headline',
            'c-heading',            
            'headline-text'
        ]
        # Loop through each URL and scrape headlines
        for url in urls_to_scrape:
            soup = self.get_page_content(url)
            if not soup:
                logging.error(f"Failed to get content from {url}")
                continue

            # Look for headlines with the specified classes
            for class_name in headline_classes:
                elements = soup.find_all(class_= class_name) # 'a',
                logging.info(f"Count {len(elements)} for {class_name} in {url}")
                for element in elements:
                    title = element.get_text(strip=True)
                    if(element.name == 'a'):
                        link = element.get('href', '')
                    else:
                        link = "relative_url"

                    if title:
                        # Convert relative URLs to absolute
                        full_url = urljoin(base_url, link)
                        for parent in element.parents:
                            if parent.find('time'):
                                posting_date = parent.find('time').get_text(strip=True)
                            else:
                                posting_date = 'NA'
                                
                        headline_data = {
                            'title': title,
                            'url': full_url,
                            'source': 'El Financiero CR',
                            'posting_date': posting_date,
                            #'scraped_at': datetime.now().isoformat()
                        }
                        
                        # Avoid duplicates
                        if headline_data not in headlines:
                            headlines.append(headline_data)
                            logging.info(f"Found headline: {title[:100]}...")
                       
        logging.info(f"Scraped {len(headlines)} headlines from El Financiero")
        return headlines
    
    def scrape_all_sites(self) -> List[Dict]:
        """
        Scrape headlines from all configured news sites.        
        Returns:
            Combined list of headlines from all sites
        """
        all_headlines = []        
        # Scrape Panama Banking News
        panama_headlines = self.scrape_panama_banking_news()
        all_headlines.extend(panama_headlines)        
        # Scrape El Financiero
        financiero_headlines = self.scrape_el_financiero()
        all_headlines.extend(financiero_headlines)
        
        return all_headlines

    def save_to_csv(self, headlines: List[Dict], filename: str = 'news_headlines.csv'):
        """
        Save headlines to CSV file.        
        Args:
            headlines: List of headline dictionaries
            filename: Output CSV filename
        """
        if not headlines:
            logging.warning("No headlines to save")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = headlines[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for headline in headlines:
                    writer.writerow(headline)
            
            logging.info(f"Saved {len(headlines)} headlines to {filename}")
        
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")
    
    def save_to_json(self, headlines: List[Dict], filename: str = 'news_headlines.json'):
        """
        Save headlines to JSON file.        
        Args:
            headlines: List of headline dictionaries
            filename: Output JSON filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(headlines, jsonfile, indent=2, ensure_ascii=False)
            
            logging.info(f"Saved {len(headlines)} headlines to {filename}")
        
        except Exception as e:
            logging.error(f"Error saving to JSON: {e}")
    
    def print_headlines(self, headlines: List[Dict], max_display: int = 10):
        """
        Print headlines to console.        
        Args:
            headlines: List of headline dictionaries
            max_display: Maximum number of headlines to display
        """
        if not headlines:
            print("No headlines found.")
            return
        
        print(f"\n=== Found {len(headlines)} Headlines ===\n")
        
        for i, headline in enumerate(headlines[:max_display], 1):
            print(f"{i}. {headline['title']}")
            print(f"   Source: {headline['source']}")
            print(f"   URL: {headline['url']}")
            if 'class' in headline:
                print(f"   Class: {headline['class']}")
            print("-" * 80)
        
        if len(headlines) > max_display:
            print(f"... and {len(headlines) - max_display} more headlines")

def main():     
    # Initialize scraper with 1-second delay between requests
    scraper = NewsScraper(delay=1.0)
    
    try:
        # Scrape headlines from all sites
        print("Starting scraping...")
        headlines = scraper.scrape_all_sites()
        
        if headlines:           
            # Save results                                             
            scraper.save_to_csv(headlines, file_path)                        
            print(f"\n=== Summary ===")
            print(f"Total headlines scraped: {len(headlines)}")            
            # Count by source
            source_counts = {}
            for headline in headlines:
                source = headline['source']
                source_counts[source] = source_counts.get(source, 0) + 1            
            for source, count in source_counts.items():
                print(f"{source}: {count} headlines")
            
            print(f"\nData saved to: {file_path}")            
        
        else:
            print("No headlines were scraped. Check the logs for errors.")
    
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()