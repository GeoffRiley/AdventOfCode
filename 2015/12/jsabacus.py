import json
from numbers import Number

from typing import Union


# Based on multiple code samples from stackoverflow questions about flattening nested structures

def _do_flatten(obj, prefix=None, skip_dicts_with=None):
    rows = []
    dot_prefix = prefix and (prefix + ".") or ""
    if isinstance(obj, dict):
        if not obj:
            rows.append(((prefix or "") + "$empty", "{}"))
        else:
            if skip_dicts_with is None or skip_dicts_with not in obj.values():
                for key, item in obj.items():
                    rows.extend(_do_flatten(item, prefix=dot_prefix + key, skip_dicts_with=skip_dicts_with))
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            rows.extend(_do_flatten(item, prefix=dot_prefix + str(i), skip_dicts_with=skip_dicts_with))
    elif obj is None:
        rows.append(((prefix or "") + "$none", "None"))
    elif isinstance(obj, bool):
        rows.append(((prefix or "") + "$bool", obj))
    elif isinstance(obj, int):
        rows.append(((prefix or "") + "$int", obj))
    elif isinstance(obj, float):
        rows.append(((prefix or "") + "$float", obj))
    else:
        rows.append((prefix, str(obj)))
    return rows


def flatten(obj, skip_dicts_with=None):
    return dict(_do_flatten(obj, skip_dicts_with=skip_dicts_with))


def jsabacus(doc: str, skip_dicts_with=None) -> int:
    j = json.loads(doc)
    k = flatten(j, skip_dicts_with=skip_dicts_with)
    ans = 0
    v: Union[str, bool, int, float]
    for v in k.values():
        if isinstance(v, Number):
            ans += int(v)
    return ans


if __name__ == '__main__':
    with open('input') as f:
        document = f.read()

    res = jsabacus(document)
    print(f'Part 1: {res}')
    res = jsabacus(document, skip_dicts_with='red')
    print(f'Part 2: {res}')

    '''
    Part 1: 191164
    Part 2: 87842
    '''
