import json


class Offer:
    def __init__(self, offer_id: str, **kwargs):
        self.offer_id = offer_id
        for i in kwargs:
            if i != 'id':
                setattr(self, i, kwargs[i])

    def update_offer(self, other):
        for attribute in other.__dict__:
            if attribute != 'offer_id':
                setattr(self, attribute, getattr(other, attribute))

    def get_properties(self):
        return [i for i in self.__dict__ if i != 'offer_id']

    def get_message_dist(self):
        return self.__dict__


class Subscriber:
    def __init__(self, triggers: list, shipments: list):
        self.triggers = triggers
        self.shipments = shipments


class Update:
    def __init__(self, trace_id: str, offer: Offer):
        self.trace_id = trace_id
        self.offer = offer

    def get_message_json(self):
        return json.dumps({'trace_id': self.trace_id
                              , 'offer': self.offer.get_message_dist()})


subscribers = []
updates = []

# n, m = list(map(int, input().split(' ')))
#
# for _ in range(n):
#     row = input().split(' ')
#     a, b = int(row[0]), int(row[1])
#     subscribers.append(Subscriber(row[2:2 + a], row[2 + a:]))
#
# for _ in range(m):
#     js = json.load(input())
#     updates.append(Update(js['trace_id'], Offer(**js['offer'])))

with open('./test.txt', 'r') as f:
    rows = f.read().splitlines()
n, m = list(map(int, rows[0].split(' ')))
for i in range(1, n + 1):
    row = rows[i].split(' ')
    a, b = int(row[0]), int(row[1])
    subscribers.append(Subscriber(row[2:2 + a], row[2 + a:]))

for i in range(m):
    js = json.loads(rows[n + i + 1])
    updates.append(Update(js['trace_id'], Offer(js['offer']['id'], **js['offer'])))

offers = {}
for upd in updates:
    updated_properties = []
    if upd.offer.offer_id not in offers.keys():
        offers[upd.offer.offer_id] = upd.offer
        updated_properties += upd.offer.get_properties()
    else:
        offers[upd.offer.offer_id].update_offer(upd.offer)
        updated_properties += upd.offer.get_properties()
    for sub in subscribers:
        if set(sub.triggers) & set(updated_properties):
            print(upd.get_message_json())
