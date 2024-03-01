import datetime

def generate_csv_filename():
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data_{timestamp}.csv"
    return filename


def concatenate(lst, separator=','):
    if not lst:
        return ""

    result = str(lst[0])
    for item in lst[1:]:
        result += separator + str(item)
    return result