import re
import os

def parse_and_append(target_pdf, category):
    txt_file = r"d:\9991.張天春詩文彙編網站\pdf_content_fitz.txt"
    db_file = r"d:\9991.張天春詩文彙編網站\database.md"
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        
    in_section = False
    poems = []
    
    current_title = ""
    current_subtitle = ""
    current_content = ""
    current_footnotes = {}
    
    buffer_title = ""
    
    for i in range(len(lines)):
        line = lines[i].strip()
        if not line:
            continue
            
        if line.startswith(f"--- FILE: {target_pdf} ---"):
            in_section = True
            continue
        elif line.startswith("--- FILE:") and in_section:
            break
            
        if not in_section:
            continue
            
        # Skip headers
        if line in [category, '張天春詩文彙編'] or re.match(r'^\d+$', line):
            continue
            
        # Detect footnotes
        if re.match(r'^\d+　', line):
            parts = line.split('　', 1)
            if len(parts) == 2:
                num = parts[0]
                content = parts[1]
                # Filter out judge records (評審紀錄)
                content = re.sub(r'左詞宗.*?評選。?', '', content)
                content = re.sub(r'右詞宗.*?評選。?', '', content)
                content = re.sub(r'詞宗.*?評選。?', '', content)
                current_footnotes[num] = content.strip()
            continue
            
        # Detect poem content
        if '，' in line and '。' in line:
            # clean embedded numbers
            clean_line = re.sub(r'\d+', '', line)
            if current_content:
                current_content += "<br>" + clean_line
            else:
                current_content = clean_line
                
            # If we just started a poem, the buffer_title is our title
            if buffer_title and not current_title:
                if buffer_title.startswith('其'):
                    current_subtitle = buffer_title
                else:
                    current_title = buffer_title
                    current_subtitle = ""
        else:
            # If we hit a new title, it means the previous poem is done
            if current_content:
                # Save previous poem
                # Try to extract the first footnote as source if it exists
                source = ""
                anno_str = ""
                
                if '1' in current_footnotes:
                    source_match = re.search(r'刊於《.*?》.*?期.*?頁\d+', current_footnotes['1'])
                    if not source_match:
                         source_match = re.search(r'刊於《.*?》', current_footnotes['1'])
                    if source_match:
                        source = source_match.group(0)
                        
                annos = []
                for k, v in current_footnotes.items():
                    if k == '1' and source:
                        if len(v) < len(source) + 15:
                            continue
                    val = v.replace(source, '').strip('。， ')
                    if val:
                        annos.append(f"{k}. {val}")
                
                if annos:
                    anno_str = "<br>".join(annos)
                else:
                    anno_str = "無"
                
                if not source:
                    source = "未詳"
                    
                full_title = current_title
                if current_subtitle:
                    full_title += " " + current_subtitle
                    
                poems.append({
                    'category': category,
                    'title': full_title,
                    'content': current_content,
                    'source': source,
                    'annotation': anno_str
                })
                
                # reset for next
                if not line.startswith('其'):
                    current_title = ""
                current_subtitle = ""
                current_content = ""
                current_footnotes = {}
            
            # Title handling
            if re.match(r'^左\w+|^右\w+', line):
                continue
                
            if len(line) < 20 and '　' not in line:
                buffer_title = line

    # Save the last poem
    if current_content:
        source = ""
        anno_str = "無"
        full_title = current_title + (" " + current_subtitle if current_subtitle else "")
        poems.append({
            'category': category,
            'title': full_title,
            'content': current_content,
            'source': "未詳",
            'annotation': anno_str
        })
        
    print(f"Parsed {len(poems)} poems.")

    # Read existing database.md
    with open(db_file, 'r', encoding='utf-8') as f:
        db_content = f.read()
        
    # Append new poems
    if not db_content.endswith('\n'):
        db_content += '\n'
    
    append_str = ""
    for p in poems:
        title = p['title'].replace('|', '｜')
        content = p['content'].replace('|', '｜')
        source = p['source'].replace('|', '｜')
        anno = p['annotation'].replace('|', '｜')
        append_str += f"| {p['category']} | {title} | {content} | {source} | {anno} |\n"
        
    with open(db_file, 'a', encoding='utf-8') as f:
        f.write(append_str)
        
    print(f"Successfully appended {len(poems)} poems to database.md.")

if __name__ == "__main__":
    parse_and_append("五言絕句.pdf", "五言絕句")
