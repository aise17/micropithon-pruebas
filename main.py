import time
from lib.src.microdot import Microdot, Response, send_file
from lib.src.microdot_utemplate import render_template, init_templates
from hcsr04 import HCSR04
from lib.umqttsimple import MQTTClient
# from machine import Pin, PWM
import machine
import ubinascii




app = Microdot()
Response.default_content_type = 'text/html'
init_templates('templates')

print("preparando servidor....")

sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
pwm = machine.PWM(machine.Pin(13))
pwm.freq(50)


#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())

MQTT_CLIENT_ID = b"rabbit@rabbitmq-5ddd646b5-d5w7m"
MQTT_BROKER    = b"65.109.197.46"
MQTT_PORT    = 32497
MQTT_USER      = b"rabbitmq"
MQTT_PASSWORD  = b"rabbitmq"




def connect_and_subscribe():
  try:
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER,port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD )
    client.connect()
    print('Connected to %s MQTT broker, subscribed to %s topic')
    return client
  except OSError as e:
    print(e)
    restart_and_reconnect()
        

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

@app.route('/')
def index(request):
    print("llamada recivida")
    return render_template('index.html',led_value=1)

@app.route('/armored')
def armored(request):
    print("Armored...")
    for position in range(1000,9000,50):
        pwm.duty_u16(position)
        time.sleep(0.01)
    for position in range(9000,1000,-50):
        pwm.duty_u16(position)
        time.sleep(0.01)
    return render_template('index.html',led_value=1)

@app.route('/send')
def send(request):
    print("Send...")

    try:
        client = connect_and_subscribe()
        print("Conected...")
        msg = b'Pruebaa'
        client.publish(b"/hello", msg)
    except OSError as e:
        print(e)
        restart_and_reconnect()

    return render_template('index.html',led_value=1)

@app.route('/static/<path:path>')
def static(request, path):
    print("Sierviendo estatico....")
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

app.run(port=80, debug=True)



# import pika

# credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters('65.109.197.46',32497, '/', credentials))
# channel = connection.channel()

# channel.queue_declare(queue='hello')

# channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# connection.close()