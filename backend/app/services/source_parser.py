import re

def extract_source_ids(answer: str):
    return list(set(re.findall(r"\[SOURCE_\d+\]", answer)))
