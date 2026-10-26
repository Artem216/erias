"""Задание 3. Фильтрация и разреженное хранение матрицы."""


PRODUCTS = ["P1", "P2", "P3", "P4", "P5", "P6"]
USERS = ["U1", "U2", "U3", "U4", "U5"]
RATINGS = [
    [5, 4, 5, 0, 5],
    [5, 5, 5, 0, 5],
    [5, 4, 4, 0, 5],
    [4, 3, 4, 0, 3],
    [0, 0, 0, 0, 0],
    [4, 5, 5, 0, 1],
]
MIN_AVERAGE = 4.0


def nonzero_average(row):
    total = 0
    count = 0
    for value in row:
        if value != 0:
            total += value
            count += 1
    return total / count if count else 0.0


def active_column_indexes(matrix):
    indexes = []
    for column in range(len(matrix[0])):
        active = False
        for row in matrix:
            if row[column] != 0:
                active = True
                break
        if active:
            indexes.append(column)
    return indexes


def filter_matrix():
    active_columns = active_column_indexes(RATINGS)
    kept_products = []
    filtered = []

    for product, row in zip(PRODUCTS, RATINGS):
        average = nonzero_average(row)
        print(f"{product}: средняя ненулевая оценка = {average:.2f}")
        if average >= MIN_AVERAGE:
            kept_products.append(product)
            filtered.append([row[column] for column in active_columns])

    kept_users = [USERS[column] for column in active_columns]
    return kept_products, kept_users, filtered


def to_coo(matrix):
    """COO: параллельные массивы значений, строк и столбцов."""
    values, rows, columns = [], [], []
    for row_number, row in enumerate(matrix):
        for column_number, value in enumerate(row):
            if value != 0:
                values.append(value)
                rows.append(row_number)
                columns.append(column_number)
    return values, rows, columns


def to_csr(matrix):
    """CSR: значения, столбцы и начало каждой строки."""
    values, columns = [], []
    row_index = [0]
    for row in matrix:
        for column_number, value in enumerate(row):
            if value != 0:
                values.append(value)
                columns.append(column_number)
        row_index.append(len(values))
    return values, columns, row_index


def to_ellpack(matrix):
    """ELLPACK: равное число ячеек на строку с заполнением нулями."""
    max_nonzero = max(sum(value != 0 for value in row) for row in matrix)
    values_table = []
    columns_table = []

    for row in matrix:
        values = []
        columns = []
        for column_number, value in enumerate(row):
            if value != 0:
                values.append(value)
                columns.append(column_number)
        while len(values) < max_nonzero:
            values.append(0)
            columns.append(0)
        values_table.append(values)
        columns_table.append(columns)

    return values_table, columns_table


def print_dense(products, users, matrix):
    print("       " + "".join(f"{user:>5}" for user in users))
    for product, row in zip(products, matrix):
        print(f"{product:>5}  " + "".join(f"{value:>5}" for value in row))


def main():
    print(f"Порог среднего рейтинга: {MIN_AVERAGE:.1f}\n")
    products, users, matrix = filter_matrix()

    print("\nПосле удаления нулевого/низкого рейтинга и неактивных пользователей:")
    print_dense(products, users, matrix)

    coo_values, coo_rows, coo_columns = to_coo(matrix)
    print("\nCOO:")
    print("  Value =", coo_values)
    print("  Row   =", coo_rows)
    print("  Col   =", coo_columns)

    csr_values, csr_columns, csr_row_index = to_csr(matrix)
    print("\nCSR:")
    print("  Value    =", csr_values)
    print("  Col      =", csr_columns)
    print("  RowIndex =", csr_row_index)

    ell_values, ell_columns = to_ellpack(matrix)
    print("\nELLPACK:")
    print("  Value  =", ell_values)
    print("  Column =", ell_columns)


if __name__ == "__main__":
    main()
