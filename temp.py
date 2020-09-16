import datetime

G = 1.25

def score(obj):
    D = get_day_difference(obj.wrote_datetime)
    L= len(obj.like)

    return (L-1) / pow((D+2), G)


def get_day_difference(datetime):
    return datetime.datetime.now().day - datetime.day

