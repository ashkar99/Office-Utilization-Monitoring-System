from mqtt_as import MQTTClient, config
from machine import Pin
import network
import uasyncio as asyncio
import utime

# Define IR sensor pins
IR_in_pin = Pin(2, Pin.IN, Pin.PULL_DOWN)  # IR sensor for entrance
IR_out_pin = Pin(19, Pin.IN, Pin.PULL_DOWN)  # IR sensor for exit

# Initialize variables for person count and time tracking
person_count = 0
last_activation_time = 0
lock_period_ms = 1000  # Time period to lock the sensors after activation to avoid multiple counts
person_entered = False
person_exited = False

# MQTT setup
topic = 'room/persons'
wifi_ssid = 'LNU-iot'
wifi_password = 'modermodemet'
config['server'] = '64.225.110.253'
config['port'] = 1883
config['user'] = 'king'
config['password'] = 'arthur'
config['ssid'] = wifi_ssid
config['wifi_pw'] = wifi_password
config["queue_len"] = 1  # Sets the length of the message queue

MQTTClient.DEBUG = True  # Enable debugging for MQTT client
client = MQTTClient(config)  # Create MQTT client instance


async def wifi_connect():
    """Asynchronous method to connect to the WiFi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        await asyncio.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


def sensor_in_handler(pin):
    """Callback for IR sensor at the entrance."""
    global person_entered, last_activation_time, lock_period_ms
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_activation_time) > lock_period_ms:
        person_entered = True
        last_activation_time = current_time


def sensor_out_handler(pin):
    """Callback for IR sensor at the exit."""
    global person_exited, last_activation_time, lock_period_ms
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_activation_time) > lock_period_ms:
        person_exited = True
        last_activation_time = current_time


# Set up interrupt requests (IRQ) for the IR sensors
IR_in_pin.irq(trigger=Pin.IRQ_RISING, handler=sensor_in_handler)  # IRQ for entrance sensor
IR_out_pin.irq(trigger=Pin.IRQ_RISING, handler=sensor_out_handler)  # IRQ for exit sensor


async def main(client):
    """Main asynchronous loop handling MQTT communication and person count."""
    global person_entered, person_exited, person_count
    await client.connect()  # Connect to the MQTT broker

    while True:
        # If a person has entered, increment count and send update via MQTT
        if person_entered:
            person_count += 1
            await client.publish(topic, str(person_count), qos=1)
            print(f"One person came in the room, The number of persons in the room: {person_count}")
            person_entered = False

        # If a person has exited, decrement count and send update via MQTT
        if person_exited and person_count > 0:
            person_count -= 1
            await client.publish(topic, str(person_count), qos=1)
            print(f"One person came out the room, The number of persons in the room: {person_count}")
            person_exited = False

        await asyncio.sleep(0.1)  # Small sleep to prevent high CPU usage


try:
    asyncio.run(main(client))  # Run the main function
finally:
    client.close()  # Ensure the client is closed properly on program termination
