"""Задание 4. Рекомендации по похожим предпочтениям пользователей."""


PRODUCTS = ["P1", "P2", "P3", "P4", "P5"]
USERS = ["U1", "U2", "U3", "U4"]

# Строки — товары, столбцы — пользователи.
RATINGS = [
    [5, 5, 4, 5],
    [5, 5, 3, 0],
    [5, 5, 5, 5],
    [5, 0, 2, 0],
    [0, 5, 1, 0],
]

# В задании матрица сходства дана для U1, U2 и U3; U4 исключён.
SIMILARITY = {
    ("U1", "U2"): 0.9,
    ("U1", "U3"): 0.7,
    ("U2", "U3"): 0.6,
}
NEIGHBOUR_COUNT = 1


def get_similarity(first, second):
    return SIMILARITY[tuple(sorted((first, second)))]


def user_ratings(user):
    column = USERS.index(user)
    return [row[column] for row in RATINGS]


def average_nonzero(values):
    total = 0
    count = 0
    for value in values:
        if value != 0:
            total += value
            count += 1
    return total / count if count else 0.0


def nearest_neighbours(target, product_index, allowed_users):
    candidates = []
    for user in allowed_users:
        if user == target:
            continue
        rating = user_ratings(user)[product_index]
        if rating != 0:
            candidates.append((get_similarity(target, user), user))
    candidates.sort(reverse=True)
    return candidates[:NEIGHBOUR_COUNT]


def predict(target, product_index, allowed_users):
    """Формула из задания, записанная через обычные циклы."""
    neighbours = nearest_neighbours(target, product_index, allowed_users)
    if not neighbours:
        return None, []

    target_average = average_nonzero(user_ratings(target))
    numerator = 0.0
    denominator = 0.0

    for similarity, neighbour in neighbours:
        neighbour_values = user_ratings(neighbour)
        neighbour_average = average_nonzero(neighbour_values)
        neighbour_rating = neighbour_values[product_index]
        numerator += (neighbour_rating - neighbour_average) * similarity
        denominator += abs(similarity)

    prediction = target_average + numerator / denominator
    return prediction, [user for similarity, user in neighbours]


def recommend(target, allowed_users):
    values = user_ratings(target)
    variants = []
    for product_index, rating in enumerate(values):
        if rating == 0:
            prediction, neighbours = predict(target, product_index, allowed_users)
            if prediction is not None:
                variants.append((prediction, PRODUCTS[product_index], neighbours))
    variants.sort(reverse=True)
    return variants[0] if variants else None


def cold_start_recommendation():
    """Для нового пользователя выбирает товар с наибольшим средним рейтингом."""
    variants = []
    for product, ratings in zip(PRODUCTS, RATINGS):
        variants.append((average_nonzero(ratings), product))
    variants.sort(reverse=True)
    return variants[0]


def main():
    allowed_users = ["U1", "U2", "U3"]
    print("User-based рекомендации, число ближайших соседей K = 1")
    print("U4 исключён: для него в задании не дана строка сходств.\n")

    for target in allowed_users:
        result = recommend(target, allowed_users)
        if result is None:
            print(f"{target}: все товары уже оценены")
            continue
        score, product, neighbours = result
        print(
            f"{target}: рекомендовать {product}, прогноз = {score:.2f}, "
            f"сосед = {', '.join(neighbours)}"
        )

    average, product = cold_start_recommendation()
    print(
        f"\nНовый пользователь: рекомендовать {product} "
        f"(средний рейтинг {average:.2f})"
    )


if __name__ == "__main__":
    main()
