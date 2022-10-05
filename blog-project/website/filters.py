import timeago
import datetime



def fromnow(date):
   
    return timeago.format(date, datetime.datetime.now())


def trim(content):
    if len(list(content)) > 200:
        return "".join(list(content))[0:200]+" ...."

    else:
        return content+" ...."