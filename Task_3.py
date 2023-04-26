import json


class Offer:
    def __init__(self, id: str, **kwargs):
        self.id = id
        for i in kwargs:
            if i != 'id' and i != 'partner_content':
                setattr(self, i, kwargs[i])
            elif i == 'partner_content':
                for j in kwargs['partner_content']:
                    setattr(self, j, kwargs['partner_content'][j])

    def update_offer(self, other):
        updated_properties = []
        for attribute in other.__dict__:
            if attribute != 'id' and getattr(self, attribute, None) != getattr(other, attribute, None):
                setattr(self, attribute, getattr(other, attribute))
                updated_properties.append(attribute)
        return updated_properties, self

    def get_properties(self):
        return [i for i in self.__dict__.keys() if i != 'id']

    def get_message_dict(self, triggers: list, shipments: list):
        dic = {'id': self.id}
        lst_to_send = triggers + shipments
        for key, value in self.__dict__.items():
            if key in lst_to_send and (key == 'price' or key == 'stock_count'):
                dic[key] = value

        if 'partner_content' in lst_to_send:
            for i in ['title', 'description']:
                if i in self.__dict__.keys():
                    if 'partner_content' not in dic.keys():
                        dic['partner_content'] = {i: getattr(self, i)}
                    else:
                        dic['partner_content'].update({i: getattr(self, i)})

        for i in ['title', 'description']:
            if i in lst_to_send and i in self.__dict__.keys():
                if 'partner_content' not in self.__dict__.keys():
                    dic['partner_content'] = {i: getattr(self, i)}
                else:
                    dic['partner_content'].update({i: getattr(self, i)})
        return dic


class Subscriber:
    def __init__(self, triggers: list, shipments: list):
        self.triggers = triggers
        self.shipments = shipments


class Update:
    def __init__(self, trace_id: str, offer: Offer):
        self.trace_id = trace_id
        self.offer = offer

    def get_message_json(self, triggers: list, shipments: list):
        return json.dumps({'trace_id': self.trace_id, 'offer': self.offer.get_message_dict(triggers, shipments)})


subscribers = []
updates = []
offers = {}

n, m = list(map(int, input().split(' ')))

for _ in range(n):
    row = input().split(' ')
    a, b = int(row[0]), int(row[1])
    subscribers.append(Subscriber(row[2:2 + a], row[2 + a:]))

for _ in range(m):
    inp = input()
    with io.StringIO(inp) as f:
        js = json.load(f)
    updates.append(Update(js['trace_id'], Offer(**js['offer'])))

# with open('./test.txt', 'r') as f:
#     rows = f.read().splitlines()
# n, m = list(map(int, rows[0].split(' ')))
# for i in range(1, n + 1):
#     row = rows[i].split(' ')
#     a, b = int(row[0]), int(row[1])
#     subscribers.append(Subscriber(row[2:2 + a], row[2 + a:]))
#
# for i in range(m):
#     js = json.loads(rows[n + i + 1])
#     updates.append(Update(js['trace_id'], Offer(**js['offer'])))

for upd in updates:
    updated_properties = []
    if upd.offer.id not in offers.keys():
        offers[upd.offer.id] = upd.offer
        updated_properties += upd.offer.get_properties()
    else:
        updated_properties, upd.offer = offers[upd.offer.id].update_offer(upd.offer)
    for sub in subscribers:
        lst_buff = sub.triggers
        if 'partner_content' in sub.triggers:
            lst_buff = sub.triggers + ['title', 'description']
        if set(lst_buff) & set(updated_properties):
            print(upd.get_message_json(sub.triggers, sub.shipments))
