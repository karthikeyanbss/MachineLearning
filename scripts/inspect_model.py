import spacy
nlp = spacy.load('output/model-last')
doc = nlp("Jeff Bezos founded Amazon in Seattle.")
print([(ent.text, ent.label_) for ent in doc.ents])