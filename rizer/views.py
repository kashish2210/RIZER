from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
import json


apiKey = "AIzaSyDv9bp4_xSayJxH6GnXdCfhdfqsZMERxr4"

def home(request):
    context = {}
    return render(request, 'index.html', context)

@csrf_exempt
def summarize(request):
    raw_data = request.body
    article = raw_data.decode('utf-8')

    numOfWords = 150
    prompt = (
        f"Summarize this article in {numOfWords} words. I am using the result of this prompt for an webapp. So make sure that it doesn't contain any formatting. It should be plain text. Here is the article: "
        + article
    )

    genai.configure(api_key=apiKey)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(prompt)

    jsonResult = {"result" : response.text}
    
    return JsonResponse(jsonResult)


from django.core.files.storage import FileSystemStorage

from PyPDF2 import PdfReader

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def upload(request):
    return render(request, 'fileupload.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        file_path = fs.path(filename)

        with open(file_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text+= page.extract_text()
        

        numOfWords = 150
        prompt = (
            f"Summarize this pdf files text in {numOfWords} words. I am using the result of this prompt for an webapp. So make sure that it doesn't contain any formatting. It should be plain text. Here is the article: "
            + text
        )

        genai.configure(api_key=apiKey)
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])

        response = chat_session.send_message(prompt)
        return HttpResponse(response.text)
    return render(request, 'index.html')


def mcqs(request):
    return render(request, 'mcqs.html')


def getMcqs(request):
    raw_data = request.body
    article_dict = json.loads(raw_data.decode('utf-8'))
    article = article_dict.get("article")
    
    prompt =  "can you ask me five mcq questions based on this article:" + article + '''Each question should be in dictionary format and all the question should be in the list:
{"question": "generated question",
"option_1": "generated option-1",
"option_2": "generated option-2",
"option_3": "generated option-3",
"option_4": "generated option-4",
"answer": "the correct answer(like this 1, 2, 3, 4)"}
i am going to use the result of this prompt in webapp so only provide five question nothing else.'''

    genai.configure(api_key=apiKey)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(prompt)

    questions = json.loads(response.text[8:-3])
    

    jsonResult = {"questionList" : questions}
    print(jsonResult)
    
    return JsonResponse(jsonResult)

def tts(request):
    return render(request, 'speaker.html')

def login(request):
    return render(request, 'login.html')