# text_to_minecraft_book

Turn full-length books (like from Project Gutenberg) into readable Minecraft written books using Python. Automatically splits long texts into volumes and formats them for use with command blocks. Some times will split across sentences depending on the length of chapters.

## Features

- Converts plain text files into Minecraft book commands
- Automatically splits content into volumes (100 pages max)
- Escapes special characters to ensure valid JSON
- Outputs /give commands for Minecraft Java Edition

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/your-username/minecraft-book-converter.git
cd minecraft-book-converter
pip install -r requirements.txt
```
## Example

`/give @p command_block`

Then paste this inside the block:
/give @p written_book[written_book_content={title:"Meditations Vol. 1",author:"TextBot",pages:[...]}]


## Limitations

- Only supports Minecraft Java Edition 1.20.5+
- Chat cannot handle long commands — use command blocks

## Credits

Built by [Sam Woytiuk](https://www.linkedin.com/in/samuel-woytiuk) — inspired by Stoic philosophy and Minecraft creativity.
