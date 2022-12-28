# import streamlit as st
import spacy
from spacy.tokens import Doc, Span
from annoy import AnnoyIndex
import jellyfish
import pandas as pd
import string
import os
import json
from pathlib import Path
from distutils.sysconfig import get_python_lib
import os

Span.set_extension("fuzzy_matches", default=True, force=True)
Span.set_extension("annoy_matches", default=True, force=True)
Span.set_extension("scripture", default=True, force=True)



BASE_DIR = None
if os.path.isfile(get_python_lib() + "/vulgata_spacy"):
  BASE_DIR = get_python_lib() + "/vulgata_spacy"
else:
  BASE_DIR = os.path.dirname(__file__)

embedding_file = BASE_DIR + "/data/clem_partial.npy"
csv_file = BASE_DIR + "/data/clem_vulgate.csv"
map_file = BASE_DIR + "/data/index_map_partial.json"
spacy_model = "vulgata_pipeline"
annoy_file = "annoy_index/clem_400_partial.ann"

def create_annoy_index():
    import numpy as np
    doc_embeddings = np.load(embedding_file)
    t = AnnoyIndex(100, 'angular')
    for i, embedding in enumerate(doc_embeddings):
        t.add_item(i, embedding)
    t.build(400)
    os.mkdir("annoy_index")
    t.save(annoy_file)


css_data = """
<style>
.tooltip {
  position: 0px;
  border-bottom: 3px dotted black;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 300px;
  background-color: lightgray;
  color: black;
  text-align: left;
  border-radius: 6px;
  padding: 5px 0;
  position: absolute;
  z-index: 1;
  top: -5px;
  right: 110%;
}

.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 100%;
  margin-top: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: transparent transparent transparent black;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
"""

# st.markdown(css_data, unsafe_allow_html=True)

class VulgataSpaCy:
    def __init__(self):
        self.nlp = spacy.load(spacy_model)
        self.sent_parser = spacy.blank("en")
        self.sent_parser.add_pipe("sentencizer")
        self.df = pd.read_csv(csv_file)
        with open(map_file, "r") as f:
            self.index_map = json.load(f)
        if os.path.isfile(annoy_file):
            pass
        else:
            print("Currently creating annoy index. This only needs to be done once.")
            create_annoy_index()

    def create_doc(self, text):
        text = text.replace(";", ".")
        sent_doc = self.sent_parser(text)
        docs = []
        for sent in sent_doc.sents:
            doc = self.nlp(sent.text)
            docs.append(doc)
        doc = Doc.from_docs(docs)
        self.doc = doc
        return doc


    def visualize_doc(self):
        import streamlit as st
        st.markdown(css_data, unsafe_allow_html=True)
        def create_tooltip(doc):
            html_strings = []
            original_strings = []
            for ent in doc.ents:
                original_strings.append(ent.text)
                color_map = {"QUOTE": "yellow", "SCRIPTURE": "pink"}
                if ent._.scripture != True:
                    data = ent._.scripture
                    base_string = f"<mark style='background: #eda6bb'><span class='tooltip'>{ent.text}<span class= 'tooltiptext'>{ent.label_} "
                    for h in data:
                        base_string = base_string + f"<br>({h['score']:.2f})-{h['matcher']}:<br>{h['book']}: {h['chapter']}, {h['verse']}<br>{h['latin']}<br><br>"
                    base_string = base_string + "</span></span></mark>"
                    html_strings.append(base_string)
                else:
                    html_strings.append(f"<mark style='background: #a6edb9'><span class='tooltip'>{ent.text}<span class= 'tooltiptext'>{ent.label_}</span></span></mark>")
            raw_text = doc.text
            for h, o in zip(html_strings, original_strings):
                raw_text = raw_text.replace(o, h)

            return raw_text
        html_data = create_tooltip(self.doc)
        st.markdown(html_data, unsafe_allow_html=True)

    def annoy_matcher(self, style="ent", max_distance=.5, num_hits=1):
        t = AnnoyIndex(100, metric="angular")
        t.load("annoy_index/clem_400_partial.ann")
        df = self.df
        doc = self.doc
        def create_data(matches, ent):
            all_matches = []
            for match in matches:
                ent, label, score, answer = match
                match_data = {"score": score, "book":
                                               answer.book, "chapter": int(answer.chapter),
                                               "verse": int(answer.verse),
                                               "latin": answer.latin,
                                               "matcher": "annoy"}
                all_matches.append(match_data)
            if all_matches:
                ent._.scripture = all_matches
                ent.label_ = "SCRIPTURE"
            return ent
        new_ents = []
        total_hits = num_hits*20


        if style=="ent":
            parse_data = list(doc.ents)
        elif style=="sent":
            parse_data = doc.sents
            try:
                parse_data = list(doc.sents)
            except:
                doc.ents = [Span(doc, 0, len(doc), label="QUOTE")]
                parse_data = list(doc.ents)

        for ent in parse_data:
            temp_text = ent.text.lower()
            temp_text = "".join([c for c in temp_text if c not in string.punctuation])
            temp_text = temp_text.strip()
            temp = self.nlp(temp_text).vector
            res = t.get_nns_by_vector(temp, total_hits, include_distances=True)
            matches = []
            for idx, score in zip(res[0], res[1]):
                df_idx = self.index_map[str(idx)]
                answer = df.iloc[df_idx]
                if score < max_distance:
                    matches.append([ent, "SCRIPTURE", score, answer])
            if matches:

                matches = matches[:num_hits]
                ent = create_data(matches, ent)
                new_ents.append(ent)
            else:
                new_ents.append(ent)
        doc.ents = new_ents
        return doc
