import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def turn_to_num(x):
    if x == "Less than 1 year":
        return 0.5
    if x == "More than 50 years":
        return 50
    return float(x)

def shorten_categories(categories,
                       cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        country = categories.keys()[i]
        num_entries = categories.values[i]
        
        if num_entries >= cutoff:
            categorical_map[country] = country
        else:
            categorical_map[country] = "Other"
    return categorical_map


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post Grad"
    return "Less than a Bachelor’s"

def load_data():
    df = pd.read_csv("./stack-overflow-developer-survey-2020/survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop(["Employment"], axis=1)
    
    categorical_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(categorical_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Other"]
    df["Salary"] >= 10000
    
    df["YearsCodePro"] = df["YearsCodePro"].apply(turn_to_num)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    
    return df


df = load_data()

def show_explore_page():
    st.title("Explore SWE Salaries around the world")
    
    st.write("""### Stack Overflow Developer Survey 2020""")
    
    
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
    