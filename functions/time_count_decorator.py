f_time = []


def full_time():
    s_time = round(sum(f_time), 2)
    if s_time > 60:
        print(f"[*] Время выполнения всей программы {int(s_time // 60)} минут {int(s_time % 60)} секунд.")
    else:
        print(f"[*] Время выполнения всей программы {s_time} секунд.")


def time_count(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        return_val = func(*args, **kwargs)
        end = time.time()
        print(f'[*] Время выполнения {func.__name__}: {round((end - start), 3)} секунд.')
        f_time.append(end - start)
        return return_val

    return wrapper
