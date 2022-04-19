"""
services to import data from excel files

def import_xl(path_to_file):
    pass
"""

import pandas as pd
from .models import Topic
from django.core.exceptions import ValidationError

def get_or_create_topic(topic_name):
    """
    fetched a topic (case insensitive) if exists, else creates one

    @string topic_name: name of the topic
    """
    topic_name = topic_name.strip()

    try:
        topic, _ = Topic.objects.get_or_create(topic=topic_name)
    except ValidationError:
        # topic already exists
        topic = Topic.objects.filter(topic__iexact=topic_name).first()

    return topic


def read_excel(path,sheet_value):
    """
    function used to read the excel/csv file.
    
    @string path: path to the excel file
    @string sheet_value: sheet name in the excel file

    @returns:nothing

    comments:
    Each row of the excel file has a format
    col1 (Topic)        |   col2 (SubTopics)
    -----------------------------------------------------
    parent topic |  comma seaparted child topics 
    """
    
    # create a pandas data frame from the sheet of the excel file
    df = pd.read_excel(path,sheet_name=sheet_value)

    #iterating through the length of the rows that are present in the dataframe
    for row in range(len(df.index)):
        # get or creqate parent topic
        parent_topic = get_or_create_topic(df['Topic'][row].strip())

        # Get and assign the subtopics
        parent_topic.children.add(*map(get_or_create_topic, df['SubTopics'][row].split(",")))
        
