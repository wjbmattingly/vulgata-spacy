import streamlit as st
from vulgata_spacy import vulgata_spacy

nlp = vulgata_spacy.VulgataSpaCy()
text = st.text_area("Paste Text Here")
annoy_bool = st.checkbox("Use Annoy Index")
if annoy_bool:
    max_distance = st.slider("Set Max Distance", .01, 1.0, .5)
    style = st.selectbox("Run Annoy on:", ["sent", "ent"])
if text != "":
    doc = nlp.create_doc(text)
    if annoy_bool:
        doc = nlp.annoy_matcher(style=style, max_distance=max_distance)
    nlp.visualize_doc()
