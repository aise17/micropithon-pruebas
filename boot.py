# boot.py -- run on boot-up

# import upip

import esp

esp.osdebug(None)
import gc
gc.collect()


from scron.week import simple_cron
# simple_cron.add('helloID', lambda *a,**k: print('hello'))
# simple_cron.add(
#     'Sunday12.00',
#     lambda *a,**k: print('wake-up call'),
#     weekdays=6,
#     hours=12,
#     minutes=0,
#     seconds=0
# )
# simple_cron.run()


SSID = "MOVISTAR_F8B0"
SSI_PASSWORD = "QB4neVXdRTxMfJwCXGT6"

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()
# upip.install("micropython-scron")
# upip.install("microdot")
# upip.install("utemplate")



