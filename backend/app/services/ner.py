from transformers import pipeline

ner_pipeline = pipeline(
    "ner", 
    model="dslim/bert-base-NER", 
    aggregation_strategy="simple" 
)

def extract_entities(text: str):
    if not text.strip():
        return []
    
    results = ner_pipeline(text.title())
    
   
    entities = []
    for entity in results:
        label = f"{entity['word']} ({entity['entity_group']})"
        entities.append(label)
        
    return entities

