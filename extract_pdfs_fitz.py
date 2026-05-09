import fitz
import os

files = [
    r"d:\9991.張天春詩文彙編網站\DOC\七言絕句.pdf",
    r"d:\9991.張天春詩文彙編網站\DOC\五言絕句.pdf",
    r"d:\9991.張天春詩文彙編網站\DOC\古詩及詞調.pdf",
    r"d:\9991.張天春詩文彙編網站\DOC\律詩.pdf",
    r"d:\9991.張天春詩文彙編網站\DOC\詩人介紹與推薦序.pdf",
    r"d:\9991.張天春詩文彙編網站\DOC\詩鐘及對聯.pdf"
]

with open('pdf_content_fitz.txt', 'w', encoding='utf-8') as out:
    for f in files:
        out.write(f"\n\n--- FILE: {os.path.basename(f)} ---\n")
        try:
            doc = fitz.open(f)
            for page in doc:
                out.write(page.get_text() + "\n")
        except Exception as e:
            out.write(f"Error reading {f}: {e}\n")
