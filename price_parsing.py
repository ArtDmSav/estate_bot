import re


def f_price(msg):
    r_str = r"((price)?(евро)?(cтоимость)?(цена)?(в)?(за)?(аренд[аы])?(euro)?(eur)? ?(мес)?(месяц)?[€\-💶💴:/]? ?" \
            r"\d{1,3}[\.',\s]?\d{3}" \
            r" ?(price)?(евро)?(euro)?(eur)?[€\-💶💴:/]?(cтоимость)?(цена)? ?(в)?(за)?(аренд[аы])? ?(мес)?(месяц)?)" \
            r"|((price)?(евро)?(cтоимость)?(цена)?(в)?(за)?(аренд[аы])?(euro)?(eur)? ?(мес)?(месяц)?[€\-💶💴:/]? ?" \
            r"\d{3}" \
            r" ?(price)?(евро)?(euro)?(eur)?[€\-💶💴:/]?(cтоимость)?(цена)? ?(в)?(за)?(аренд[аы])? ?(мес)?(месяц)?)"
    num = re.findall(r_str, msg)  # лист с найдеными значениями // заменить на re.search
    first_numbers = []

    for elem_list in num:  # перезаписываем в лист без пустых строк
        for elem_str in elem_list:
            if elem_str != '':
                first_numbers.append(elem_str)
    # print('first_number = ', first_numbers)           # чеккаем глазами поллученый лист в консоли
    try:  # ловим ошибку приведения типов
        return int(clean_price(first_numbers))  # запускаем вторую функцию и возвращаем результат
    except ValueError:  # выдаем результат -1 который можно идентифицировать ошибкой
        # print("exeption: type = str")
        return -1


def clean_price(first_number):
    re_clean_price = r"(\d{1,3}[\.',\s]?\d{3})|(\d{3})"
    flag = True
    second_number = []
    result = []
    for string in first_number:
        for key_w in ["евро", "euro", "eur", "€", "💶", "💴", "price", "цена", "cтоимость"]:
            if flag and key_w in string:
                flag = False
                num = re.findall(re_clean_price, string)
                for elem_list in num:
                    for elem_str in elem_list:
                        if elem_str != '':
                            second_number.append(elem_str)
                # print("second number = ", second_number)
                if not second_number:
                    flag = True
                    continue
                flag_2 = True
                for elem in second_number:
                    for ch in [",", ".", " "]:
                        if ch in elem:
                            # print('append result = ', elem.replace(ch, ""))
                            result.append(elem.replace(ch, ""))
                            flag_2 = False
                            break  # установить continue для допуска более 1 цены
                    if flag_2:
                        result.append(elem)
                # print("result = ", result)
                return result[0]
    if flag:
        for string in first_number:
            if re.findall(re_clean_price, string):
                if string != "":
                    second_number.append(string.replace(" ", ""))
        flag = False
        for elem in second_number:
            flag_2 = True
            for ch in [".", ","]:
                if ch in elem:
                    flag_2 = False
                    result.append(elem.replace(ch, ""))
            if flag_2:
                result.append(elem)
        result.sort(reverse=True)
        if not result:
            flag = True
        try:
            return result[0]
        except IndexError:
            # print("except IndexError")
            return -1
