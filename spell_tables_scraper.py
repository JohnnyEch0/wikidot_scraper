import requests
from bs4 import BeautifulSoup
import os
import sys
import scraper

def scrape_table_and_spells(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tables = soup.find_all('table', class_='wiki-content-table')
    spell_urls = []
    
    
    
    for i, table in enumerate(tables):
        print(f"Table Nr {i}")
        output_folder = os.path.join(os.path.expanduser("~"), f"Documents\Jarson MD\Zeno\_Assets\wikidot_scrapes\spells\level_{i}")
        os.makedirs(output_folder, exist_ok=True)

        for row in table.find_all('tr')[1:]:  # Skip header row
            
            columns = row.find_all('td')
            if columns:
                spell_link = columns[0].find('a')
                if spell_link:
                    spell_url = "http://dnd5e.wikidot.com" + spell_link['href']
                    spell_name = spell_link.text.strip()
                    if "/" in spell_name:
                        print(f"\n a / was found! \n")
                        spell_name = input(f"\n DANGER:   provide alternative naming for {spell_name}")
                    
                    output_path = output_folder + f"\{spell_name}.md"
                    print(f"Scraping for {spell_name} at {spell_url} to {output_path}")

                    scraper.main(spell_url, output_path)
            
                    
                    

if __name__ == "__main__":
    base_url = "http://dnd5e.wikidot.com/spells"

    scrape_table_and_spells(base_url)
    sys.exit("Succesfully scraped!")