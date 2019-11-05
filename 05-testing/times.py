import datetime

import requests

def time_range(t0, t1, n=1, g=0):
    if t1 < t0:
        raise ValueError("Stopping date should happen after than starting date")
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
             if tr0 <= tra <= tr1 or tr0 <= trb <= tr1:
                low = max(tr0, tra)
                high = min(tr1, trb)
                if low == high:
                    # If low and high are equal is that edges are touching
                    # and we don't want to return such element, continue to
                    # next element.
                    continue   
                ot.append((low, high))
    return ot

def iss_passes(lat, lon, n=5):
    """
    Returns a time_range like output for the passes of the International Space Station
    at a given location and for a number of days from today.
    """
    iss_request = requests.get("http://api.open-notify.org/iss-pass.json",
                               params={
                                   "lat": lat,
                                   "lon": lon,
                                   "n": n})

    if iss_request.status_code != 200:
        # the request have failed by any reason
        return []
    response = iss_request.json()['response']
    return [(datetime.datetime.fromtimestamp(x['risetime']).strftime("%Y-%m-%d %H:%M:%S"),
             (datetime.datetime.fromtimestamp(x['risetime'] + x['duration'])).strftime("%Y-%m-%d %H:%M:%S"))
            for x in response]


if __name__ == "__main__":
    print(iss_passes(51.5074, -0.1278)) # ISS passes over London

