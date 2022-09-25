import ujson,time,os
#Requires - users.json, profit.json (sample.json is the data file from thr.py)



def restart():
    user_tree = {}
    with open('users.json','w') as outfile:
        jsonDump = ujson.dump(user_tree,outfile,indent=4)

def inventory():
    with open('Profit.json') as infile:
        auctions = ujson.load(infile)
        
        total_profit = 0
        total_auctions = 0
        for auction in auctions['auction']:
            profit = auction['profit']
            total_profit+=profit
            total_auctions+=1
        total_profit = "{:,}".format(total_profit)

    return({'response':'Success', 'total_profit':total_profit, 'total_auctions':total_auctions})

def reset_lc(ip):
    if len(ip) < 64:
        return {'response':'Invalid Request. Do NOT send unauthorized requests.'}

    with open('users.json') as infile:
        file = ujson.load(infile)
    file[ip] = time.time() - 1000
    with open('users.json','w') as outfile:
        jsonDump = ujson.dump(file,outfile,indent=4)
    return({'response':'Success'})
    


            
           
def data_request(ip):
    if len(ip) < 64:
        return {'response':'Invalid Request. Do NOT send unauthorized requests.'}

    response = None
    
    def output(code, response):
        print('output')
        if code == 0:
            response['response'] = 'Success'
        elif code == 1:
            response = {'response':response}
        return response


    def update_lc(ip):
        print('update')
        with open('users.json') as infile:
            file = ujson.load(infile)
        file[ip] = time.time() + 60
        with open('users.json','w') as outfile:
            jsonDump = ujson.dump(file,outfile,indent=4)
        return({'response':'Success'})
        
    def serve(ip):
        print('serve')
        update_lc(ip)
        
        with open('Profit.json') as infile:
            file = ujson.load(infile)
        auctions = file['auction']
        auction = auctions[0]
        auctions.pop(0)
        auctions = {'auction':auctions}

        with open('stats.json') as infile:
            file = ujson.load(infile)
            file['total_auctions'] +=1
            profit_int = auction['profit']
            file['total_profit'] += profit_int
        with open('stats.json','w') as outfile:
            jsonDump = ujson.dump(file,outfile,indent=4)
        
        with open('Profit.json','w') as outfile:
            jsonDump = ujson.dump(auctions,outfile,indent=4)
            
        return(auction)
        
        
                            
    def add(ip):
        print('add')
        with open('users.json') as infile:
            file = ujson.load(infile)
        file[ip] = 0
        with open('users.json','w') as outfile:
            jsonDump = ujson.dump(file,outfile,indent=4)

    with open('users.json') as infile:
        file = ujson.load(infile)
    for user in file:
        if user == ip:
            print('found_user')
            lc = file[user]
            if lc < time.time():
                print('lc_pass')
                auction = serve(ip)
                response = output(0,auction)
            else:
                print('lc_fail')
                timeT = (lc - time.time()) /  60 / 60
                timeT = round(timeT, 2)
                response = output(1, 'Please wait {} hours.'.format(timeT))
                
    if ip not in file:
        print('add_null')
        add(ip)
        auction = serve(ip)
        response = output(0,auction)


    return(response)


   
def stats():
    response = {}
    pet_count_list = {}
    count = 0
    with open('stats.json') as infile:
        stats = ujson.load(infile)
    with open('users.json') as infile:
        users = ujson.load(infile)
    with open('data.json') as infile:
        data = ujson.load(infile)
    for auction in data['auction']:
        name = auction['name']
        if name not in pet_count_list:
            pet_count_list[name] = 1
        else:
            pet_count_list[name] +=1  
    for user in users:
        count+=1
    last_updt = os.path.getmtime('Profit.json')
    last_updt = round((time.time() - last_updt))
    response['last_update'] = last_updt
    response['total_auctions'] = stats['total_auctions']
    response['total_profit'] = stats['total_profit']
    response['total_users'] = count
    response['pet_count'] = pet_count_list
    response['response'] = 'Success'

    return(response)
    
            
            
    
        
        
        

    
