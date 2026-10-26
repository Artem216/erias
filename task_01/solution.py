"""Задание 1. Поиск похожих товаров и пользователей."""

from math import sqrt


PRODUCTS = ["P1", "P2", "P3", "P4", "P5", "P6"]
USERS = ["U1", "U2", "U3", "U4", "U5"]

# Строки — товары, столбцы — пользователи.
RATINGS = [
    [5, 4, 5, 3, 5],
    [5, 5, 5, 3, 5],
    [5, 4, 4, 2, 5],
    [5, 3, 5, 0, 3],
    [5, 0, 5, 0, 0],
    [4, 5, 5, 3, 1],
]


def cosine(vector_a, vector_b):
    """Косинусное сходство без специальных библиотек."""
    scalar_product = 0
    length_a_squared = 0
    length_b_squared = 0

    for a, b in zip(vector_a, vector_b):
        scalar_product += a * b
        length_a_squared += a * a
        length_b_squared += b * b

    if length_a_squared == 0 or length_b_squared == 0:
        return 0.0

    return scalar_product / sqrt(length_a_squared * length_b_squared)


def transpose(matrix):
    """Меняет строки и столбцы местами с помощью обычных циклов."""
    result = []
    for column_number in range(len(matrix[0])):
        column = []
        for row in matrix:
            column.append(row[column_number])
        result.append(column)
    return result


def find_pairs(names, vectors):
    """Возвращает все пары, отсортированные от самых похожих."""
    pairs = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            similarity = cosine(vectors[i], vectors[j])
            pairs.append((similarity, names[i], names[j]))
    pairs.sort(reverse=True)
    return pairs


def print_top(title, pairs, count=2):
    print(title)
    for place, (similarity, first, second) in enumerate(pairs[:count], 1):
        print(f"  {place}. {first} - {second}: {similarity:.6f}")


def main():
    product_pairs = find_pairs(PRODUCTS, RATINGS)
    user_pairs = find_pairs(USERS, transpose(RATINGS))

    print("Косинусное сходство: (A · B) / (|A| · |B|)\n")
    print_top("Два самых близких товара:", product_pairs)
    print()
    print_top("Два самых близких пользователя:", user_pairs)


if __name__ == "__main__":
    main()
