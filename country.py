class Country(object):
    country_list = []
    code_map = {}

    def __init__(self, code, fy, ly):
        self.name = ""
        self.code = code
        self.gdp = {}
        self.first_year = fy
        self.last_year = ly
        self.growth = {}

    def compute_growths(self):
        self.growth[self.first_year] = 'NA'
        for year in range(self.first_year +1, self.last_year +1):
            if self.gdp[year-1] != 'NA' and self.gdp[year] != 'NA':
                self.growth[year] = 100.0*(self.gdp[year] - self.gdp[year-1]) \
                / self.gdp[year-1]
            else:
                self.growth[year] = 'NA'

    def print_gdp_and_growth(self):
        line = self.name + "\n"
        line += "year\tgdp\tgrowth\n"
        for year in range(self.first_year, self.last_year + 1):
            line += str(year) + "\t" + str(self.gdp[year]) + "\t" + str(
                self.growth[year]) + "\n"
        print(line)
