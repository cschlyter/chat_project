import requests
import pika
import json
from django.http import HttpResponse


def stock(request):

    if request.method == 'POST':
        command = request.POST.get('command')
        room_name = request.POST.get('room_name')

        user = "Stock Robot"

        if command.startswith("/stock="):
            robot_message = get_stock_quote(command)

            send_rabbit_message(robot_message, room_name, user)

            return HttpResponse("Message sent.", status=200)
        else:
            robot_message = f"Invalid command: {command}. Try /stock=STOCK_NAME"
            send_rabbit_message(robot_message, room_name, user)

        return HttpResponse("Invalid message.", status=500)


def send_rabbit_message(robot_message, room_name, user):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='stock_queue')
    body = {
        "message": robot_message,
        "user": user,
        "room": room_name
    }
    channel.basic_publish(exchange='',
                          routing_key='stock_queue',
                          body=json.dumps(body))
    print("Message sent to queue")
    connection.close()


def get_stock_quote(command):
    stock_name = command.split("=")[1]

    url = f"https://stooq.com/q/l/?s={stock_name.lower()}&f=sd2t2ohlcv&h&e=csv"
    r = requests.get(url)

    if r.status_code == 200:
        csv_file = r.content
        data = csv_file.decode('utf-8').splitlines()
        share_open_value = data[1].split(",")[3]
        robot_message = f"{stock_name.upper()} quote is {share_open_value} per share"
    else:
        robot_message = "An error ocurred while getting the Stock price. Please try again."

    return robot_message

