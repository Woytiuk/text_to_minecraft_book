import requests
import re
import textwrap
import json

# === Config ===
MAX_PAGES = 100
MAX_CHARS_PER_PAGE = 255
MAX_COMMAND_LENGTH = 32000  # Minecraft safe limit for chat/command blocks

def fetch_text(url):
    print(f"Downloading from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_text(text):
    match = re.search(r'\*{3} ?start.*?\*{3}', text, re.IGNORECASE)
    start = match.end() if match else 0
    match = re.search(r'\*{3} ?end.*?\*{3}', text, re.IGNORECASE)
    end = match.start() if match else len(text)
    return text[start:end].strip()

def split_chapters(text):
    chapters = re.split(r"\n(?=[IVXLCDM]+\.\s)", text)
    return [c.strip() for c in chapters if len(c.strip()) > 100]

def count_pages(text):
    return len(textwrap.wrap(text, MAX_CHARS_PER_PAGE))

def format_json_pages(pages):
    return [json.dumps({"text": page}) for page in pages]

def build_command(pages, vol_num, title="Minecraft Book", author="TextBot"):
    formatted_pages = format_json_pages(pages)
    nbt = f'/give @p written_book[written_book_content={{title:"{title} Vol. {vol_num}",author:"{author}",pages:[{",".join(formatted_pages)}]}}] 1'
    return nbt if len(nbt) <= MAX_COMMAND_LENGTH else None

def chunk_chapters(chapters):
    volumes = []
    current = []
    page_count = 0
    for chapter in chapters:
        pages_needed = count_pages(chapter)
        if page_count + pages_needed > MAX_PAGES:
            volumes.append(current)
            current = [chapter]
            page_count = pages_needed
        else:
            current.append(chapter)
            page_count += pages_needed
    if current:
        volumes.append(current)
    return volumes

def main():
    url = input("Paste Project Gutenberg .txt URL:\n> ").strip()
    raw = fetch_text(url)
    clean = extract_text(raw)
    chapters = split_chapters(clean)
    volumes = chunk_chapters(chapters)

    commands = []
    for i, vol in enumerate(volumes, start=1):
        full_text = "\n\n".join(vol)
        pages = textwrap.wrap(full_text, MAX_CHARS_PER_PAGE)[:MAX_PAGES]
        cmd = build_command(pages, i)
        if cmd:
            commands.append(cmd)
        else:
            print(f"Skipping Volume {i}: too large for Minecraft command.")

    with open("minecraft_book_commands.txt", "w", encoding="utf-8") as f:
        for cmd in commands:
            f.write(cmd + "\n\n")

    print(f"{len(commands)} Minecraft book command(s) saved to 'minecraft_book_commands.txt'")

if __name__ == "__main__":
    main()
