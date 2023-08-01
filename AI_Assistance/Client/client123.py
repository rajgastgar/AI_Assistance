import eel
import gevent
eel.init("D:\HackathonProject\AI_Assistance\Client\www")
eel.start("home.html", size =(1000,700),port=9000, block=False)
gevent.get_hub().join()