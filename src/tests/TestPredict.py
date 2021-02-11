import unittest

from predict.predict import Predict


class TestPredict(unittest.TestCase):
    def setUp(self):
        self.obj = Predict(range(1, 10), 20, 50, 12)

    def test_get_characteristics(self):
        characteristics = [[1.999999999999548, 2.999999494626941, 3.9985044078324092,
                            4.805945120646411, 4.665466521057987, 4.3934251347398785,
                            4.261773749649913, 4.204215040347433, 4.180561657877333],

                           [19.684210526316374, 19.07692483705545, 17.441916045834613,
                            10.794929232608402, 2.7878368434545338, 0.7399545108421891,
                            0.23493189048010127, 0.0783608511411276, 0.025873400636012716]]
        self.assertEqual(self.obj.get_characteristics(), characteristics)

    def test_get_predict(self):
        predict = [['4', '4.8059', '10.7949'],
                   ['9', '4.1806', '0.0259'],
                   ['9', '4.1806', '0.0259']]
        self.assertEqual(self.obj.get_predict(), predict)


if __name__ == '__main__':
    unittest.main()
