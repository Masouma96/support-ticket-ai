from transformers import pipeline

_ner_pipeline = None


def _get_ner_pipeline():
    global _ner_pipeline
    if _ner_pipeline is None:
        _ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple",
        )
    return _ner_pipeline


def extract_entities(text: str):
    if not text or not text.strip():
        return {}

    results = _get_ner_pipeline()(text)

    entities = {}
    for entity in results:
        key = entity["entity_group"]
        entities.setdefault(key, []).append(entity["word"])

    return entities
