![vulgata spacy logo](images/logo.png)

# About

Vulgata spaCy is a library built upon [spaCy](www.spacy.io) to automate the identification and extraction of potential Biblical quotes in medieval Latin texts. The main pipeline leverages [Bloom embeddings](https://explosion.ai/blog/bloom-embeddings) which were trained on the entire Patrologia Latina (PL) after substantial cleaning. The PL text was left lemmatized. Unfortunately, the data lisencing prevents its distribution. These bloom embeddings were loaded into a spaCy pipeline as floret embeddings. This allows for the pipeline to be quite small, while still being able to capture deep semantic and synactic meaning.

The pipeline contains several different components. First, the pipeline contains an EntityRuler whose patterns can identify direct quotation or partial quotation of Scripture with or without punctuation marks.

A second component is a quote detection machine learning model that is designed to identify quotes within context. Quotation marks and other indicators were removed before training so that the model would learn the features and context of Latin quotations.

Both of these components flag potential or likely Scriptural quotes. But being able to detect a Scriptural reference is, however, only part of the challenge. The second step in this process is linking that quote to a specific verse of the Vulgate. This problem is not as straightforward as it might appear and is compounded in several ways. First, Latin texts do not have standard spelling (even across modern editions); second, modern Latin texts do not agree on punctuation; third, many version of the Bible circulated in the Middle Ages that did not conform to the standard Vulgate, meaning words could appear out of order or synonyms used. These variant readings are often collectively known as Vetus Latina material. Therefore, matching "in initio fect Deus terras et caelum" to Genesis 1:1 ("in principio creavit Deuts terram et caelum") is not as simple as fuzzy-string matching. In order to correctly link data, semantic and synactic meaning must be retained.

To overcome this, Vulgata SpaCy contains the entire Vulgate as raw text, cleaned text, and partial text. These were embedded with the pipeline's vectors. An annoy index was then created. The pipeline allows for users to create their own index and query it with a new text.
