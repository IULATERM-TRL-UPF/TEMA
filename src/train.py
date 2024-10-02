# -*- coding: utf-8 -*-


from tokenizers.implementations import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
import torch
from transformers import RobertaConfig
import json
from transformers import RobertaTokenizerFast
from transformers import RobertaForMaskedLM
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments


def train(lang):

    tokenizer = ByteLevelBPETokenizer(
        "./vocab.json",
        "./merges.txt",
    )

    tokenizer._tokenizer.post_processor = BertProcessing(
        ("</s>", tokenizer.token_to_id("</s>")),
        ("<s>", tokenizer.token_to_id("<s>")),
    )
    tokenizer.enable_truncation(max_length=512)


    config = RobertaConfig(
        vocab_size=52_000,
        max_position_embeddings=514,
        num_attention_heads=12,
        num_hidden_layers=6,
        type_vocab_size=1,
    )

    tokenizer_config = {"max_len": 512}

    with open("./tokenizer_config.json", 'w') as fp:
        json.dump(tokenizer_config, fp)


    tokenizer = RobertaTokenizerFast.from_pretrained("./"+lang+"BERT", max_len=512)
    model = RobertaForMaskedLM(config=config)


    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=0.15
    )


    training_args = TrainingArguments(
        output_dir="./"+lang+"BERT",
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_gpu_train_batch_size=64,
        save_steps=10_000,
        save_total_limit=2,
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.save_model("./"+lang+"BERT")