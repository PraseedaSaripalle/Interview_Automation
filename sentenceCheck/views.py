from django.shortcuts import render
import json
from django.http import JsonResponse
from django.shortcuts import render
from sentenceCheck.models import Topic,Question,Answer
from django.template.loader import render_to_string
import random
from json import dumps
from django.shortcuts import render
# packages
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial import distance
#from .forms import AnsForm


def topic(request):
    print("in topic section")
    topics=list()
    if 'term' in request.GET:
        print("inside topic if condition")
        qs=Topic.objects.filter(topic_name__istartswith=request.GET.get("term"))   
        print("json object in topic function. 1", qs)
        for topic in qs:
            topics.append(topic.topic_name)
            print("json object in topic function.2 ")
        return JsonResponse(topics, safe=False)
    return render(request,"topic.html",{'topics':topics})


def retireveTopic(request):
    print("inside retrieve topic")
    #topic=Topic.objects.all()
    topic=Topic.objects.filter(topic_level=1)
    print("My topics",topic)
    
    return render(request,'topic.html',{'topic':topic})


def retireveSubTopicTemp(request):
    print("inside retireveSubTopitemp")
    if request.method == 'GET':
        topic_name=request.GET['topicname']
        print("topic_name", topic_name)
        topic=Topic.objects.get(topic_name=topic_name)
        subtopics=topic.children.all()
        print("My subtopics",subtopics)
        html = render_to_string('topic.html', {"topics":subtopics})
        return JsonResponse(html, safe=False)
    return render(request,"topic.html",{"topic":subtopics})


def questionDetails(request, topic_name):
    print("Displaying the details of the subtopics and the questions.")
    #Retrieving the Subtopics for a given topic
    print("topic_name",topic_name)
    rquestions=Question.objects.all().filter(topics__topic_name=topic_name)
    possible_ids = list(rquestions.values_list('id', flat=True))
    randomid=random.choices(possible_ids)
    randomQues=rquestions.filter(pk__in=randomid)
    randomid=randomid[0]
    for a in randomQues:
        question_text=a.question_text
  
    return render(request,'questions.html',{'qid':randomid,'questiontext':question_text})

    
'''
def txt_speech(generateQues):
    tts=gTTS(generateQues)
    tts.save('1.wav')  #tts to wav file
    soun='1.wav'
    print("Entered sound")
    #Audio(soun,autoplay=True)  #playing wav file using audio method
    return soun
'''
'''
@api_view(["GET"])
def tts(request):
	print(request.__class__)
	
	if request.is_ajax:
		print("AJAX request")
	else:
		print("Not AJAX request")
	print(request.query_params)
	text_list = request.query_params.getlist('text_list[]')
	print("Text list: ",text_list)

	lang = request.query_params.get('lang')
	print("lang: ",lang)
	if lang is not None and text_list!=[]:
		for sentence in text_list:
			speech(sentence,lang)
	return render(request, "text_to_speech.html")
'''
def verify(request):
    print("entered into verify")
    if request.method == 'POST':
        transcript = request.POST['transcript']
        quid = request.POST['quid']
        print("this is transcript",transcript)
        print("this is quid",quid)
        print("The type of quid is",type(quid))
        answers=Answer.objects.filter(question__id=quid)
        print("Answers are ",answers)
        answersList=[]
        for a in answers:
            answersList.append((a.answer,a.grade))
            #answersList.append(a.grade)
        print(answersList)
        similarity_check=cosine_distance_countvectorizer_method(transcript,answersList)
        excellent_index=[i for i,v in enumerate(similarity_check) if v[2]=="E"][0]
        excellent_answer=similarity_check[excellent_index][1]
        print("excellent answer is",excellent_answer)
        
        #closest_result=max(similarity_check)
        print("similarity_check",similarity_check)
        print("value", similarity_check[0][0])
        print("GRADE", similarity_check[0][1])
        closest_result=similarity_check[0][0]
        grade=similarity_check[0][2]
        user_closest_answer=similarity_check[0][1]
        null_value=0
        if similarity_check[0][0]==0:
            null_value=int(similarity_check[0][0])
            null_value=1
            #just for sending this to the template
            #null_value=1
    return render(request,"answer.html",{'submitted':1,'closest_result':closest_result,'grade':grade,'excellent_answer':excellent_answer,'user_closest_answer':user_closest_answer,'null_value':null_value})

def cosine_distance_countvectorizer_method(transcript,answersList):
    ans1=answersList[0][0]
    ans2=answersList[1][0]
    ans3=answersList[2][0]
    ans4=answersList[3][0]
    print("Entered into def function")
    cosine1=vectorizer(ans1,transcript)
    cosine2=vectorizer(ans2,transcript)
    cosine3=vectorizer(ans3,transcript)
    cosine4=vectorizer(ans4,transcript)

    cosine_values=[]
    cosine_values.append((cosine1,ans1,answersList[0][1]))
    cosine_values.append((cosine2,ans2,answersList[1][1]))
    cosine_values.append((cosine3,ans3,answersList[2][1]))
    cosine_values.append((cosine4,ans4,answersList[3][1]))
    print("cosine values are:",cosine_values)
    #cosine_values.sort(key=lambda y: y[0])
    cosine_values.sort(reverse=True)
    
    print(cosine_values)

    return cosine_values
        
    #return render(request,"content.html",{"submitted":1,"sentence_similarity1":cosine1,"sentence_similarity2":cosine2,"sentence_similarity3":cosine3})           
    # if a GET (or any other method) we'll create a blank form

def vectorizer(useranswer,DBanswer):
    allsentences = [useranswer,DBanswer]
    vectorizer = CountVectorizer()
    print("entered into vectorizer function")
    all_sentences_to_vector = vectorizer.fit_transform(allsentences)
    print("all_sentences entered")
    text_to_vector_v1 = all_sentences_to_vector.toarray()[0].tolist()
    text_to_vector_v2 = all_sentences_to_vector.toarray()[1].tolist()
            # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    print('Similarity of two sentences are equal to ',round((1-cosine)*100,2),'%')
    cosine = round((1-cosine)*100,2)
    print("consine", cosine)
    return cosine
