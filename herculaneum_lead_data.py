
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st

csv_files = {
    '1992': 'annual_29_099_0005_1992.csv',
    '2024': 'annual_29_099_0013_2024.csv',
    '2021': 'annual_29_099_0013_2021.csv',
    '1996': 'annual_29_099_0015_1996.csv',
    '2017': 'annual_29_099_0005_2017.csv',
    '2018': 'annual_29_099_0005_2018.csv',
    '2019': 'annual_29_099_0005_2019.csv',
    '2005': 'annual_29_099_0009_2005.csv',
    '2010': 'annual_29_099_0009_2010.csv',
    '2020': 'annual_29_099_0013_2020.csv',
    '1990': 'annual_29_099_0005_1990.csv',
    '2025': 'annual_29_099_0005_2025.csv',
    '1996': 'annual_29_099_0015_1996.csv',
    '1997': 'annual_29_099_0015_1997.csv',
    '1998': 'annual_29_099_0015_1998.csv',
    '1999': 'annual_29_099_0015_1999.csv',
    '2000':'annual_29_099_0015_2000.csv',
    '2001': 'annual_29_099_0015_2001.csv',
    '2006': 'annual_29_099_0015_2006.csv',
    '2008': 'annual_29_099_0015_2008.csv',
    '2009': 'annual_29_099_0015_2009.csv',
    '2022': 'annual_29_099_0020_2022.csv',
    '2011': 'annual_29_099_9002_2011.csv',
    '2012': 'annual_29_099_9004_2012.csv'
}

def get_max_values(df):
    max_value = df['First Maximum Value'].iloc[0]
    print('Largest Value: ', max_value)

    second_max_value = df['Second Maximum Value'].iloc[0]
    print('Second Largest Value: ', second_max_value)

    third_max_value = df['Third Maximum Value'].iloc[0]
    print('Third Maximum Value: ', third_max_value)

    fourth_max_value = df['Fourth Maximum Value'].iloc[0]
    print('Fourth Maximum Value: ', fourth_max_value)

    return max_value, second_max_value, third_max_value, fourth_max_value

def get_max_dates(df):
    first_date = pd.to_datetime(df['First Maximum DateTime'].iloc[0]).date()
    second_date = pd.to_datetime(df['Second Maximum DateTime'].iloc[0]).date()
    third_date = pd.to_datetime(df['Third Maximum DateTime'].iloc[0]).date()
    fourth_date = pd.to_datetime(df['Fourth Maximum DateTime'].iloc[0]).date()

    return first_date, second_date, third_date, fourth_date

def calculate_average(df):
    cols = [
        'First Maximum Value',
        'Second Maximum Value',
        'Third Maximum Value',
        'Fourth Maximum Value']
    average = round(df.loc[0, cols].mean(), 2)
    return average

# This function displays colors
def color_lead_value(value):
    if value > 0.15:
        color = 'red'
    else:
        color = 'green'

    return f"<span style='color: {color};'>{value} µg/m3</span>"

# This function displays the values to the user.
def display_values(max_value,
                   second_max_value,
                   third_max_value,
                   fourth_max_value,
                   average,
                   first_date,
                   second_date,
                   third_date,
                   fourth_date):
   # st.write('Largest Value: ', max_value, 'µg/m3 |', ' Date: ', first_date)
    st.markdown(
        f"Largest Value: {color_lead_value(max_value)} | Date: {first_date}",
        unsafe_allow_html=True
    )
    st.markdown(
        f"Second Largest Value: {color_lead_value(second_max_value)} | Date: {second_date}",
        unsafe_allow_html=True
    )
    st.markdown(
        f"Third Largest Value: {color_lead_value(third_max_value)} | Date: {third_date}",
        unsafe_allow_html=True
    )
    st.markdown(
        f"Fourth Largest Value: {color_lead_value(fourth_max_value)} | Date: {fourth_date}",
        unsafe_allow_html=True
    )
    st.markdown(
        f"Average of Max Values: {color_lead_value(average)}",
        unsafe_allow_html=True
    )

def create_graph():
    years = []
    averages = []

    for year, csv_file in csv_files.items():
        try:
            df = pd.read_csv(csv_file)
            average = calculate_average(df)

            years.append(int(year))
            averages.append(average)
        except FileNotFoundError:
            pass
    graph_data = pd.DataFrame({
        'Year': years,
        'Average': averages
    })

    graph_data = graph_data.sort_values('Year')
    fig, ax = plt.subplots()

    ax.plot(
        graph_data['Year'],
        graph_data['Average'],
        color='red',
        marker='o',
        linestyle='solid'
    )

    ax.set_title('Average Max Lead Values by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Lead Value µg/m3')

    st.pyplot(fig)

def tabs():
    tab1, tab2, tab3, tab4 = st.tabs(['About', 'Graphs', 'Sources', 'Photos'])
    
    with tab1:
        st.header("What is this Website?")
        st.write("My name is Olivia Harris, and I grew up in a little" \
        " town called Herculaneum, Missouri. Herculaneum is known for its decades" \
        " long battle with lead contamination. In Herculaneum, there are" \
        " air monitors, most of which are still active, that read" \
        " levels of lead in the air. This website takes that data" \
        " directly from the EPA's website, and translates it into " \
        "something easier to understand. I hope to show those living " \
        "in Herculaneum that the lead problem of the past " \
        "may still be an issue of the present.")

    with tab2:
        st.header('Average Max Lead Values by Year')
        create_graph()

    with tab3:
        st.header('Sources')
        st.write('- https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5&extent=-146.2334,13.1913,-46.3896,56.5319\n',
                 '- https://archive.cdc.gov/www_atsdr_cdc_gov/csem/leadtoxicity/safety_standards.html\n'
                 '- https://dnr.mo.gov/waste-recycling/sites-regulated-facilities/interest/doe-run-herculaneum-smelter\n'
                 '- https://www.stlpr.org/show/st-louis-on-the-air/2022-01-21/herculaneums-environmental-cleanup-offers-lessons-for-today\n')
    
    with tab4:
        st.image(
            ['IMG_5222.jpg', 'IMG_1870.JPG', 'IMG_5380.jpg'],
            caption=['A sign: 2017', 'An active air monitor: 2024', 'The smokestack'],
            width=250
        )

def get_input():
    st.title('Lead Data (Herculaneum, Missouri)')

    select_year = st.selectbox('Select a year: ', ['1990', '1991', '1992', '1993', '1994',
    '1995', '1996', '1997', '1998', '1999', '2000', '2001',
    '2002', '2003', '2004', '2005', '2006', '2007',
    '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',
    '2016', '2017', '2018', '2019', '2020', '2021', '2022',
    '2023', '2024', '2025', '2026'])


    if select_year in csv_files:
        df = pd.read_csv(csv_files[select_year])
        
        max_value, second_max_value, third_max_value, fourth_max_value = get_max_values(df)
        first_date, second_date, third_date, fourth_date = get_max_dates(df)
        average = calculate_average(df)
        display_values(
            max_value,
            second_max_value,
            third_max_value,
            fourth_max_value,
            average,
            first_date,
            second_date,
            third_date,
            fourth_date)

        #create_graph(
            #max_value,
            #second_max_value,
            #third_max_value,
            #fourth_max_value)
    else:
        st.write('Data not available')

    st.write("For reference, the EPA National Ambient Air Quality Standards (NAAQS) " \
    "set the limit of lead in the air at 0.15𝜇𝑔/𝑚. Anything above 0.15𝜇𝑔/𝑚 is cause" \
    " for concern.")


get_input()
tabs()
