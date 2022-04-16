"""
services to import data from excel files

def import_xl(path_to_file):
    pass
"""

import pandas as pd
from .models import Topic

def read_excel(path,sheet_value):
    df = pd.read_excel (path,sheet_name=sheet_value)
    for row in range(len(df.index)):
        print(row)
        print("df['Topic'][row]",df['Topic'][row])
        tlist=Topic.objects.filter(topic__iexact=df['Topic'][row])
        nooftopics=tlist.count()
        print("nooftopics",nooftopics)
        topic=None
        if(nooftopics==0):
            topic=Topic.objects.create(topic=df['Topic'][row])
            topic.save()
            print("saved topic",topic)
        topic = Topic.objects.get(topic=df['Topic'][row])
        subtopic=df['SubTopics'][row]
        subtopic_seperaetd=subtopic.split(",")
        subtopic_count=0
        for subtopiccolumn in subtopic_seperaetd:
            subtopiccolumn=subtopiccolumn.strip()
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
