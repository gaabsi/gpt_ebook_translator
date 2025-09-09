export OPENAI_API_KEY="PUT YOUR API KEY HERE"

INPUT_EPUB="$1" #Path of the .epub as input
OUTPUT_EPUB="$2" #Path of the .epub you want to create
CHAP_START="$3" #First chapter you want to translate
CHAP_END="$4" #Last chapter you want to translate

caffeinate python main.py "$INPUT_EPUB" "$OUTPUT_EPUB" "$CHAP_START" "$CHAP_END"