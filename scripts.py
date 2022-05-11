import logging
import random

from datacenter.models import Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject
from typing import List, Optional


def get_schoolkid(schoolkid_full_name: str) -> Optional[Schoolkid]:
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
    except Schoolkid.DoesNotExist:
        logging.info(f'There is less than one student with this name')
    except Schoolkid.Schoolkid.MultipleObjectsReturned:
        logging.info(f'There is more than one student with this name')


def fix_marks(schoolkid_full_name: str) -> None:
    schoolkid = get_schoolkid(schoolkid_full_name)
    if schoolkid:
        Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid_full_name: str) -> None:
    schoolkid = get_schoolkid(schoolkid_full_name)
    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()


def get_commendations() -> List[str]:
    return [
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


def create_commendation(schoolkid_full_name: str, subject_title: str) -> None:
    schoolkid = get_schoolkid(schoolkid_full_name)
    if not schoolkid:
        return
    subject = Subject.objects.filter(title=subject_title, year_of_study=schoolkid.year_of_study).get()
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject,
    ).order_by('-date')
    if not lessons:
        logging.info('There is no lessons with this student')
        return
    last_lesson = lessons.get()
    commendation = Commendation(
        text=random.choice(get_commendations()),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=last_lesson.teacher,
    )
    commendation.save()
