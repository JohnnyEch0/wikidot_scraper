import requests
from bs4 import BeautifulSoup
import re
import sys, os

def scrape_spell(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    content = soup.find('div', id='page-content')
    if not content:
        return None

    spell_name = soup.find('div', class_='page-title').text.strip()
    paragraphs = content.find_all('p')
    level_school_line = None
    for p in paragraphs:
        if re.match(r'\d+(st|nd|rd|th)-level \w+', p.text):
            level_school_line = p.text
            level_school = re.match(r'(\d+)(st|nd|rd|th)-level (\w+)', level_school_line)
            level = level_school.group(1)
            school = level_school.group(3)
            break
        if "cantrip" in p.text:
            level = 0
            school = p.text.split()[0]   
            break
            
        else:
            level_school = None
            level = "Unknown"
            school = "Unknown"


    # Extract casting time, range, components, and duration
    details_text = paragraphs[2].text.strip()  # Assuming it's always the third paragraph
    details = re.findall(r'(\w+[^:]+):\s*([^:\n]+)', details_text)
    details_dict = {k.lower(): v.strip() for k, v in details}

    casting_time = details_dict.get('casting time', 'Unknown')
    spell_range = details_dict.get('range', 'Unknown')
    components = details_dict.get('components', 'Unknown')
    duration = details_dict.get('duration', 'Unknown')

    # Extract description
    description_paras = paragraphs[3:-1]  # Exclude the last paragraph (spell lists)
    description = ' '.join([p.text.strip() for p in description_paras])

    # Extract classes
    classes_para = paragraphs[-1].text
    classes = classes_para.split(':')[-1].strip()

    action_type = ""
    if casting_time == "1 action":
        action_type = "action"
    elif casting_time == "1 reaction":
        action_type = "reaction"
    elif casting_time == "1 bonus action":
        action_type = "bonus action"
    else:
        action_type = casting_time
    # Format the markdown
    markdown = f"""---
type: 
- spell
casting time:
- {action_type}
known: 
level: {level}
school: {school.lower()}
---
#### {spell_name}
*{level_school.group(0) if level_school else 'Unknown level and school'}*
___
- **Casting Time:** {casting_time}
- **Range:** {spell_range}
- **Components:** {components}
- **Duration:** {duration}
---
{description}

**Classes:** {classes}
"""

    return markdown, spell_name


if __name__ == "__main__":
    if not len(sys.argv) >= 2:
        sys.exit("provide spell name as an argument")
    # Example usage
    url = "http://dnd5e.wikidot.com/spell:"
    url += sys.argv[1].strip().replace(" ", "_")

def main(url, output_path):
    markdown_output, spell_name = scrape_spell(url)

    if markdown_output:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)
        print(f"{spell_name} information saved to {output_path}")

    else:
        print(f"Failed to scrape {spell_name} information.")

# output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "DnD_Spells")