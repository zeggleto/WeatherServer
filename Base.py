from flask import render_template
from flask import Flask, json, request
from Weather import get_all_weather, update_all, get_local_weather, get_single_weather
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/singleweather/<city>", methods=["GET"])
def return_single_weather(city):
    response = get_single_weather(city)
    return json.dumps(response)


@app.route("/localweather", methods=["POST"])
def return_local_weather():
    response = request.get_json()
    return json.dumps(get_local_weather(response["lat"], response["long"]))


@app.route("/currentweather", methods=["GET"])
def return_all_weather():
    return json.dumps(get_all_weather())


def update():
    update_all(False)


scheduler = BackgroundScheduler()
scheduler.add_job(
    func=update,
    trigger=IntervalTrigger(seconds=1200),
    id='printing_job',
    name='Update weather stats every 20 minutes',
    replace_existing=True)
scheduler.start()


if __name__ == '__main__':
    update_all(True)
    app.run()
