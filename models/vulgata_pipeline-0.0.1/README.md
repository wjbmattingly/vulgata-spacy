| Feature | Description |
| --- | --- |
| **Name** | `vulgata_pipeline` |
| **Version** | `0.0.1` |
| **spaCy** | `>=3.4.4,<3.5.0` |
| **Default Pipeline** | `entity_ruler`, `ner` |
| **Components** | `entity_ruler`, `ner` |
| **Vectors** | -1 keys, 100000 unique vectors (100 dimensions) |
| **Sources** | n/a |
| **License** | n/a |
| **Author** | [n/a]() |

### Label Scheme

<details>

<summary>View label scheme (5 labels for 2 components)</summary>

| Component | Labels |
| --- | --- |
| **`entity_ruler`** | `PARTIAL_SCRIPTURE`, `SCRIPTURE` |
| **`ner`** | `PARTIAL_SCRIPTURE`, `QUOTE`, `SCRIPTURE` |

</details>

### Accuracy

| Type | Score |
| --- | --- |
| `ENTS_F` | 89.50 |
| `ENTS_P` | 92.59 |
| `ENTS_R` | 86.61 |
| `NER_LOSS` | 175806.07 |