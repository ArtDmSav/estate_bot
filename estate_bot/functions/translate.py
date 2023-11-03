from googletrans import Translator
from estate_bot.functions.time_count_decorator import time_count


@time_count
def to_en(text):
    tr = Translator()
    result = tr.translate(text)
    return result.text


@time_count
def to_ru(text):
    tr = Translator()
    result = tr.translate(text, dest='ru')
    return result.text


@time_count
def to_el(text):
    tr = Translator()
    result = tr.translate(text, dest='el')
    return result.text
