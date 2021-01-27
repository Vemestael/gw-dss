import src.core.libqtmcalc as libqtmcalc


class SMO:
    def __init__(self, channel_count, queue_count, la, mu, nu=0, n=-1):
        self.channel_count = channel_count
        self.queue_count = queue_count
        self.la = la
        self.mu = mu
        self.nu = nu
        self.n = n

    def solve(self):
        x = libqtmcalc.qtm(self.channel_count, self.queue_count, self.la, self.mu, self.nu, self.n)
        return [libqtmcalc.qtm_data.calc_avg_count_served_req(x), libqtmcalc.qtm_data.calc_avg_queue(x)]
