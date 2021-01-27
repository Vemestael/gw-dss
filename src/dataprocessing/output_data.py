from src.database.db_api import DbApi


class OutputData:
    def __init__(self, predicts):
        for predict, predict_value in predicts.items():
            DbApi.add_new_predict(
                descriptor=predict,
                channel_count=predict_value.get('channel_count'),
                avg_count_of_served_requests=predict_value.get('n'),
                avg_queue_length=predict_value.get('l')
            )
