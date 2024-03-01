def concatenate(lst, separator=','):
    if not lst:
        return ""

    result = str(lst[0])
    for item in lst[1:]:
        result += separator + str(item)
    return result