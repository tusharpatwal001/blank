from transformers import AutoTokenizer



def create_token(sentence: str) -> list:
    """
    Return tokens from the provided string.
    """
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    tokens = tokenizer.tokenize(sentence)
    # print()
    return tokens

# ['hi', ',', 'my', 'name', 'is', 'tu', '##sha', '##r', 'pat', '##wal', '.']