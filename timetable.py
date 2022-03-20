from tabulate import tabulate
import requests

g_limit = 10
g_url = f'https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D={g_limit}&sort=departure_time' \
       '&include=schedule%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north'


def get_sched_time(response):
    included = response['included']
    for prediction in response['data']:
        schedule_id = prediction['relationships']['schedule']['data']['id']
        for record in included:
            if record['id'] == schedule_id:
                return record['attributes']['departure_time']
    return None


def fill_timetable(response, timetable):
    for prediction in response['data']:
        time = '{%H:%M:%S}'.format(get_sched_time(response))
        dest = prediction['relationships']['route']['data']['id']
        train_num = prediction['relationships']['trip']['data']['id']
        status = prediction['attributes']['status']
        timetable.append(list([time, dest, train_num, status]))


if __name__ == "__main__":
    response = requests.get(g_url).json()
    print(response['data'][0].keys())

    timetable = []
    fill_timetable(response, timetable)

    table_header = ['Time', 'Destination', 'Train #', 'Status']
    table_format = "fancy_grid"
    print(tabulate(timetable, table_header, tablefmt=table_format))
