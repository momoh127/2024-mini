"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import urequests
import network

ssid = 'BU Guest (unencrypted)'
password = ''

database_api_url = "https://miniproject-21cf4-default-rtdb.firebaseio.com/.json"


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
     # %% let user know game started / is over
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def scorer(t: list[int | None]) -> dict:
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if t_good:
        avg_time = sum(t_good) / len(t_good)
        min_time = min(t_good)
        max_time = max(t_good)
    else:
        avg_time = min_time = max_time = None

    print(f"Average response time: {avg_time} ms")
    print(f"Minimum response time: {min_time} ms")
    print(f"Maximum response time: {max_time} ms")

    score = (len(t_good) / len(t)) if len(t) > 0 else 0
    data = {
        "average_time_ms": avg_time,
        "min_time_ms": min_time,
        "max_time_ms": max_time,
        "score": score,
        "response_times": t
    }

    return data


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def post_data_to_cloud(data: dict) -> None:
    """Send response time data to a cloud server using HTTP POST"""
    try:
        # Sending the data using HTTP POST
        response = urequests.post(database_api_url, json=data)
        if response.status_code == 200:
            print("Data uploaded successfully!")
        else:
            print(f"Failed to upload data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    connect_to_wifi()

    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    N = 10  # Number of flashes
    on_ms = 500  # Time for how long the LED will be on
    t: list[int | None] = []

    blinker(3, led)

    
    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))
        
        led.high()
        
        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)
    score_data = scorer(t)


    now: tuple[int] = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"
    print(f"Saving results to {filename}")
    write_json(filename, score_data)

    post_data_to_cloud(score_data)