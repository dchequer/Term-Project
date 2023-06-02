import os
from os import path
import datetime as dt

DATA_PATH = path.join(path.dirname(__file__), '..', 'data')

#print(DATA_PATH)

dir = os.listdir(DATA_PATH)
#print(dir)

def date_parser(text: str) -> dt.date | None:
    try:
        date = dt.datetime.strptime(text, '%Y%m%d').date()
    except ValueError:
        date = None
    return date
fail = date_parser('123re')
print(fail)

for file in dir:
    print(file)
    print(date_parser(file.split('.')[0]))


class DataLoader:
    def __init__(self) -> None:
        self.path = DATA_PATH


    def get_subjects_from_date(self, date: dt.date) -> None:
        date_as_string = date.strftime('%Y%m%d')
        print(date_as_string)

        for file_name in os.listdir(self.path):
            if date_as_string == file_name:
                print(file_name)


print('-------------------')
DL = DataLoader()
DL.get_subjects_from_date(dt.date(2020, 1, 18))
