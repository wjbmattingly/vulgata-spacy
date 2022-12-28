import streamlit as st
from vulgata_spacy import vulgata_spacy

nlp = vulgata_spacy.VulgataSpaCy()
text = st.sidebar.text_area("Paste Text Here")
annoy_bool = st.checkbox("Use Annoy Index")
if text != "":
    doc = nlp.create_doc()
    if annoy_bool:
        doc = nlp.annoy_matcher(style="sent", max_distance=.50)
    nlp.visualize_doc()
