import re
from function import Func

isTimed = False

def isStock(line):
    pattern = re.compile(r"^(\w+):\d+$")
    return re.match(pattern, line)

def isProcess(line):
    if line.startswith("optimize"):
        return None
    pattern = re.compile(r"^(\w+):\(")
    return re.match(pattern, line)


def splitStock(stock):
    stock = stock.split(":")
    if len(stock) > 2:
        return 
    return stock[0], stock[1]

def getStock(line, stocks, processList):
    if isStock(line):
        stockName, quantity = splitStock(line)
        if stockName and quantity:
            stocks[stockName] = int(quantity)
            return True
    return False

def splitProcess(line):
    name = line[:line.find(":")]
    delay = line[line.rfind(":") + 1:]
    
    costs = line[line.find("(") + 1:line.find(")")]
    rewards = line[line.rfind("(") + 1:line.rfind(")")]

    costsDict = {}
    rewardsDict = {}
    
    realCosts = costs.split(";")
    realRewards = rewards.split(";")
    
    for cost in realCosts:
        costName, quantity = tuple(cost.split(":"))
        costsDict[costName] = int(quantity)
    
    for reward in realRewards:
        rewardName, quantity = tuple(reward.split(":"))
        rewardsDict[rewardName] = int(quantity)
    
    return name, costsDict, rewardsDict, delay

def getProcess(line, stocks, processList):
    if isProcess(line):
        processName, costs, rewards, delay = splitProcess(line)
        for key in costs.keys():
            if key not in stocks:
                stocks[key] = 0
        for key in rewards.keys():
            if key not in stocks:
                stocks[key] = 0
        processList.append(Func(processName, costs, rewards, delay))
        return True
    return False


def isObjective(line):
    return line.startswith("optimize")


def getObjective(line, toOptimize):
    global isTimed
    if isObjective(line):
        tmpToOptimize = line[line.find("(") + 1:line.find(")")]
        tmpToOptimize = tmpToOptimize.split(";")
        for elem in tmpToOptimize:
            if elem == 'time':
                isTimed = True
                continue
            toOptimize.append(elem)
        return len(toOptimize) > 0 
    return False


def functionTable(stocks, processList, toOptimize, index, line):
    if index == 0:
        index += (not getStock(line, stocks, processList))
        if index > 0 and not isProcess(line):
            print("ERROR")
            exit(0)
    if index == 1:
        index += (not getProcess(line, stocks, processList))
        if index > 1 and not isObjective(line):
            print("ERROR")
            exit(0)
    if index == 2:
        index += (getObjective(line, toOptimize))
    return index

def didParsingSucceed(index, stocks, processList, toOptimize):
    return index == 3 and len(stocks) and len(processList) and len(toOptimize) 

def parseFile(data, stocks, processList, toOptimize):
    index = 0
    for line in data:
        if not line:
            return didParsingSucceed(index, stocks, processList, toOptimize)
        if line[0] == "#":
            continue
        index = functionTable(stocks, processList, toOptimize, index, line)
    return didParsingSucceed(index, stocks, processList, toOptimize)


def isTime():
    return isTimed
