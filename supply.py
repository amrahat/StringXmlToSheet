import urllib, json
import sched, time

s = sched.scheduler(time.time, time.sleep)
#2019-07-03 12:29:58

url = "https://supply.p-stageenv.xyz/v1/drivers/2706"  # 2706#7083


def do_something(sc):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    if data['location']:
        print data['location']['last_location_ping_at']
    else:
        print "Null"
    # do your stuff

    s.enter(3, 1, do_something, (sc,))


s.enter(1, 1, do_something, (s,))
s.run()
