
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


def check_keyword(text, keyword):
    # Load pre-trained BERT model and tokenizer
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize the text
    tokens = tokenizer(text, return_tensors="pt")

    # Use the model to get token classifications
    outputs = model(**tokens)
    predictions = outputs.logits.argmax(dim=2)

    # Check if the keyword is present in the tokenized text
    keyword_token_ids = tokenizer(keyword, return_tensors="pt")["input_ids"][0]
    keyword_present = any(keyword_token_ids.tolist() in prediction.tolist() for prediction in predictions.tolist())

    return keyword_present

# Example usage
text = """
There was plenty to get excited about at the start of the decade as carmakers from Tesla, opens new tab to Volkswagen, opens new tab to BYD (002594.SZ), opens new tab wanted to ensure they had enough lithium, nickel and cobalt for what was hoped to be sustained rapid uptick in EV sales. The price for all three ingredients at least doubled roughly between 2021 and 2022. But they have since gone into reverse as deliveries of new EVs, while still growing, are lower than many expected and manufacturers like Ford Motor, opens new tab and General Motors, opens new tab have cut investments."""

keyword = "Tesla"

if check_keyword(text, keyword):
    print(f"The text mentions {keyword}.")
else:
    print(f"The text does not mention {keyword}.")
