import fitz
import re

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_poems(text):
    lines = text.split('\n')
    poems = []
    
    current_title = ""
    current_subtitle = ""
    current_content = ""
    current_footnotes = {}
    
    # State tracking
    in_footnotes = False
    
    poem = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # skip headers
        if re.match(r'^\d+$', line) or line in ['七言絕句', '張天春詩文彙編']:
            continue
            
        # Detect footnotes section
        if re.match(r'^\d+　', line):
            in_footnotes = True
            # Parse footnote
            parts = line.split('　', 1)
            if len(parts) == 2:
                num = parts[0]
                content = parts[1]
                # Filter out judge records
                content = re.sub(r'左詞宗.*?評選。?', '', content)
                content = re.sub(r'右詞宗.*?評選。?', '', content)
                current_footnotes[num] = content
            continue
            
        # Detect poem content
        if '，' in line and '。' in line:
            in_footnotes = False
            # Clean embedded footnote numbers in the poem
            clean_content = re.sub(r'\d+', '', line)
            
            if poem and not poem['content']:
                poem['content'] = clean_content
            else:
                # Append to existing content or it's a new line
                if poem:
                    poem['content'] += "<br>" + clean_content
            continue
            
        # If it's a title
        if not in_footnotes and not ('，' in line or '。' in line):
            # It's a title or subtitle
            if line.startswith('其'):
                current_subtitle = line
                # Create a new poem entry for "其二"
                poem = {
                    'title': current_title,
                    'subtitle': current_subtitle,
                    'content': "",
                    'footnotes': []
                }
                poems.append(poem)
            elif len(line) > 1 and len(line) < 20 and '　' not in line:
                current_title = line
                current_subtitle = ""
                poem = {
                    'title': current_title,
                    'subtitle': current_subtitle,
                    'content': "",
                    'footnotes': []
                }
                poems.append(poem)

    return poems, current_footnotes

if __name__ == "__main__":
    text = parse_pdf(r"d:\9991.張天春詩文彙編網站\DOC\七言絕句.pdf")
    poems, footnotes = parse_poems(text)
    
    # Print the first 10 for review
    for p in poems[:10]:
        print(f"Title: {p['title']} {p['subtitle']}")
        print(f"Content: {p['content']}")
        print("---")
