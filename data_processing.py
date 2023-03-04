import pandas as pd 
# pandas를 통해 가공되지 않은 raw data로부터 원하는 형태(Frame)의 데이터를 추출할 수 있다.
# pandas로 또 무엇이 가능할까?


# <Daily>
df = pd.read_csv("data/daily_report.csv") 

# Daily Total
totals_df = df[["Confirmed","Deaths","Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={"index":"condition"})

# Daily by Country
countries_df = df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = countries_df.groupby("Country_Region").sum().sort_values(by="Confirmed", ascending=False).reset_index()

# <Cumulative>
# Enter a country name to get data for that country, 
# or don't enter a country name to get global data.
def make_final_df(country=None):
    def make_df(condition, country=None):
        df = pd.read_csv(f"data/{condition}_global.csv")
        if(country):
            df = df.loc[df["Country/Region"] == country]
        df = (
            df.drop(columns=["Province/State","Country/Region","Lat","Long"])
            .sum()
            .reset_index(name=f"{condition}")
        );
        df = df.rename(columns={"index":"date"}) # rename과 drop은 새로운 Obj를 반환한다.
        return df

    conditions = ["confirmed","deaths","recovered"]
    final_df = None
    for condition in conditions:
        condition_df=make_df(condition, country)
        if(final_df is None):
            final_df = condition_df
        else:
        #a.merge(b): a에 b를 횡으로 이어붙인다.
            final_df = final_df.merge(condition_df)
    return final_df

# <Dropdown Options>
dropdown_options = countries_df
dropdown_options = dropdown_options.sort_values("Country_Region")
dropdown_options = dropdown_options["Country_Region"].reset_index()