import pytest
from lib.time_error import *
from unittest.mock import Mock

def test_construction():
    requester = Mock()
    timer = Mock()
    time_error = TimeError(requester, timer)
    assert (time_error.requester, time_error.timer) == (requester, timer)

def test_error():
    timer = Mock()
    timer.time.return_value = 1700578050.5

    requester = Mock()
    response = Mock()
    response.json.return_value = {
        'abbreviation': 'GMT', 'client_ip': '86.141.14.57',
        'datetime': '2023-11-21T14:47:30.698880+00:00', 'day_of_week': 2,
        'day_of_year': 325, 'dst': False, 'dst_from': None,
        'dst_offset': 0, 'dst_until': None, 'raw_offset': 0,
        'timezone': 'Europe/London', 'unixtime': 1700578050,
        'utc_datetime': '2023-11-21T14:47:30.698880+00:00',
        'utc_offset': '+00:00', 'week_number': 47
        }
    requester.get.return_value = response
    
    time_error = TimeError(requester, timer)
    assert time_error.error() == -0.5

