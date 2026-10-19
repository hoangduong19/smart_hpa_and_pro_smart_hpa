# Spike load for improvement C2 (plan.md section 7): the same users as locustfile.py, but the user count jumps
# between a low base load and a spike instead of rising once and staying high.
#
#   0-3 min    50 users   base load
#   3-7 min   250 users   spike 1 (50 users/s, so the spike is reached in 4 s)
#   7-10 min   50 users   sudden drop
#   10-13 min 250 users   spike 2
#   13-15 min  50 users   drop
#
# --run-time stops a short trial early; --users and --spawn-rate are not read. tick() checks --run-time itself:
# Locust 2.46 waits for the shape to finish before it starts its own run-time timer, so -t alone never fires.
#
# Usage: locust -f locustfile_spike.py --host http://192.168.161.10 --headless -t 900s

from locust import LoadTestShape

from locustfile import WebsiteUser  # noqa: F401  (Locust picks up the user class from this module)

# (end of stage in seconds, users, spawn rate per second); make_user_metrics.py reads this for its phases
STAGES = [
    (180, 50, 5),
    (420, 250, 50),
    (600, 50, 50),
    (780, 250, 50),
    (900, 50, 50),
]


class SpikeShape(LoadTestShape):
    use_common_options = True

    def tick(self):
        t = self.get_run_time()
        run_time = self.runner.environment.parsed_options.run_time
        if run_time and t >= run_time:
            return None
        for end, users, rate in STAGES:
            if t < end:
                return users, rate
        return None
