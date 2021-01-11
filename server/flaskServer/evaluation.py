import dbconnector.dbconnector as dbcon
import sys

###
# Evaluation data
###
class Evaluation():
    def __init__(self, datadb):
        self.datadb = datadb

    #returns most likely user
    def max_likely_user(self, ip):
        data = self.datadb.get_user_for_ip(ip)

        if len(data)>0:
            return 1, data[0][0]

        return 0, "nothing"
