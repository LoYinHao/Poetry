import re
import os

def parse_and_update():
    txt_file = r"d:\9991.張天春詩文彙編網站\pdf_content_fitz.txt"
    db_file = r"d:\9991.張天春詩文彙編網站\database.md"
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        
    in_qiyan = False
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
            
        if line.startswith("--- FILE: 七言絕句.pdf ---"):
            in_qiyan = True
            continue
        elif line.startswith("--- FILE:") and in_qiyan:
            break
            
        if not in_qiyan:
            continue
            
        # Skip headers
        if line in ['七言絕句', '張天春詩文彙編'] or re.match(r'^\d+$', line):
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
                
                # Check footnote 1 for source
                if '1' in current_footnotes:
                    source_match = re.search(r'刊於《.*?》.*?期.*?頁\d+', current_footnotes['1'])
                    if not source_match:
                         source_match = re.search(r'刊於《.*?》', current_footnotes['1'])
                    if source_match:
                        source = source_match.group(0)
                        
                # Combine remaining footnotes into annotation
                annos = []
                for k, v in current_footnotes.items():
                    if k == '1' and source:
                        # if the entire footnote 1 is just the source, skip it
                        if len(v) < len(source) + 15:
                            continue
                    # remove source from annotation string
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
                    'category': '七言絕句',
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
            
            # Not a poem line, not a footnote, not a header -> It must be a title
            # Sometimes there are notes like "左八", "右花左七" embedded in the title line
            # e.g., "採菱\n4　左八\n新妝結伴" => skip "左八"
            if re.match(r'^左\w+|^右\w+', line):
                continue
                
            # Ignore lines that are too long to be titles
            if len(line) < 20 and '　' not in line:
                buffer_title = line

    # Save the last poem
    if current_content:
        source = ""
        anno_str = "無"
        full_title = current_title + (" " + current_subtitle if current_subtitle else "")
        poems.append({
            'category': '七言絕句',
            'title': full_title,
            'content': current_content,
            'source': "未詳",
            'annotation': anno_str
        })

    # Read existing database.md
    with open(db_file, 'r', encoding='utf-8') as f:
        db_content = f.read()
        
    # Append new poems
    # Ensure it ends with newline
    if not db_content.endswith('\n'):
        db_content += '\n'
        
    # To avoid duplicates, let's just rewrite the whole database or append
    # Since database currently has our manual samples, let's just rewrite it
    # completely with the new parsed poems to be clean.
    
    new_db = "# 張天春詩文彙編資料庫\n\n| 類別 | 標題 | 內文 | 創作年份/來源 | 註釋 |\n| :--- | :--- | :--- | :--- | :--- |\n"
    for p in poems:
        title = p['title'].replace('|', '｜')
        content = p['content'].replace('|', '｜')
        source = p['source'].replace('|', '｜')
        anno = p['annotation'].replace('|', '｜')
        new_db += f"| {p['category']} | {title} | {content} | {source} | {anno} |\n"
        
    with open(db_file, 'w', encoding='utf-8') as f:
        f.write(new_db)
        
    print(f"Successfully parsed and wrote {len(poems)} poems to database.md.")

if __name__ == "__main__":
    parse_and_update()
