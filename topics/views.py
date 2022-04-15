from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .services import *

def upload_topics(request):
    path="D:\Ml Project\Enligence Internship\datasets\TopicsTaxonomy.xlsx"
    sheet_value='CS'
    read_excel(path,sheet_value)
    return render(request,'upload.html')
