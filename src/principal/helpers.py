import hashlib
import math


def have_more(total, npp, page):
    if total % (npp * page) == total:
        return False

    if total % (npp * page) == 0:
        return False

    return True


def paginator(current_page, objects, epp=5):
    """Função paginadora

    Args:
        current_page (int): página atual
        objects (any): objetos a serem paginados
        epp (int, optional): Número de elementos por página. Por padrão, este valor é 5.

    Returns:
        any: Objetos paginados
        int: Total de páginas
        range: Intervalo [a,b) em que a página atual está inserida
    """

    total = math.ceil(len(objects) / epp)

    if current_page <= 4:
        if total <= current_page + 3:
            bounds = range(1, total + 1)

        else:
            bounds = range(1, current_page + 3)

    elif current_page + 3 >= total:
        bounds = range(current_page - 2, total + 1)

    else:
        bounds = range(current_page - 2, current_page + 3)

    result = paginate(objects, current_page, epp)

    return result, total, bounds


def qnt_page(qnt_ant, qnt_pos):
    if qnt_ant > qnt_pos:
        return qnt_ant

    return qnt_pos


def join_range(rng1, rng2, qnt_page):
    if rng2 != range(1, 1) and rng1 != range(1, 1):
        rng = rng1 if rng1[0] <= rng2[0] else rng2

        if rng1[-1] >= rng2[-1]:
            rng = range(rng[0], rng1[-1] + 1)
        else:
            rng = range(rng[0], rng2[-1] + 1)

        return rng

    if rng1 == range(1, 1):
        return rng2

    if rng2 == range(1, 1):
        return rng1

    return None


def email_token(email):
    return hashlib.md5(
        "[Jmh!&DKfY#u&l#4zvFXw5mV4iD(uEmUW]:{}".format(email.lower()).encode(),
        usedforsecurity=False,
    ).hexdigest()


def paginate(obj, page, npp):
    return obj[((page - 1) * npp) : ((page) * npp)]
