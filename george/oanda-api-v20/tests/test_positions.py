import sys
import unittest
import json
from . import unittestsetup
from .unittestsetup import environment as environment
from .unittestsetup import fetchTestData
import requests_mock


from oandapyV20 import API
import oandapyV20.endpoints.positions as positions
from oandapyV20.endpoints.positions import responses

access_token = None
accountID = None
account_cur = None
api = None


class TestPositions(unittest.TestCase):
    """Tests regarding the positions endpoints."""

    def setUp(self):
        """setup for all tests."""
        global access_token
        global accountID
        global account_cur
        global api
        # self.maxDiff = None
        try:
            accountID, account_cur, access_token = unittestsetup.auth()
            setattr(sys.modules["oandapyV20.oandapyV20"],
                    "TRADING_ENVIRONMENTS",
                    {"practice": {
                     "stream": "https://test.com",
                     "api": "https://test.com",
                     }})
            api = API(environment=environment,
                      access_token=access_token)
            api.api_url = 'https://test.com'
        except Exception as e:
            print("%s" % e)
            exit(0)

    @requests_mock.Mocker()
    def test__positions_list(self, mock_get):
        """get the positions list for an account."""
        tid = "_v3_accounts_accountID_positions"
        resp, data = fetchTestData(responses, tid)
        r = positions.PositionList(accountID)
        mock_get.register_uri('GET',
                              "{}/{}".format(api.api_url, r),
                              text=json.dumps(resp))
        result = api.request(r)
        self.assertTrue(resp == result)

    @requests_mock.Mocker()
    def test__openpositions_list(self, mock_get):
        """get the openpositions list for an account."""
        tid = "_v3_accounts_accountID_openpositions"
        resp, data = fetchTestData(responses, tid)
        r = positions.OpenPositions(accountID)
        mock_get.register_uri('GET',
                              "{}/{}".format(api.api_url, r),
                              text=json.dumps(resp))
        result = api.request(r)
        self.assertTrue(resp == result)

    @requests_mock.Mocker()
    def test__positiondetails(self, mock_get):
        """get the details of a single instrument's position."""
        tid = "_v3_accounts_accountID_positiondetails"
        resp, data = fetchTestData(responses, tid)
        r = positions.PositionDetails(accountID, instrument="EUR_USD")
        mock_get.register_uri('GET',
                              "{}/{}".format(api.api_url, r),
                              text=json.dumps(resp))
        result = api.request(r)
        self.assertTrue(resp == result)

    @requests_mock.Mocker()
    def test__positionclose(self, mock_put):
        """close single instrument's position long side."""
        tid = "_v3_accounts_accountID_position_close"
        resp, data = fetchTestData(responses, tid)
        r = positions.PositionClose(accountID, instrument="EUR_USD", data=data)
        mock_put.register_uri('PUT',
                              "{}/{}".format(api.api_url, r),
                              text=json.dumps(resp))
        result = api.request(r)
        self.assertTrue(resp == result)


if __name__ == "__main__":

    unittest.main()
