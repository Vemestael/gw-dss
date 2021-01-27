from src.core.core import SMO


class Predict:
    def __init__(self, channel_count_arr, queue_count, la, mu, nu=0, n=-1):
        self.channel_count_arr = channel_count_arr
        self.queue_count = queue_count
        self.la = la
        self.mu = mu
        self.nu = nu
        self.n = n

    def get_characteristics(self) -> list:
        n_arr = []  # count_served_req
        l_arr = []  # avg_queue
        for channel_count in self.channel_count_arr:
            smo = SMO(channel_count, self.queue_count, self.la, self.mu, self.nu, self.n)
            smo_solve = smo.solve()
            n_arr.append(float(smo_solve[0]))
            l_arr.append(float(smo_solve[1]))

        return [n_arr, l_arr]

    def get_predict(self) -> list:
        characteristics = self.get_characteristics()
        n_max = 0
        n_max_index = 0
        l_min = 20
        l_min_index = 0
        optimality_coefficient = 0
        optimality_coefficient_index = 0
        for i in range(len(self.channel_count_arr)):
            n = round(characteristics[0][i], 8)
            l = round(characteristics[1][i], 8)
            # наиболее оптимальный вариант - максимум заявок и минимум очереди
            coefficient = 0
            if l != 0:
                coefficient = n / l
            if n > n_max:
                n_max = n
                n_max_index = i
            if l < l_min:
                l_min = l
                l_min_index = i
            if coefficient > optimality_coefficient:
                optimality_coefficient = coefficient
                optimality_coefficient_index = i

        predict = [
            [f"{self.channel_count_arr[n_max_index]}",
             f"{round(n_max, 4)}",
             f"{abs(round(characteristics[1][n_max_index], 4))}"],

            [f"{self.channel_count_arr[optimality_coefficient_index]}",
             f"{round(characteristics[0][optimality_coefficient_index], 4)}",
             f"{abs(round(characteristics[1][optimality_coefficient_index], 4))}"],

            [f"{self.channel_count_arr[l_min_index]}",
             f"{round(characteristics[0][l_min_index], 4)}",
             f"{abs(round(l_min, 4))}"]
        ]

        return predict
