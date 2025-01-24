from transformers import GPT2LMHeadModel,GPT2Tokenizer
import torch
from gtts import gTTS
import pygame
import io
import speech_recognition as sr
import random 
import re
import time
def text2speech(text):
    # Tạo âm thanh bằng gTTS
    tts = gTTS(text, lang='vi')

    # Tải âm thanh vào bộ nhớ (BytesIO)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Phát âm thanh với pygame
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()
    # Chờ đến khi âm thanh phát xong
    while pygame.mixer.music.get_busy():  # Check if music is still playing
        pygame.time.Clock().tick(10)  # Wait for the music to finish
def assistant(conversation:list):
    if(len(conversation)>3):
        conversation = conversation[-3:-1]
    context = ''
    for i in conversation:
        if(i['type']=='user'):
            context += f'<|im_start|>user<|im_sep|>{i["message"]}?<|im_end|>'
        else:
            context += f'<|im_start|>assistant<|im_sep|>{i["message"]}<|im_end|>'

    li = ['Bạn',"Tôi",'Tôi nghĩ', 'Bạn nên','Có thể']
    element = random.choice(li)
    input_text = f'{context}<|im_start|>assistant<|im_sep|>'
    input_text = f'{context}<|im_start|>assistant<|im_sep|>{element}'
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    model.eval()
    outputs = model.generate(
        inputs['input_ids'],
        pad_token_id=tokenizer.pad_token_id,
        attention_mask = inputs['attention_mask'],
        do_sample=True,
        max_length=256,# chỉnh
        min_length=10,
        top_k=40,
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2,
        num_return_sequences=1
    )

    print('context',context)
    # Giải mã kết quả
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print('origin',generated_text)
    generated_text = re.sub(r'\s*<\|im_start\|>\s*', '<|im_start|>', generated_text)
    generated_text = re.sub(r'\s*<\|im_sep\|>\s*', '<|im_sep|>', generated_text)
    generated_text = re.sub(r'\s*<\|im_end\|>\s*', '<|im_end|>', generated_text)
    generated_text = generated_text.replace(f'{context}<|im_start|>assistant<|im_sep|>','')
    print('replace',generated_text)
    if generated_text.find('<|im_end|>')>=0:
        generated_text = generated_text.split('<|im_end|>')[0]
        print('spilt',generated_text)
    elif generated_text.find('<|im_sep|>')>=0:
        generated_text = generated_text.split('<|im_sep|>')[0]
        print('split',generated_text)
    elif generated_text.find('<|im_start|>')>=0:
        generated_text = generated_text.split('<|im_start|>')[0]
        print('slipt',generated_text)

    return generated_text


if __name__ == '__main__':
    if('device' not in globals()):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer = GPT2Tokenizer.from_pretrained('./Model/Fineturning')
        model = GPT2LMHeadModel.from_pretrained('./Model/Fineturning')
        model.to(device)

    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    conversation = []
    conversation.append({
        'type':'assistant',
        'message':'Chào bạn tôi có thể giúp gì cho bạn.'
    })
    print('=====================start===========')
    while(True):
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source,timeout=None, phrase_time_limit=5)
        try:
            # Chuyển âm thanh thành văn bản (hỗ trợ tiếng Việt)
            print('======================recording===========================')
            text = recognizer.recognize_google(audio, language='vi-VN')
            if(text.lower().find('stop')>=0): break
            print("Bạn vừa nói:", text)
            conversation.append({
                'type': 'user',
                'message': text,
            })
            response = assistant(conversation)
            conversation.append({
                'type':'assistant',
                'message':f'{response}<|im_end|>'
            })
            print(response)
            text2speech(response);
        except sr.UnknownValueError:
            print("Không nhận dạng được giọng nói.")
        except sr.RequestError as e:
            print(f"Lỗi kết nối: {e}")
