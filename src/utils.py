import math
def format_time(time):
    return "{hours}:{minutes}:{seconds}".format(
                hours=math.floor(time/3600),
                minutes=math.floor((time % 3600)/60),
                seconds=math.floor(time % 3600 % 60)
            )