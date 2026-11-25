from sys import argv
from transformers import GPT2LMHeadModel, GPT2Tokenizer, set_seed
from transformers.utils import logging

logging.set_verbosity_error()

def load_tokenizer_and_model(model_name_or_path):
    return GPT2Tokenizer.from_pretrained(model_name_or_path), \
        GPT2LMHeadModel.from_pretrained(model_name_or_path)

def generate(
    model, tok, text,
    do_sample=True, max_length=100, repetition_penalty=5.0,
    top_k=5, top_p=0.95, temperature=1,
    num_beams=None,
    no_repeat_ngram_size=3
    ):
    input_ids = tok.encode(text, return_tensors="pt")
    out = model.generate(
        input_ids,
        max_length=max_length,
        repetition_penalty=repetition_penalty,
        do_sample=do_sample,
        top_k=top_k, top_p=top_p, temperature=temperature,
        num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
        )
    return list(map(tok.decode, out))

tokenizer, model = load_tokenizer_and_model('ai-forever/rugpt3large_based_on_gpt2')

while True:
    try:
        prompt = input("Введите промпт: ")

        set_seed(42)

        result = generate(
            model, tokenizer, prompt,
            do_sample=True, max_length=100, repetition_penalty=5.0,
            top_k=5, top_p=0.95, temperature=1,
            num_beams=1,
            no_repeat_ngram_size=3
            )

        print(" ".join(result))
        print()

    except KeyboardInterrupt:
        exit()