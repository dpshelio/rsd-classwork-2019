import datetime

def time_range(t0, t1, n=1, g=0):
    t0_s = datetime.datetime.strptime(t0, "%Y-%m-%d %H:%M:%S")
    t1_s = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    d = (t1_s - t0_s).total_seconds() / n + g * (1/n - 1)
    sec_range = [(t0_s + datetime.timedelta(seconds=i * d + i * g),
                  t0_s + datetime.timedelta(seconds=(i + 1) * d + i * g)) for i in range(n)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


def overlap_time(obs1, obs2):
    ot = []
    for tr0, tr1 in obs1:
        for tra, trb in obs2:
            low = max(tr0, tra)
            high = min(tr1, trb)
            ot.append((low, high))
    return ot


if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(overlap_time(large, short))

