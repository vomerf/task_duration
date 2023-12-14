from datetime import time, datetime, timedelta


busy = [
    {'start': '10:30', 'stop': '10:50'},
    {'start': '18:40', 'stop': '18:50'},
    {'start': '14:40', 'stop': '15:50'},
    {'start': '16:40', 'stop': '17:20'},
    {'start': '20:05', 'stop': '20:20'}
]

busy.sort(key=lambda x: x['start'], reverse=True)

busy_intervals = [
    {
        "begin_of_reception": (
            datetime.combine(
                datetime.today(), time.fromisoformat(duration['start'])
            )
        ),
        "end_of_reception": (
            datetime.combine(
                datetime.today(), time.fromisoformat(duration['stop'])
            )
        ),
    }
    for duration in busy
]

free_windows: list = []


def create_shedule(start_time, end_time, duration):

    current_time = start_time
    while current_time < end_time:
        busy_flag = False
        for dict_time in busy_intervals:
            if current_time >= dict_time['begin_of_reception']:
                busy_intervals.pop()
                break
            if (dict_time['begin_of_reception'] <=
                    current_time <
                    dict_time['end_of_reception']):
                busy_flag = True
                next_time = dict_time.get('end_of_reception')
                break

        if not busy_flag:
            for item in busy_intervals:
                next_time = None
                if (
                        item['begin_of_reception'] -
                        current_time <
                        timedelta(minutes=duration)
                ):
                    next_time = dict_time.get('end_of_reception')
                    break
            if next_time is None or busy_intervals == []:
                next_time = current_time + timedelta(minutes=duration)
                if next_time <= end_time:
                    free_windows.append(
                        {
                            'begin_of_reception': current_time,
                            'end_of_reception': next_time,
                        }
                    )
        current_time = next_time
    return free_windows


def main(start_of_work, end_of_work, duration):
    shedule = create_shedule(start_of_work, end_of_work, duration)
    count = 0
    for begin, finish in shedule:
        print(
            f"Начало приема: {shedule[count][begin].strftime('%H:%M')} - "
            f"Конец приема {shedule[count][finish].strftime('%H:%M')}"
        )
        count += 1


if __name__ == "__main__":
    start_work = datetime.combine(
        datetime.today(),
        time(hour=int(input('Введите целочисленное значение начала смены: ')))
    )
    end_work = datetime.combine(
        datetime.today(),
        time(hour=int(input('Введите целочисленное значение конца смены: ')))
    )
    duration = int(input(
        'Введите целочисленное значение минут на прием одного пациента: ')
    )
    main(start_work, end_work, duration)
