from .statistic_models import *

def get_statistics():
    stats = []
    for stat in db_get_statistics():
        stats.append({
            'artist': stat['artist'],
            'title': stat['title'],
            'whistle': stat['whistle'],
            'active': stat['active'],
            'total': stat['total'],
            'score': stat['score']
        })

    return stats

def get_activity():
    activity_data = [{'date': row[0], 'total_activity': row[1]} for row in db_get_activity()]
    return activity_data