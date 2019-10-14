import math
import unittest

try:
    from nose_parameterized import parameterized
except ImportError:
    print("*** Please install 'nose_parameterized' to run these tests ***")
    exit(0)


import oandapyV20.contrib.factories as req


class TestContribFactories(unittest.TestCase):
    """Tests regarding contrib factories.

    The reference is created using the second dict parameter. The
    first dict parameter is merge with this, but only for the keys
    that do NOT exist. That allows us to override parameters.
    The result should reflect the data constructed by the class

    """

    @parameterized.expand([
       (req.InstrumentsCandlesFactory,
           "DE30_EUR",
           {},
           {"len": 1},
        ),
       (req.InstrumentsCandlesFactory,
           "DE30_EUR",
           {"from": "2017-01-01T00:00:00Z",
            "to": "2017-01-02T00:00:00Z",
            "granularity": "M1"},
           {"len": int(math.ceil(24*60.0 / 500))},
        ),
       (req.InstrumentsCandlesFactory,
           "DE30_EUR",
           {"from": "2017-01-01T00:00:00Z",
            "granularity": "M1"},
           {},
        ),
       (req.InstrumentsCandlesFactory,
           "DE30_EUR",
           {"from": "2017-01-01T00:00:00Z",
            "to": "2022-06-30T00:00:00Z",
            "granularity": "M1"},
           {},
        ),
       (req.InstrumentsCandlesFactory,
           "DE30_EUR",
           {"to": "2017-06-30T00:00:00Z",
            "granularity": "M1"},
           {},
           ValueError,
        ),
       (req.InstrumentsCandlesFactory,
           "EUR_GBP",
           {"from": "2017-04-01T00:00:00Z",
            "to": "2017-09-23T00:00:00Z",
            "granularity": "M30"},
           {"len": 17},
        ),
       (req.InstrumentsCandlesFactory,
           "DE30_EUR",
           {"from": "2017-01-01T00:00:00Z",
            "to": "2017-06-30T00:00:00Z",
            "granularity": "H4"},
           {"len": 3},
        ),
       (req.InstrumentsCandlesFactory,
           "DE30_EUR",
           {"from": "2017-01-01T00:00:00Z",
            "to": "2017-06-30T00:00:00Z",
            "count": 5000,         # same as previous, but increase batchsize
            "granularity": "H4"},
           {"len": 1},
        ),
    ])
    def test__candlehistory(self, factory, instrument, inpar, refpar,
                            exc=None):
        """candlehistoryfactory."""
        if not exc:
            # run the factory
            i = 0
            for r in factory(instrument, params=inpar):
                if i == 0 and inpar:
                    self.assertTrue(r.params['from'] == inpar['from'])
                    # the calculated 'to' should be there
                    self.assertTrue('to' in r.params)
                if 'len' in refpar and i == refpar['len']:
                    self.assertTrue('to' not in r.params)
                i += 1

        # else:
        #     with self.assertRaises(exc) as err:
        #         r = factory(instrument, params=inpar)


if __name__ == "__main__":

    unittest.main()
