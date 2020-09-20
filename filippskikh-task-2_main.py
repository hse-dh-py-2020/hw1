import requests

def get_teacher_schedule(teacher_name):
    # https://ruz.hse.ru/api/search?term=....&type=person
    response = requests.get('https://ruz.hse.ru/api/search', {
        'term': teacher_name,
        'type': 'person'
    })

    teachers = response.json()
    if len(teachers) == 0:
        print("Преподаватель не найден!")
        return None

    teacher = teachers[0]
    response = requests.get('https://ruz.hse.ru/api/schedule/person/{}'.format(teacher['id']), {
        'start': '2020.09.14',
        'finish': '2020.09.20',
        'lng': 1
    })
    schedule = response.json()
    return schedule

def main():
    while True:
        teacher = input('Введите ФИО преподавателя: ')
        schedule = get_teacher_schedule(teacher)
        if schedule:
            for lesson in schedule:
                print("Дата:", lesson['dayOfWeekString'], lesson['date'])
                print("Время: {} - {}".format(lesson['beginLesson'], lesson['endLesson']))
                print("Дисциплина:", lesson['discipline'])
                print("Группа:", lesson['group'])
                print('Место проведения:', lesson['auditorium'], lesson['building'])
                print('Преподаватель:', lesson['lecturer'])
                print('---------------')


if __name__ == '__main__':
    main()