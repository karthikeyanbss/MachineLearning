#!/usr/bin/env python
"""Auto-annotate sample texts using 'expected_entities' names.

This script will:
- read `data/samples/sample_texts.json`
- for each text, find occurrences of the expected entity strings
- try to infer a label from spaCy's NER if available, otherwise use 'MISC'
- write a `data/train.spacy` DocBin and a human-readable `data/train.json`

Run inside the project's venv:
    venv\Scripts\python.exe scripts\auto_annotate_expected.py
"""
import json
from pathlib import Path
import spacy
from spacy.tokens import DocBin

ROOT = Path(__file__).resolve().parents[1]
DATA_IN = ROOT / "data" / "samples" / "sample_texts.json"
OUT_JSON = ROOT / "data" / "train.json"
OUT_SPACY = ROOT / "data" / "train.spacy"

nlp = spacy.load("en_core_web_sm")

def find_all_occurrences(text: str, substring: str):
    start = 0
    while True:
        idx = text.find(substring, start)
        if idx == -1:
            break
        yield idx, idx + len(substring)
        start = idx + len(substring)


def infer_label_from_doc(doc, start, end, text_snip):
    # Look for a matching entity in spaCy's doc
    for ent in doc.ents:
        if ent.start_char == start and ent.end_char == end and ent.text == text_snip:
            return ent.label_
    # If exact char-span not found, try matching text equality
    for ent in doc.ents:
        if ent.text == text_snip:
            return ent.label_
    return "MISC"


def main():
    DATA_IN.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(DATA_IN.read_text(encoding="utf8"))

    out_data = []
    db = DocBin()

    for item in data:
        text = item.get("text", "")
        expected = item.get("expected_entities", [])

        doc = nlp(text)
        spans = []
        seen = set()

        for name in expected:
            for (s, e) in find_all_occurrences(text, name):
                if (s, e) in seen:
                    continue
                seen.add((s, e))
                label = infer_label_from_doc(doc, s, e, name)
                # Create a span from character offsets
                span = doc.char_span(s, e, label=label, alignment_mode="contract")
                if span is None:
                    # fallback: try expand alignment
                    span = doc.char_span(s, e, label=label, alignment_mode="expand")
                if span is None:
                    # give up and skip this occurrence
                    continue
                spans.append(span)

        # set ents on a fresh doc created by nlp.make_doc to avoid running pipeline twice
        doc_for_db = nlp.make_doc(text)
        # convert spans to spans on doc_for_db by mapping token indices
        new_spans = []
        for sp in spans:
            # map char indices to new doc
            new_span = doc_for_db.char_span(sp.start_char, sp.end_char, label=sp.label_, alignment_mode="contract")
            if new_span is None:
                new_span = doc_for_db.char_span(sp.start_char, sp.end_char, label=sp.label_, alignment_mode="expand")
            if new_span is not None:
                new_spans.append(new_span)

        # attach entities
        try:
            doc_for_db.ents = new_spans
        except Exception:
            # skip if spans invalid
            doc_for_db.ents = tuple()

        db.add(doc_for_db)

        ents_out = [(span.start_char, span.end_char, span.label_) for span in new_spans]
        out_data.append((text, {"entities": ents_out}))

    OUT_JSON.write_text(json.dumps(out_data, indent=2), encoding="utf8")
    db.to_disk(OUT_SPACY)
    print(f"Wrote {OUT_JSON} and {OUT_SPACY}")


if __name__ == "__main__":
    main()
