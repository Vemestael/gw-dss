from database.db_api import DbApi


class InputData:
    @staticmethod
    def get_count_of_calls_by_range(date_start, date_end):
        info = DbApi.get_calls_info_by_date(date_start, date_end)
        avg_calls = []
        for el in info:
            avg_calls.append(el[2])

        ranges = []
        for i in range(0, 167, 8):
            ranges.append(avg_calls[i: i + 8])

        result = []
        for i in range(0, 21, 3):
            result.append(ranges[i:i + 3])

        lambda_by_shift = []
        for day in result:
            for shift in day:
                avg_lambda = 0
                for hour in shift:
                    avg_lambda += hour
                lambda_by_shift.append(avg_lambda / 8)

        result.clear()
        for i in range(0, 21, 3):
            result.append(lambda_by_shift[i:i + 3])

        return result
