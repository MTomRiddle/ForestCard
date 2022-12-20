MONTH = {
    1: 'янв.',
    2: 'фев.',
    3: 'мар.',
    4: 'апр.',
    5: 'май.',
    6: 'июн.',
    7: 'июл.',
    8: 'авг.',
    9: 'сен.',
    10: 'окт.',
    11: 'ноя.',
    12: 'дек.',
}

WEEK = {
    0: 'ПН',
    1: 'ВТ',
    2: 'СР',
    3: 'ЧТ',
    4: 'ПТ',
    5: 'СБ',
    6: 'ВС'
}

class CustTime:
    def __init__(self, time):
        self.id = time.id
        self.hours = time.time.hour
        self.minutes = time.time.minute

    def __hash__(self):
        return (hash(self.hours) + hash(self.minutes)) % (10 ** 9 + 7)

    def str(self):
        return f'{self.hours}:{self.minutes:02}'
    def __str__(self):
        return f'{self.hours}:{self.minutes:02}'

class CustDate:
    def __init__(self, date):
        self.id = date.id
        self.day = date.date.day
        self.month = MONTH[date.date.month]
        self.weekday = WEEK[date.date.weekday()]

    def __hash__(self):
        return (hash(self.day) + hash(self.month)) % (10**9 + 7)

    def __str__(self):
        return f'{self.day} {self.month}'
