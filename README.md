# Real Time Chat with Stock Bot
> A real time chat with a bot for checking stock prices.

## Requirements  (Prerequisites)
Tools and packages required to successfully install this project.
For example:
* Python 3.3 and up
* Latest version of pip
* RabbitMQ (To procces to stock bot messages)
* Redis (Used by the channels library)
* Docker (Optional)

## Installation

`$ pip3 install -r requirements.txt`

Configure in your OS the following environment variables:

SECRET_KEY="Example Secret"

RABBIT_HOST=localhost

REDIS_HOST=localhost


## Running the tests

`python3 manage.py test`

## Usage example
You need to have Redis and RabbitMQ running and configured in the environment variables:

To run rabbit via docker:

`docker run -d --hostname my-rabbit --name rabbit-server -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

To run Redis via docker:

`docker run -p 6379:6379 -d redis:5`

Run the migrations:

`python3 manage.py migrate`

To run the server:

`python3 manage.py runserver`

To run the bot consumer service:

`python3 manage.py stock_consume`

Navigate to:

`http://127.0.0.1:8000/chat`

Register a user and login to see the chat.

## Screenshots


