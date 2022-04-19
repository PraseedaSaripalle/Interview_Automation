"""
services to import data from excel files

def import_xl(path_to_file):
    pass
"""

import pandas as pd
from .models import Topic

def read_excel(path,sheet_value):
    #function used to read the excel/csv file. path and the name of the sheet are to be given as the parameters.
    df = pd.read_excel (path,sheet_name=sheet_value)
    #the pandas function is used to directly import the excel files.
    for row in range(len(df.index)):
        #iterating through the length of the rows that are present in the dataframe
        #print(row)
        print("df['Topic'][row]",df['Topic'][row])
        tlist=Topic.objects.filter(topic__iexact=df['Topic'][row])
        #filtering topic, if it had the same topicname
        nooftopics=tlist.count()
        #counting the topic query set
        print("nooftopics",nooftopics)
        topic=None
        if(nooftopics==0):
            #checking for the condition if topic count is 0
            topic=Topic.objects.create(topic=df['Topic'][row])
            #if 0, then enter that topic
            topic.save()
            #save the entered topic
            print("saved topic",topic)
        topic = Topic.objects.get(topic=df['Topic'][row])
        #get all the entered topics and put them in topic. 
        subtopic=df['SubTopics'][row]
        #get subtopics from the excel
        subtopic_seperaetd=subtopic.split(",")
        #since the children of a topic are stored in as comma seperated values, we need to split those values. The resultant is in form of a list.
        subtopic_count=0
        for subtopiccolumn in subtopic_seperaetd:
            subtopiccolumn=subtopiccolumn.strip()
            #strip is going to remove the unwanted spaces before and after the word.
            print("subtopiccolumn",subtopiccolumn)
            tlist=Topic.objects.filter(topic__iexact=subtopiccolumn)
            nooftopics=tlist.count()
            print("nosubtopics",nooftopics)
            
            subtopic_name=None
            if(nooftopics==0):
                subtopic_name=Topic.objects.create(topic=subtopiccolumn)
                subtopic_name.save()
                print("saved subtopic",subtopic_name)
                print("before adding subtopic to children")
            subtopic_name=Topic.objects.get(topic=subtopiccolumn)
            print("subtopic_name after search",subtopic_name.topic)
            topic.children.add(subtopic_name)
            subtopic_count=subtopic_count+1
