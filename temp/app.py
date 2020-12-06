import adafruit_dht
import time
import board

from flask import Flask, Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge

dhtSensor = adafruit_dht.DHT11(board.D17)

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
    })

temp_gauge = Gauge('temp_gauge', 'Temperature in Celcius')

while True:
    humidity = dhtSensor.humidity
    temp_c = dhtSensor.temperature

    print(f"Temp: {temp_c}C \nHumidity: {humidity}%")

    time.sleep(10)

@app.route('/')
def temperature():
    return f"Current temperature is {temp_c}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
