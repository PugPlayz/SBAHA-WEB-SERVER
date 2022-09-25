import os, time

time.sleep(300)

while True:
    last_updt = os.path.getmtime('Profit.json')

    if (last_updt + 600) < time.time():
        print('reboot',last_updt, time.time())
        os.system('reboot')
    time.sleep(10)
