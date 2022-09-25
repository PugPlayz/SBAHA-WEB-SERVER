import json,requests,re,threading,time,os,ujson,datetime

#thr v2.0


def restart():
    os.system("nohup python3.9 {} &".format(os.path.basename(__file__)))
    exit()

def dynSleep(startTime):
    endTime = time.time()
    timeDiff = endTime - startTime
    sRatio = round((tRequests / 120),2)
    timeToSleep = round((sRatio * 60 + 3),None)
    time.sleep(timeToSleep)

def t_Requests():
    global tRequests
    tRequests+=1    
    

def startup():
    def SplitPages(totalPages):
        current = -1
        threadMap = {}
        aucPerThr = 5

        threads = int(totalPages / aucPerThr)

        #threads = 1
        for thread in range(threads):
            thread+=1
            threadMap[f'thread-{thread}'] = []
            threadMap[f'thread-{thread}'].append(current + 1)
            threadMap[f'thread-{thread}'].append(int(totalPages / threads) + current)
            current+= int(totalPages / threads)
        if current != threads:
            lastThread = threadMap[f'thread-{thread}']
            lastThread[1] = totalPages

        return(threadMap)
    
    try:
        data = requests.get("https://api.hypixel.net/skyblock/auctions",  timeout=10).json()
        totalPages = data['totalPages'] - 1
        t_Requests()
    except Exception as e:
        print(e)
        restart()
    threadMap = SplitPages(totalPages)
    with open('tMap.json','w') as outfile:
        jsonDump = ujson.dump(threadMap,outfile,indent=4)
    return threadMap


def threadStart(threadMap):
    global cleanAuctions
    def Data(pStart,pEnd):

        def DataFilter(data):
            allowedTiers = ['EPIC', 'LEGENDARY','MYTHIC']
            auctions = data["auctions"]
            for auction in auctions:
                itemName = auction["item_name"]
                lvl = itemName[5:8].strip(" []")
                if lvl.isnumeric():
                    lvl = int(lvl)
                    if auction['bin']:
                        itemTier = auction['tier']
                        if itemTier in allowedTiers:

                            itemName =  re.sub("[\(\[].*?[\)\]]", "", itemName)
                            itemName = itemName.replace("\u2726","")
                            itemName = itemName.strip()

                            passAuction = {}
                            passAuction['start'] = auction['start']
                            passAuction['name'] = itemName
                            passAuction['tier'] = itemTier
                            passAuction['lvl'] = lvl
                            passAuction['price'] = auction['starting_bid']
                            passAuction['user'] = auction['auctioneer']

                            cleanAuctions['auction'].append(passAuction)

                            
        currentPage = pStart
        while currentPage <= (pEnd):
            try:
                data = requests.get("https://api.hypixel.net/skyblock/auctions?page={}".format(currentPage)).json()
            except:
                restart()
            t_Requests()
            currentPage +=1
            DataFilter(data)


    

    threadsList = []
    for thread in threadMap:
        threadRange = threadMap[thread]
        pStart = threadRange[0]
        pEnd = threadRange[1]
        newThread = threading.Thread(target=Data, args=(pStart,pEnd))
        newThread.start()
        threadsList.append(newThread)
        
    for oldThread in threadsList:
        oldThread.join()

    
    cleanAuctions['auction'] = sorted(cleanAuctions['auction'], key=lambda k: (k['price']))
    return(cleanAuctions)


def ProfitFinder(auctions):
    profitList = {}
    profitList['auction'] = []

    
    filterList = ['Ghoul','Hound','Endermite','Spirit','Jerry','Bee']
    
    for main in auctions['auction']:
        num = 0
        mainName = main['name']
        
        if mainName in filterList:
            continue
        for auction in auctions['auction']:

            cursorName = auction['name']
            
            if main == auction:
                continue

            mainTier = main['tier']

            cursorTier = auction['tier']

            if num == 0:
                if  mainName == cursorName and  mainTier == cursorTier:
                    mainLvl = main['lvl']
                    cursorLvl = auction['lvl']
                    high = mainLvl + 100
                    low = mainLvl - 15
                    if cursorLvl in range(low,high):
                        mainPrice = main['price']
                        cursorPrice = auction['price']
                        
                        if cursorLvl > mainLvl:
                            estRatio = cursorLvl - mainLvl
                            estRatio = estRatio / 100
                            estSP = cursorPrice - cursorPrice * estRatio
                        else:
                            estSP = cursorPrice
                        estSP = round(estSP, None)
                            
                            
                        pProfit = estSP - mainPrice

                
                        if pProfit >= 90000:
                            main['estSP'] = estSP
                            main['profit'] = pProfit
                            main.pop('start')
                            profitList['auction'].append(main)
                            num+=1
                        else:
                            num+=1
                            pass
            else:
                 pass      
    profitList['auction'] = sorted(profitList['auction'], key=lambda k: (k['profit']), reverse=True)
    profitList['auction'] = sorted(profitList['auction'], key=lambda k: (k['price']))
    return profitList                    



        

                    
                
while True:
    #VAR RESET -\
    tRequests = 0
    cleanAuctions = {}
    cleanAuctions['auction'] = []
    # -/
    
    startTime = time.time()           
    threadMap = startup()
    auctions = threadStart(threadMap)
    profit = ProfitFinder(auctions)

    with open('data.json','w') as outfile:
        jsonDump = ujson.dump(auctions,outfile,indent=4)
    with open('Profit.json','w') as outfile:
        jsonDump = ujson.dump(profit,outfile,indent=4)

    dynSleep(startTime)







