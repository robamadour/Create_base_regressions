class Dummy(object):

    def __init__(self, type, data):
        self.type = type
        self.data = data

    def get_value(self, year, country):

        if self.type == "country":
            if self.data == country:
                return 1
            else:
                return 0
        elif self.type == "year":
            if self.data == year:
                return 1
            else:
                return 0
        elif self.type == "pre":
            if (self.data[0] - year) > 0 and (self.data[0] - year) < 6 and \
                    self.data[1] == country:
                return 1
            else:
                return 0
        elif self.type == "post":
            if (year - self.data[0]) < 6 and (year - self.data[0]) > 0 and \
                    self.data[1] == country:
                return 1
            else:
                return 0
        else:
            return "NA"