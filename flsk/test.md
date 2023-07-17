Partitions count

    def count_partitions(n: int, m: int) -> int:
        if n == 0:
            return 1
        elif n < 0:
            return 0
        elif m == 0:
            return 0

        return count_partitions(n - m, m) + count_partitions(n, m - 1)