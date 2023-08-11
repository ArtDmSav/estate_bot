import re

from functions.time_count_decorator import time_count


# First searching price keywords
@time_count
def f_price(msg):
    r_str = r"((price)?(евро)?(cтоимость)?(цена)?(в)?(за)?(аренд[аы])?(euro)?(eur)? ?(мес)?(месяц)?[€\-💶💴:/]? ?" \
            r"\d{1,3}[\.',\s]?\d{3}" \
            r" ?(price)?(евро)?(euro)?(eur)?[€\-💶💴:/]?(cтоимость)?(цена)? ?(в)?(за)?(аренд[аы])? ?(мес)?(месяц)?)" \
            r"|((price)?(евро)?(cтоимость)?(цена)?(в)?(за)?(аренд[аы])?(euro)?(eur)? ?(мес)?(месяц)?[€\-💶💴:/]? ?" \
            r"\d{3}" \
            r" ?(price)?(евро)?(euro)?(eur)?[€\-💶💴:/]?(cтоимость)?(цена)? ?(в)?(за)?(аренд[аы])? ?(мес)?(месяц)?)"

    # List with our keywords in tuple in list
    first_search = re.findall(r_str, msg)

    # Rewrite num in list without empty string
    first_numbers = [el_s for _ in first_search for el_s in _ if el_s != '']

    # Catch typecast error
    # If catch error we return result = -1, after we can identify this result (-1) like an error
    try:
        return int(clean_price(first_numbers))
    except ValueError:
        return -1


# Second clean price search
def clean_price(first_number):
    re_clean_price = r"(\d{1,3}[\.',\s]?\d{3})|(\d{3})"
    flag = True
    second_number = []
    trig_w = ["евро", "euro", "eur", "€", "💶", "💴", "price", "цена", "cтоимость"]
    result = []
    for string in first_number:
        for key_w in trig_w:
            if flag and key_w in string:
                flag = False
                num = re.findall(re_clean_price, string)
                second_number = [el_s for _ in num for el_s in _ if el_s != '']
                if not second_number:
                    flag = True
                    continue
                flag_2 = True
                for elem in second_number:
                    for ch in [",", ".", " "]:
                        if ch in elem:
                            result.append(elem.replace(ch, ""))
                            flag_2 = False
                            break
                    if flag_2:
                        result.append(elem)
                return result[0]
    # If we can't find match with list 'trig_w', we start finding price in first search list
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
            return -1
        try:
            return result[0]
        except IndexError:
            return -1
