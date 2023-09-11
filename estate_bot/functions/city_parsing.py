import re

from estate_bot.functions.time_count_decorator import time_count


@time_count
def parse(msg):
    # Write city name on 3 language (En, Gr[en transcription], Ru)
    re_limassol = r"(л[ие]м[ао]сс?ол[ае]?)|(l[ie]m[ae]ss?o[ls])|(n[ei]ap[oa]lis)|(lim)|(лим)"
    re_larnaka = r"(л[ао]рнак[ае])|(l[ae]r[nv]aka)"
    re_pafos = r"(паф[ао]сс?е?)|(paf[ao]ss?)"
    re_nikosiya = r"(н[ие]к[оа]сс?и[яи])|(n[ie]k[oa]ss?ia)|(lefkosa)"

    if re.search(re_limassol, msg):
        return "Лимассол"
    if re.search(re_larnaka, msg):
        return "Ларнака"
    if re.search(re_pafos, msg):
        return "Пафос"
    if re.search(re_nikosiya, msg):
        return "Никосия"

    return "Кипр"
