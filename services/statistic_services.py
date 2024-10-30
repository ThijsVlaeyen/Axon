from .statistic_models import db_get_statistics

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