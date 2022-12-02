import csv


def read_file(file_name: str) -> tuple:
    """
    Функция извлекает данные их csv файла, возвращает заголовки и записи.
    К каждой записи присваивается id.

    :param file_name: str
    :return: tuple
    """
    data = []
    with open(file_name, 'r', encoding='utf-8') as file:
        headers = file.readline().rstrip('\n').split(',')
        id_data = 1
        for line in file:
            a = tuple(line.rstrip('\n').split(','))

            data.append({id_data: a})
            id_data += 1

    return headers, data


def partition(nums, low, high):
    pivot = nums[(low + high) // 2]
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while nums[i] < pivot:
            i += 1

        j -= 1
        while nums[j] > pivot:
            j -= 1

        if i >= j:
            return j

        nums[i], nums[j] = nums[j], nums[i]


def quick_sort(nums):
    def _quick_sort(items, low, high):
        if low < high:
            split_index = partition(items, low, high)
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)

    _quick_sort(nums, 0, len(nums) - 1)


def write_data(data: list, columns:dict, sorted_list: list, limit: int, order: str, file_name: str) -> None:
    """
    Функция записывает отсортированные и ограниченные лимитом строк данные
    в csv файл.

    :param data: list
    :param columns: dict
    :param sorted_list: list
    :param limit: int
    :param order: str
    :param file_name: str
    :return: None
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        if order == 'asc':
            top = [data[columns[str(item)]] for item in sorted_list[:limit]]

        elif order == 'desc':
            top_inverse = [data[columns[str(item)]] for item in sorted_list[-limit:]]
            top = top_inverse[::-1]

        top_without_id = []
        for d_dict in top:
            for v in d_dict.values():
                top_without_id.append('|'.join(v))

        top_writer = csv.writer(file, delimiter='\n', quoting=csv.QUOTE_MINIMAL)
        top_writer.writerow(top_without_id)

        print('data uploaded to file')


def select_sorted(sort_column: str, order: str, limit: int, file_name: str) -> None:
    """
    Функция создает словарь для сортировки по выбранному столбцу,
    создает список значений выбранного столбца, а также словарь для сохранения
    соответствия id записи.
    Внутри функции также вызываются функции для быстрой сортировки
    и записи отсортированных данных в файл.

    :param sort_column: str
    :param order: str
    :param limit: int
    :param file_name: str
    :return: None
    """
    headers, all_data = read_file('../all_stocks_5yr.csv')

    headers_dict = {}
    v = 0
    for head in headers:
        headers_dict[head] = v
        v += 1

    list_to_sort = []
    columns_id_dict = {}
    id_c = 1
    for data_d in all_data:
        for data in data_d.values():
            column = data[headers_dict[sort_column]]
            if column == '':
                column = 0
            list_to_sort.append(float(column))
            columns_id_dict[column] = id_c
            id_c += 1

    quick_sort(list_to_sort)

    write_data(all_data, columns_id_dict, list_to_sort, limit, order, file_name)


if __name__ == '__main__':
    select_sorted(sort_column='high', order='desc', limit=10, file_name='../dump.csv')
