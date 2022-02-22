import random

from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject


def fix_marks(schoolkid_full_name: str):
    schoolkids = Schoolkid.objects.filter(full_name__contains=schoolkid_full_name)
    if len(schoolkids) > 1:
        print('There is more than one student with this name')
        return
    if not schoolkids:
        print('There is more than one student with this name')
        return
    schoolkid = schoolkids[0]
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid_full_name: str):
    schoolkids = Schoolkid.objects.filter(full_name__contains=schoolkid_full_name)
    if len(schoolkids) > 1:
        print('There is more than one student with this name')
        return
    if not schoolkids:
        print('There is more than one student with this name')
        return
    schoolkid = schoolkids[0]
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


commendations = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!']


def create_commendation(schoolkid_full_name, subject_title: str):
    schoolkids = Schoolkid.objects.filter(full_name__contains=schoolkid_full_name)
    if len(schoolkids) > 1:
        print('There is more than one student with this name')
        return
    if not schoolkids:
        print('There is more than one student with this name')
        return
    schoolkid = schoolkids[0]
    subject = Subject.objects.filter(title=subject_title, year_of_study=schoolkid.year_of_study)[0]
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject,
    ).order_by('-date')
    last_lesson = lessons.first()
    commendation = Commendation(
        text=random.choice(commendations),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=last_lesson.teacher,
    )
    print(commendation)
    commendation.save()
