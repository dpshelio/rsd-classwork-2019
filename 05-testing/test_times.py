import datetime

import pytest

import times


@pytest.mark.parametrize('test_input, expected', [
    #(input ranges, expected ranges)
    # given input
    ([["2010-01-12 10:00:00", "2010-01-12 12:00:00"], ["2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60]], [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]),
    # class time
    ([["2019-10-31 10:00:00", "2019-10-31 13:00:00"], ["2019-10-31 10:05:00", "2019-10-31 12:55:00", 3, 600]], times.time_range("2019-10-31 10:05:00", "2019-10-31 12:55:00", 3, 600)),
    # no overlap
    ([["2019-01-01 00:00:00", "2019-01-01 23:50:00"], ["2019-01-02 00:30:00", "2019-01-02 23:55:00"]], []),
    # touching edges
    ([["2019-10-31 00:00:00", "2019-10-31 00:50:00", 3, 600], ["2019-10-31 00:10:00", "2019-10-31 01:00:00", 3, 600]], []),
])
def test_many(test_input, expected):
    large = times.time_range(*test_input[0])
    short = times.time_range(*test_input[1])
    result = times.overlap_time(large, short)
    assert result == expected

def test_20_min():
    large = times.time_range("2019-01-01 00:00:00", "2019-01-01 23:50:00", 24, 10 * 60)
    short = times.time_range("2019-01-01 00:30:00", "2019-01-01 23:55:00", 24, 35 * 60)
    result = times.overlap_time(large, short)
    assert all([(datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S") - 
    datetime.datetime.strptime(t0, "%Y-%m-%d %H:%M:%S")).total_seconds() == 20 * 60
    for t0, t1 in result])
