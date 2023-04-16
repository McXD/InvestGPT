
def init_map():
    map = {"gender":0, "age":22, "income":50000, "personality":1, "deposit":900000,
           "in_debt":0, "marital_status":2, "income_expectation":1000000, "investment_purpose":1, "favourable_plan":1}
    return map




def map_risk_profile(map):
    """
        Map the risk profile (a dictionary) to a scalar value
    """
    expected_return = 1.0
    risk = 1.0
    #condition 10
    if map["favourable_plan"] == 0:
        expected_return = 0.08
        risk = 1.0
    elif map["favourable_plan"] == 1:
        expected_return = 0.06
        risk = 0.8
    else:
        expected_return = 0.03
        risk = 0.05
    #condition 1
    if map["gender"] == 0:
        expected_return *= 1.1
        risk *= 1.1
    else:
        expected_return *= 0.9
        risk *= 0.9
    #condition 2
    if 20 <= map["age"] <= 30:
        expected_return *= 1.5
        risk *= 1.5
    elif 30 <= map["age"] <= 50:
        expected_return *= 1.1
        risk *= 1.0
    else:
        expected_return *= 0.8
        risk *= 0.6
    #condition 3
    if 100000 <= map["income"] <= 300000:
        expected_return *= 0.8
        risk *= 0.8
    elif 300000 <= map["income"] <= 500000:
        expected_return *= 1.0
        risk *= 1.0
    else:
        expected_return *= 1.2
        risk *= 1.2
    #condition 4
    if map["personality"] == 0:
        expected_return *= 0.9
        risk *= 0.8
    else:
        expected_return *= 1.2
        risk *= 1.1
    #condition 5
    if 100000 <= map["deposit"] <= 300000:
        expected_return *= 0.8
        risk *= 0.8
    elif 300000 <= map["deposit"] <= 500000:
        expected_return *= 1.0
        risk *= 1.0
    else:
        expected_return *= 1.2
        risk *= 1.2
    #condition 6
    if map["in_debt"] == 0:
        expected_return *= 1.2
        risk *= 0.9
    else:
        expected_return *= 0.9
        risk *= 1.1
    #condition 7
    if map["marital_status"] == 0:
        expected_return *= 1.2
        risk *= 0.8
    elif map["marital_status"] == 1:
        expected_return *= 1.1
        risk *= 0.9
    elif map["marital_status"] == 2:
        expected_return *= 1.0
        risk *= 1.0
    else:
        expected_return *= 1.05
        risk *= 0.85
    #condition 8
    if 100000 <= map["income_expectation"] <= 300000:
        expected_return *= 0.8
        risk *= 0.8
    elif 300000 <= map["income_expectation"] <= 500000:
        expected_return *= 1.0
        risk *= 1.0
    else:
        expected_return *= 1.2
        risk *= 1.2
    #condition 9
    if map["investment_purpose"] == 0:
        expected_return *= 1.017
        risk *= 0.8
    elif map["investment_purpose"] == 1:
        expected_return *= 1.2
        risk *= 1.1
    else:
        expected_return *= 1.05
        risk *= 0.7
    result = [expected_return, risk]
    # output：0.296,2.483
    return result


if __name__ == '__main__':
    search = map_risk_profile(init_map())
    for i in search:
        print(i)

