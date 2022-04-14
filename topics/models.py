from django.db import models
from django.db.models.signals import m2m_changed, pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

from django.core.exceptions import ValidationError

def validate_topic_caseinsensitive(value):
    if Topic.objects.filter(topic__iexact=value).exists():
        raise ValidationError('This TOPIC already exists.')
    return value


# Create your models here.
class Topic(models.Model):
    topic = models.CharField(max_length=200, unique=True)
    DOMAIN, DISCIPLINE, SUBDISCIPLINE, SUBJECT, TOPIC, SUBTOPIC = range(6)
    DESCRIPTIVE_LEVEL = [
        (DOMAIN, 'domain'),
        (DISCIPLINE, 'discipline'),
        (SUBDISCIPLINE, 'sub-discipline'),
        (SUBJECT, 'subject'),
        (TOPIC, 'topic'),
        (SUBTOPIC, 'sub-topic')
    ]

    level = models.PositiveSmallIntegerField("level description", choices=DESCRIPTIVE_LEVEL, default=DOMAIN)
    children = models.ManyToManyField(
        "self", symmetrical=False, related_name="parents", blank=True
    )
    materialized_paths = models.JSONField(default=list)

    def __str__(self):
        return "{1}: {0}".format(self.topic, self.level)

    class Meta:
        ordering = ["level", "topic"]

def set_materialized_paths(topic):
    """
    sets path from parents
    """
    if topic.parents.count() == 0:
        return [[{'id':topic.id, 'topic':topic.topic}]], 0
    else:
        result = []
        level = 100
        for parent in topic.parents.all():
            for entry in parent.materialized_paths:
                e = entry+[{'id':topic.id, 'topic':topic.topic}]
                result.append(e)
                level = min(level, len(e)-1)
        return result, level
        
# this may take time but it is essential
def recursive_subtopic_update(topic):
    """
    recursively set materialized paths for all children
    """
    for f in topic.children.all():
        f.materialized_paths, f.level = set_materialized_paths(f)
        f.save()
        recursive_subtopic_update(f)
        
"""
from backend we save
"""
@receiver(pre_save, sender=Topic)
def set_new_materialised_paths(sender, instance, **kwargs):
    if hasattr(instance, '__NOOP__'):
        return

    instance.topic = instance.topic.strip()
    if instance.pk:
        t = Topic.objects.get(pk=instance.pk)
        if t.topic.lower() != instance.topic.lower():
            # if topic has changed update
            m = instance.materialized_paths
            for p in m:
                p[-1]['topic'] = instance.topic
            instance.materialized_paths = m
            # set changed so as to recursively update children in post save
            instance.__CHANGED__ = True
    else:
        # check if this is case insensitively unique
        validate_topic_caseinsensitive(instance.topic)
        

@receiver(post_save, sender=Topic)
def recursive_update(sender, instance, created, **kwargs):
    if hasattr(instance, '__NOOP__'):
        del instance.__NOOP__
        return

    # recursively update children when topic has changed
    if created:
        # set the materialized path as domain initially
        # as it gets added to any parent m2m_changed will handle appropriately
        instance.materialized_paths = [[{'id':instance.id, 'topic':instance.topic}]]
        instance.__NOOP__ = True
        instance.save()

    if hasattr(instance, '__CHANGED__'):
        del instance.__CHANGED__
        recursive_subtopic_update(instance)

@receiver(pre_delete, sender=Topic)
def update_before_delete(sender, instance, **kwargs):
    # All the children become orphans or we remove all the children
    for t in instance.children.all():
        instance.children.remove(t)


@receiver(m2m_changed, sender=Topic.children.through)
def set_topic_materialized_paths(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    #print(sender, instance, action, reverse, model, pk_set)

    # if a parent is added or removed, update instance and its subtree
    if reverse:
        instance.materialized_paths, instance.level = set_materialized_paths(instance)
        instance.__NOOP__ = True
        instance.save()
        recursive_subtopic_update(instance)
    else:
        # if children are added or removed, update its immediate childrn and their subtrees.
        for key in pk_set:
            toupdate = Topic.objects.get(pk=key)
            toupdate.materialized_paths, toupdate.level = set_materialized_paths(toupdate)
            toupdate.__NOOP__ = True
            toupdate.save()
            recursive_subtopic_update(toupdate)