from datetime import datetime

#returns strain with highest growth rate in the specified country
def growth(data, country):

#have map for each variant to its change in cases and calculate growth
        keys = ["Alpha", "B.1.1.277", "B.1.1.302", "B.1.1.519", "B.1.160", "B.1.177", "B.1.221", "B.1.258", "B.1.367", "B.1.620", "Beta", "Delta", "Epsilon", "Eta", "Gamma", "Iota", "Kappa", "Lambda", "Mu", "Omicron", "S:677H.Robin1", "S:677P.Pelican", "others", "non_who"]
        my_dict = {key: -100 for key in keys}
#r = (A/P)^(1/t) - 1 A= final amount, P = initial amount t = time r = rate
#calculate rate at which the new cases each day increases

        for strain in data[country]:
                sum = 0
                start = (0,0)
                max_case = (0,0)
                for date, num_cases in data[country][strain].items():

                        if sum == 0:
                                start = (date,num_cases)
                        if num_cases >= max_case[1]:
                            max_case = (date, num_cases)
                        sum+= num_cases

                date1 = datetime.strptime(max_case[0], "%Y-%m-%d") # Year, Month, Day
                date2 = datetime.strptime(start[0], "%Y-%m-%d")
                diff = (date1 - date2).days
                if(diff!=0):
                    my_dict[strain] = ((max_case[1]/start[1])**(1/diff))-1
                else:
                    my_dict[strain] = -1
        return max(my_dict, key=my_dict.get)


if __name__ == "__main__":
    data = {
        "United States" : {"B12" : {"10-12-21" : 2,
                                    "10-13-21" : 3,
                                    "10-14-21" : 10},
                           "B.1.1.519" : {"10-12-21" : 2,
                                          "10-13-21" : 10,
                                          "10-14-21" : 500}

                           },
        "France" : {"Norovirus" : {"10-10-21" : 10,
                                    "10-11-21" : 2,
                                    "10-12-21" : 1,},
                    "B12": {"10-12-21": 2,
                            "10-13-21": 3,
                            "10-14-21": 10}
                    }
    }
    print(growth(data, "United States"))

