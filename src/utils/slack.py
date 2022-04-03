import requests

import env


def post_slack_message(channel, message):
    url = 'https://slack.com/api/chat.postMessage'
    data = dict(
        token=env.SLACK_TOKEN,
        channel=channel,
        text=message,
    )
    headers = {'Content-Types': 'application/json'}
    res = requests.post(url, data=data, headers=headers)
    print(res)
