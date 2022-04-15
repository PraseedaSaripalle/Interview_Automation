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
        topic=Topic.objects.create(topic=df['Topic'][row])
        topic.save()
        subtopic=df['SubTopics'][row]
        subtopic_seperaetd=subtopic.split(",")
        subtopic_count=0
        for subtopic in subtopic_seperaetd:
            subtopic=subtopic.strip()
            subtopic_name=Topic.objects.create(topic=subtopic)
            subtopic_name.save()
            topic.children.add(subtopic_name)
            subtopic_count=subtopic_count+1
