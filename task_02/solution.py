"""Задание 2. Агломеративная кластеризация пользователей."""


USERS = ["U1", "U2", "U3", "U4", "U5"]
R = 0.85

# Достаточно хранить одну половину симметричной матрицы.
SIMILARITY = {
    ("U1", "U2"): 0.95,
    ("U1", "U3"): 0.90,
    ("U1", "U4"): 0.85,
    ("U1", "U5"): 0.80,
    ("U2", "U3"): 0.75,
    ("U2", "U4"): 0.70,
    ("U2", "U5"): 0.65,
    ("U3", "U4"): 0.60,
    ("U3", "U5"): 0.80,
    ("U4", "U5"): 0.70,
}


def user_similarity(first, second):
    if first == second:
        return 0.0
    key = tuple(sorted((first, second)))
    return SIMILARITY[key]


def cluster_similarity(first_cluster, second_cluster):
    """Метод ближайшего соседа: максимум сходств между элементами."""
    best = 0.0
    for first_user in first_cluster:
        for second_user in second_cluster:
            value = user_similarity(first_user, second_user)
            if value > best:
                best = value
    return best


def cluster_name(cluster):
    return "{" + ", ".join(cluster) + "}"


def print_matrix(clusters):
    names = [cluster_name(cluster) for cluster in clusters]
    width = max(16, max(len(name) for name in names) + 2)
    print(" " * width + "".join(f"{name:>{width}}" for name in names))
    for i, first in enumerate(clusters):
        line = f"{names[i]:<{width}}"
        for j, second in enumerate(clusters):
            value = 0.0 if i == j else cluster_similarity(first, second)
            line += f"{value:>{width}.2f}"
        print(line)


def closest_clusters(clusters):
    best_value = -1.0
    best_pair = None
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            value = cluster_similarity(clusters[i], clusters[j])
            if value > best_value:
                best_value = value
                best_pair = (i, j)
    return best_pair, best_value


def main():
    clusters = [(user,) for user in USERS]
    step = 0

    print(f"Порог объединения R = {R:.2f}")
    print("Связь кластеров: максимум попарных сходств (ближайший сосед).")
    print("\nНачальная матрица:")
    print_matrix(clusters)

    while len(clusters) > 1:
        (first, second), similarity = closest_clusters(clusters)
        if similarity < R:
            print(f"\nМаксимальное оставшееся сходство {similarity:.2f} < R.")
            break

        step += 1
        left = clusters[first]
        right = clusters[second]
        merged = tuple(sorted(left + right))
        print(
            f"\nШаг {step}: {cluster_name(left)} + {cluster_name(right)}, "
            f"сходство = {similarity:.2f}"
        )

        clusters = [
            cluster
            for index, cluster in enumerate(clusters)
            if index not in (first, second)
        ]
        clusters.insert(0, merged)
        print_matrix(clusters)

    print("\nИтоговые кластеры:")
    for cluster in clusters:
        print(" ", cluster_name(cluster))


if __name__ == "__main__":
    main()
