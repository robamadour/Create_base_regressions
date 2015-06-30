# coding=utf-8

import re
from country import Country
from dummy import Dummy

def read_file(input_file, fy=1870, ly=2010):
    with open(input_file) as f:
        for line_number, line in enumerate(f):
            sp = re.split("\\t|\\n", line)
            sp = sp[:-1]
            if line_number == 0:
                for i in range(1, len(sp)):
                    Country.country_list.append(Country(int(sp[i]), fy, ly))
            elif line_number == 1:
                for i in range(1, len(sp)):
                    Country.country_list[i-1].name = sp[i]
            else:
                year = int(sp[0])
                for i in range(1, len(sp)):
                    country = Country.country_list[i-1]
                    if sp[i] != '':
                        country.gdp[year] = float(sp[i])
                    else:
                        country.gdp[year] = 'NA'

    update_code_map()


def update_code_map():
    liszt = Country.country_list
    c_map = {}

    for idx, country in enumerate(liszt):
        c_map[country.code] = idx

    Country.code_map = c_map

def read_exits(input_file):
    exits = []
    with open(input_file) as f:
        for idx, line in enumerate(f):
            if idx > 0:
                sp = re.split("\\t|\\n", line)
                # sp = sp[:-1]
                exits.append([int(sp[0]), int(sp[1])])

    return exits

def print_dummies_file(output_file, exits, fy=1870, ly=2010):
    n_countries = len(Country.country_list)
    n_years = ly - fy

    dummies = []
    line = ""
    for i in range(n_countries):
        c_code = Country.country_list[i].code
        dummies.append(Dummy("country", c_code))
        line += "COUNTRY_" + str(c_code) + "\t"
    for year in range(fy + 1, ly + 1):
        dummies.append(Dummy("year", year))
        line += "YEAR_" + str(year) + "\t"
    for data in exits:
        dummies.append(Dummy("pre", [data[1], data[0]]))
        line += "PRE_" + str(data[1]) + "_" + str(data[0]) + "\t"
    for data in exits:
        dummies.append(Dummy("post", [data[1], data[0]]))
        line += "POST_" + str(data[1]) + "_" + str(data[0]) + "\t"

    line = line[:-1] + "\n"

    for year in range(fy+1, ly+1):
        for country in Country.country_list:
            for dummy in dummies:
                line += str(dummy.get_value(year, country.code)) + "\t"
            line = line[:-1] + "\n"
        print(year)

    f = open(output_file, "w")
    f.write(line)
    f.close()


def print_base_file(output_file, fy=1870, ly=2010, coma=False, ff="{0:.6f}"):
    line = "GROWTH\tCOUNTRY\tCOUNTRY1\tYEAR\tGDP\n"
    for year in range(fy+1, ly+1):
        for country in Country.country_list:
            country.compute_growths()
            growth = country.growth[year]
            gdp = country.gdp[year]

            if coma:
                if growth != 'NA':
                    growth = ff.format(growth)
                if gdp != 'NA':
                    gdp = "{0:.2f}".format(gdp)
            else:
                growth = str(growth)
                gdp = str(gdp)

            line += growth + "\t" + country.name + "\t" + str(country.code) +\
                    "\t" + str(year) + "\t" + gdp + "\n"

    f = open(output_file, "w")
    f.write(line)
    f.close()


work_dir = "C:\\Users\\Roberto\\Google Drive\\Memoria\\Codigo\\R\\1\\"
input_file = work_dir + "GDP_base_punto.txt"
output_file_c = work_dir + "GROWTH_BASE_coma.txt"
output_file_p = work_dir + "GROWTH_BASE_punto.txt"

read_file(input_file)
print_base_file(output_file_p)
print_base_file(output_file_c, coma=True)

exits_file = work_dir + "salidas_base.txt"
exits = read_exits(exits_file)

dummies_file = work_dir + "DUMMIES.txt"
print_dummies_file(dummies_file, exits)