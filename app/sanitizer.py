from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngineProvider
from .store import SessionStore
from .config import settings
import uuid

# --- Load Small Model ---
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()  # <--- FIXED: Added closing parenthesis
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
anonymizer = AnonymizerEngine()
# --------------------------------------

def generate_placeholder(entity_type: str) -> str:
    unique_id = uuid.uuid4().hex[:6]
    return f"<{entity_type}_{unique_id}>"

def sanitize_text(text: str) -> str:
    if not text:
        return text

    original_text = text
    detected_entities = []

    # 1. Handle Custom Secret Words
    for word in settings.secret_list:
        if word in text:
            placeholder = generate_placeholder("SECRET")
            SessionStore.save(placeholder, word)
            text = text.replace(word, placeholder)
            detected_entities.append("CUSTOM_SECRET")

    # 2. Handle Standard PII
    results = analyzer.analyze(text=text, language='en')
    
    if results:
        operators = {}
        for result in results:
            entity_type = result.entity_type
            placeholder = generate_placeholder(entity_type)
            sensitive_text = text[result.start:result.end]
            SessionStore.save(placeholder, sensitive_text)
            operators[entity_type] = OperatorConfig("replace", {"new_value": placeholder})
            detected_entities.append(entity_type)

        text = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators).text

    # 3. Logging
    if detected_entities:
        print(f"[IronLayer] Scrubbed {len(detected_entities)} items: {detected_entities}")
        # Import and call the logger
        from app.logger import log_event
        log_event(original_text, text, detected_entities)

    return text

def desanitize_text(text: str) -> str:
    if not text:
        return text
            
    import re
    placeholders = re.findall(r'<[A-Z]+_[a-z0-9]+>', text)
    
    for ph in placeholders:
        real_value = SessionStore.get(ph)
        if real_value:
            text = text.replace(ph, real_value)
            
    return text