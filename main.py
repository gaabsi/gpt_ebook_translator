import os
import sys 
import openai
from functions import BookTranslator

openai.api_key = os.getenv("OPENAI_API_KEY")
EPUB_ORIGINAL = sys.argv[1]
EPUB_SORTIE= sys.argv[2]
FROM = int(sys.argv[3])
TO = int(sys.argv[4])
CSS_PATH = os.path.join(os.path.dirname(__file__), "epub.css")


PROMPT = """
 You are a translator (English to French).
 Translate fluently and idiomatically, preserving tone and structure. 
 I want your translation to be easily readable. 
 This is a fantasy webnovel, you must keep a very narrative tone in your translation.
 Use Markdown: *italics*, **bold**, ## for titles.
 Do not translate proper nouns. 
 Keep ellipses and punctuation. 
 Return clean, fluent, structured Markdown.
 """


translator = BookTranslator(
    prompt=PROMPT,
    css_path=CSS_PATH
)

translator.translate_epub_to_translated_epub(
    input_epub_path=EPUB_ORIGINAL,
    output_epub_path=EPUB_SORTIE,
    chapter_start=FROM,
    chapter_end=TO
)