# Copyright (c) Facebook, Inc. and its affiliates.
import operator
import unittest

import numpy.testing
import torcharrow.dtypes as dt
from torcharrow import IMapColumn


class TestMapColumn(unittest.TestCase):
    def base_test_map(self):
        c = self.ts.Column(dt.Map(dt.string, dt.int64))
        self.assertIsInstance(c, IMapColumn)

        c = c.append([{"abc": 123}])
        self.assertDictEqual(c[0], {"abc": 123})

        c = c.append([{"de": 45, "fg": 67}])
        self.assertDictEqual(c[1], {"de": 45, "fg": 67})

    def base_test_infer(self):
        c = self.ts.Column(
            [
                {"helsinki": [-1.0, 21.0], "moscow": [-4.0, 24.0]},
                {},
                {"nowhere": [], "algiers": [11.0, 25, 2], "kinshasa": [22.0, 26.0]},
            ]
        )
        self.assertIsInstance(c, IMapColumn)
        self.assertEqual(len(c), 3)
        self.assertEqual(c.dtype, dt.Map(dt.string, dt.List(dt.float32)))

        self.assertEqual(
            list(c),
            [
                {"helsinki": [-1.0, 21.0], "moscow": [-4.0, 24.0]},
                {},
                {"nowhere": [], "algiers": [11.0, 25, 2], "kinshasa": [22.0, 26.0]},
            ],
        )

    def base_test_keys_values_get(self):
        c = self.ts.Column([{"abc": 123}, {"de": 45, "fg": 67}])

        self.assertEqual(list(c.maps.keys()), [["abc"], ["de", "fg"]])
        self.assertEqual(list(c.maps.values()), [[123], [45, 67]])
        self.assertEqual(c.maps.get("de", 0), [0, 45])


if __name__ == "__main__":
    unittest.main()
