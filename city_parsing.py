import re


def parse(msg):
    re_limassol = r"(л[ие]м[ао]сс?ол[ае]?)|(l[ie]m[ae]ss?o[ls])|(n[ei]ap[oa]lis)|(lim)|(лим)"
    re_find_lim = re.search(re_limassol, msg)  # чек англ транскрипции греческого языка
    if re_find_lim:
        return "Лимассол"

    re_larnaka = r"(л[ао]рнак[ае])|(l[ae]r[nv]aka)"
    re_find_lar = re.search(re_larnaka, msg)
    if re_find_lar:
        return "Ларнака"

    re_pafos = r"(паф[ао]сс?е?)|(paf[ao]ss?)"
    re_find_pafos = re.search(re_pafos, msg)
    if re_find_pafos:
        return "Пафос"

    re_nikosiya = r"(н[ие]к[оа]сс?и[яи])|(n[ie]k[oa]ss?ia)|(lefkosa)"
    re_find_nik = re.search(re_nikosiya, msg)
    if re_find_nik:
        return "Никосия"

    return "Кипр"
