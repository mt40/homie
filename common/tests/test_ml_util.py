from common import ml_util
from common.tests import BaseTestCase

class MLUtilTests(BaseTestCase):
    def test_expense_projection_return_type(self):
        def _check(data, project_data):
            rs = ml_util.expense_projection(data, project_data)
            self.assertEqual(len(project_data), len(rs))
            for x in rs:
                self.assertIsInstance(x, int)

        _check([1, 1, 2], [2, 3])
        _check([1, 1, 2], [])
        _check([1], [])
        _check([1], [2, 3])