# scripts/make_docbin.py
from spacy.tokens import DocBin
import spacy, json, pathlib

nlp = spacy.blank("en")
data = json.load(open("data/samples/sample_texts.json"))
db = DocBin()
for item in data:
    doc = nlp.make_doc(item["text"])
    db.add(doc)
pathlib.Path("data").mkdir(parents=True, exist_ok=True)
db.to_disk("data/samples.spacy")