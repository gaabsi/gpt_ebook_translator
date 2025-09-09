import os
import re 
import time

import ebooklib
import openai
import pypandoc
from bs4 import BeautifulSoup
from ebooklib import epub


class BookTranslator:
    def __init__(
        self, prompt, model="gpt-4o", css_path=None, temp_md_path=None, delay=2
    ):
        self.prompt = prompt
        self.model = model
        self.css_path = css_path
        self.temp_md_path = temp_md_path or os.path.join(os.getcwd(), "temp.md")
        self.delay = delay

    def extract_epub_to_markdown(self, epub_path, output_md_path):
        markdown_content = []
        book = epub.read_epub(epub_path)

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), features="xml")  
                for tag in soup.find_all(["h1", "h2", "h3", "h4", "p"]):
                    if tag.name.startswith("h"):
                        level = int(tag.name[1])
                        markdown_content.append(
                            f"\n{'#' * level} {tag.get_text().strip()}\n"
                        )
                    elif tag.name == "p":
                        text = ""
                        for child in tag.descendants:
                            if child.name in ("b", "strong"):
                                text += f"**{child.get_text()}**"
                            elif child.name in ("i", "em"):
                                text += f"*{child.get_text()}*"
                            elif child.string:
                                text += child.string
                        markdown_content.append(text.strip() + "\n")

        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_content))

    def extract_chapter_by_index(self, md_path, chapter_number, level=2):
        with open(md_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        heading_prefix = "#" * level + " "
        chapter_idx = 0
        in_chapter = False
        content = []

        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith(heading_prefix):
                chapter_idx += 1
                if chapter_idx == chapter_number:
                    in_chapter = True
                    content.append(line)
                    continue
                elif in_chapter and chapter_idx > chapter_number:
                    break
            elif in_chapter:
                content.append(line)

        return "".join(content)

    def translate_chapter(self, text):
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature = 0,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": text},
            ],
        )
        traduction = response.choices[0].message["content"]
        traduction_no_rep = re.sub(r'(\b[^.!?]+[.!?])(\s+\1)+', r'\1', traduction)
        return traduction_no_rep

    def translate_epub_to_translated_epub(
        self, input_epub_path, output_epub_path, chapter_start, chapter_end, level=2
    ):
        temp_md = self.temp_md_path
        self.extract_epub_to_markdown(input_epub_path, temp_md)

        all_translations = []
        for chap_num in range(chapter_start, chapter_end + 1):
            try:
                chap = self.extract_chapter_by_index(temp_md, chap_num, level)
            except Exception as e:
                print(e)
                continue

            try:
                translated = self.translate_chapter(chap)
                translated = f"\n\n\\newpage\n\n{translated.strip()}\n"
                all_translations.append(translated)
            except Exception as e:
                print(e)
                continue

            time.sleep(self.delay)

        final_md = temp_md.replace(".md", "_translated.md")
        with open(final_md, "w", encoding="utf-8") as f:
            f.write("\n\n".join(all_translations))

        try:
            convert_args = [
                "--standalone",
                "--toc",
            ]
            if self.css_path:
                convert_args.append(f"--css={self.css_path}")

            pypandoc.convert_file(
                final_md,
                to="epub",
                format="markdown",
                outputfile=output_epub_path,
                extra_args=convert_args,
            )
            print(f"EPUB écrit : {os.path.abspath(output_epub_path)}")

        except Exception as e:
            print(e)

        finally:
            if os.path.exists(temp_md):
                os.remove(temp_md)
            if os.path.exists(final_md):
                os.remove(final_md)
