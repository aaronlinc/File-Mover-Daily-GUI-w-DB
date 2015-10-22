import datetime
from pytz import timezone



def main():


    # New York Time
    ny = timezone('America/New_York')
    # London Time
    london = timezone('Europe/London')
    

    timeHQ = (datetime.datetime.now().strftime("%H%M"))
    timeNY = (datetime.datetime.now(ny).strftime("%H%M"))
    timeLon = (datetime.datetime.now(london).strftime("%H%M"))
    
    
    print("Portland: {}".format(isOpen(timeHQ)))
    print("New York: {}".format(isOpen(timeNY)))
    print("London:   {}".format(isOpen(timeLon)))
    


def isOpen(curTime):
    
    if (curTime < "2100") and (curTime >= "0900"):
        return 'Open'
    else:
        return 'Closed'

if __name__ == '__main__': main()
