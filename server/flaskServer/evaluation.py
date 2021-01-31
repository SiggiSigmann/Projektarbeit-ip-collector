import dbconnector.dbconnector as dbcon
import sys
import datetime

###
# Evaluation data
###
class Evaluation():
    def __init__(self, datadb):
        self.datadb = datadb

    #returns most likely user
    def max_likely_user(self, ip):
        now = datetime.datetime.now()
        to_date = now.strftime("%Y-%m-%d")
        data = self.datadb.get_user_distribution_for_ip(ip, self.datadb.get_first_measurement(), to_date)

        if len(data)>0:
            return 1, data[0][0]

        return 0, "nothing"
