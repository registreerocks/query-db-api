from os import environ as env

import requests

ENVIRONMENT = env.get('ENVIRONMENT', 'staging')
TEAMS_WEBHOOK = env.get('TEAMS_WEBHOOK')


def _notify_registree(action, customer_id, query_id):
  if ENVIRONMENT != 'local':
    card = _create_card(action, customer_id, query_id)
    res = requests.post(TEAMS_WEBHOOK, json=card)
    res.raise_for_status()



def _create_card(action, customer_id, query_id):
  return {
    "@context": "https://schema.org/extensions",
    "@type": "MessageCard",
    "themeColor": "0072C6",
    "title": action + " query on " + ENVIRONMENT + "!",
    "text": "Customer: " + customer_id + ", Query: " + query_id
}