import PyPDF2
import re
import os

def get_valid_pdf_path():
    while True:
        pdf_path = "C:\\Users\Chill\Documents\Jarson MD\Zeno\_Assets\PDF\Flee, Mortals! The MCDM Monster Book v1.0.pdf"
        if os.path.isfile(pdf_path) and pdf_path.lower().endswith('.pdf'):
            return pdf_path
        else:
            print("Invalid file path or not a PDF. Please try again.")

def extract_monster_data(pdf_path, monster_name):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            monster_data = ""
            found = False
            for page in reader.pages:
                text = page.extract_text()
                if monster_name.lower() in text.lower():
                    found = True
                    monster_data += text
                elif found and re.search(r'\n\w+\n', text):  # New monster starts
                    break
            
            if not found:
                return "Monster not found."
            
            return monster_data  # For now, just return the raw text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    pdf_path = get_valid_pdf_path()
    monster_name = input("Enter the monster name: ")
    data = extract_monster_data(pdf_path, monster_name)
    print(data)

if __name__ == "__main__":
    main()