import time

f_time = []


def full_time():
    s_time = round(sum(f_time), 2)
    if s_time > 60:
        print(f"[*] Время выполнения всей программы {int(s_time // 60)} минут {int(s_time % 60)} секунд.")
        f_time.clear()
    else:
        print(f"[*] Время выполнения всей программы {s_time} секунд.")
        f_time.clear()


def time_count(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        return_val = func(*args, **kwargs)
        end = time.time()
        f_time.append(end - start)
        print(f"[*] Время выполнения функции {func.__name__}: {round(end-start,3)} секунд.")
        return return_val

    return wrapper
