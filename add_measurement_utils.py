import datetime

def getKeyFilterArr(type, value):
    return {
        'AttributeValueList': [
            {type:value[0]},{type:value[1]}
        ],
        'ComparisonOperator': 'BETWEEN'
    }
    
def getKeyFilter(type, value, operator):
    return {
        'AttributeValueList': [
            {type:value}
        ],
        'ComparisonOperator': operator
    }

def getValueFromEvent(event, keyName, defaultValue):
    if keyName in event:
        keyValue = event[keyName]
        if keyValue != '':
            return event[keyName]
    return defaultValue

def getQueryFilter(startDate, endDate):
    dict = {
    }
    if (startDate != 0) and (endDate != 0):
        print ("between")
        startDateQueryKey = getKeyFilterArr('S', [startDate, endDate])
        dict.update({'measurementDate':startDateQueryKey})
    elif startDate != 0:
        startDateQueryKey = getKeyFilter('S', startDate, 'GE')
        dict.update({'measurementDate':startDateQueryKey})
    elif endDate != 0:
        endDateQueryKey = getKeyFilter('S', endDate, 'LE')
        dict.update({'measurementDate':endDateQueryKey})

    print ("query filter: " + str(dict))
    return dict

def getKeyConditions(moduleSN):
    moduleSNQueryKey = getKeyFilter('S', moduleSN, 'EQ')
    key_dict = {
        'moduleSN': moduleSNQueryKey
    }
    # print ("key_str: " + str(key_str))
    return key_dict

def getKeyForGetItem(moduleSN):
    moduleSNQueryKey = {
        'S':moduleSN
    }
    key_dict = {
        'moduleSN': moduleSNQueryKey
    }
    # print ("key_str: " + str(key_str))
    return key_dict

def timeCompareToCurrent(compareTo, isLater):
    now = datetime.datetime.now()
    hourStr = get2DigitsStr(now.hour)
    minuteStr = get2DigitsStr(now.minute)
    print ("hour, minute: " + hourStr + "," + minuteStr)
    hourMinuteInt = int(hourStr+minuteStr)
    result = int(compareTo) <= hourMinuteInt if isLater else int(compareTo) >= hourMinuteInt
    print ("timeCompareToCurrent: compareTo-"+compareTo + " current-"+str(now)+" isLater-"+str(isLater)+" result-"+str(result))
    return result
    
def get2DigitsStr(integ):
    if integ < 10:
        return "0"+str(integ)
    return str(integ)
