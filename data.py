from datasets import Dataset
from torch.utils.data import DataLoader
from transformers import GPT2Tokenizer
import torch
import pandas as pd
class CustomDataset:
    def __init__(self, dataset_path:str):
        self.dataset_path = dataset_path
        self.tokenizer = GPT2Tokenizer.from_pretrained('./Model/Original')
        self.tokenizer.add_special_tokens({"pad_token": "<pad>", 
                                "bos_token": "<startofstring>",
                                "eos_token": "<endofstring>"})
        self.tokenizer.add_tokens(['<|im_start|>','<|im_sep|>','<|im_end|>','assistant','user'])
    def generate_dataset(self):
        dataset = pd.read_csv(self.dataset_path)
        conversation = []
        id = 0
        text = ''
        for _,row in dataset.iterrows():
            current_id = row['id']
            question = row['user']
            answer = row['assistant']
            if(current_id != id):
                text = f'<|im_start|>user<|im_sep|>{question}<|im_end|><|im_start|>assistant<|im_sep|>{answer}<|im_end|>'
            else:
                text += f'<|im_start|>user<|im_sep|>{question}<|im_end|><|im_start|>assistant<|im_sep|>{answer}<|im_end|>'
            id = current_id
            conversation.append(text)
        dataset = Dataset.from_dict({'conversation': conversation})


        dataset = dataset.map(self.tokenize_function, batched=True)
        dataset.set_format(type='torch', columns=['input_ids', 'attention_mask'])
        return dataset
        # train_dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
        # return train_dataloader

    def tokenize_function(self,dataset):
        return self.tokenizer(dataset['conversation'],return_tensors="pt",padding="max_length", truncation=True, max_length=768)
        


if __name__ == '__main__':
    dataset = CustomDataset('./dataset/dataset.csv')
    conversation = dataset.generate_dataset()
    