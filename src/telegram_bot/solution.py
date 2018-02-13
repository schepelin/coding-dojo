# Read api token from env TELEGRAM_API_TOKEN
# get updates for bot by POST to getUpdates
# https://api.telegram.org/{api-token}/getUpdates
#
# Update response:
# {
# 	"ok": true,
# 	"result": [{
# 		"update_id": 99809483,                   <---- pass is as offset prameter to getUpdates api method
# 		"message": {
# 			"message_id": 108,
# 			"from": {
# 				"id": 107573534,
# 				"is_bot": false,
# 				"first_name": "Maxim",
# 				"last_name": "Schepelin",
# 				"username": "schepelin",
# 				"language_code": "en-BY"
# 			},
# 			"chat": {
# 				"id": 107573534,                 <---- Pass it to sendMessage api method
# 				"first_name": "Maxim",
# 				"last_name": "Schepelin",
# 				"username": "schepelin",
# 				"type": "private"
# 			},
# 			"date": 1518459332,
# 			"text": "test"                       <---- And this to produce response
# 		}
# 	}]
# }

# send response to the method by POST
# https://api.telegram.org/{api-token}/sendMessage
# with body {"chat_id": <int>, "text": "<your text>"}

# For more info
# https://core.telegram.org/bots/api#getting-updates

# Hint: for http-requests you can use requests.post(url, json=payload, headers={'Content-Type': 'application/json'})

import os
import json
import requests
from functools import reduce

def main():
    api_token = os.environ.get('TELEGRAM_API_TOKEN')
    # get updates
    # produce response for message
    # send response to the chat

    service = ApiRequester(
        api_token=api_token,
        url='https://api.telegram.org',
    )

    while True:
        updates = service.get_updates()
        for update in updates:
            reply = process(update)
            service.send_message(reply)


def process(update):
    message = 'Something wrong'
    if update.message_text == 'ping':
        message = 'pong'
    return Reply(update.chat_id, message)


class Update:
    def __init__(self, update_dict):
        self._data = update_dict

    @property
    def chat_id(self):
        return self._data['message']['chat']['id']

    @property
    def message_text(self):
        return self._data['message']['text']

    @property
    def id_(self):
        return self._data['update_id']

    def __repr__(self):
        return str(self._data)


class Reply:
    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message


class ApiRequester:

    def __init__(self, api_token, url):
        self.__url = url
        self.__api_token = api_token
        self.__last_update_id = 0

    def __update_last_update_id(self, updates):
        self.__last_update_id = reduce(
            lambda greatest, update: max(greatest, update.id_),
            updates,
            self.__last_update_id
        )

    def get_updates(self):
        host = self.__url
        api_token = self.__api_token
        updates_url = f'{host}/{api_token}/getUpdates'
        resp = requests.post(
            updates_url,
            json={
                'offset': self.__last_update_id + 1,
            },
            headers={'Content-Type': 'application/json'}
        )
        updates = list(map(Update, resp.json()['result']))

        self.__update_last_update_id(updates)
        return updates

    def send_message(self, reply):
        host = self.__url
        api_token = self.__api_token
        url = f'{host}/{api_token}/sendMessage'
        resp = requests.post(
            url,
            json={
                'chat_id': reply.chat_id,
                'text': reply.message,
            },
            headers={'Content-Type': 'application/json'}
        )
        print(resp.status_code)


if __name__ == '__main__':
    main()

