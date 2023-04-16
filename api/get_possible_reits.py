import pandas as pd

def get_possible_reits(profile):
    """
    Use the expected return risk value to select possible REITs from the database
    :param profile: a scalar of expected return and risk
    :return: a list of REIT keys
    """


    df = pd.read_excel('company.xls')
    processed_company = df.loc[df["return"] >=profile[0]]
    final_company = processed_company.loc[processed_company["SR"] <= profile[1]]
    company_list = final_company.iloc[:, 1].tolist()
    return company_list

if __name__ == '__main__':
    print(get_possible_reits([0.296,2.483]))
