import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json

def load_data(report_file):
    try:
        with open(report_file, 'r') as file:
            report = json.load(file)
        results = []
        for result in report['results']:
            results.append({
                'id': result['id'],
                'host': result['host'],
                'port': result['port'],
                'severity': result['severity'],
                'name': result['name'],
                'description': result['description'],
                'solution': result['solution']
            })
        return pd.DataFrame(results)
    except json.JSONDecodeError:
        st.error("Error loading JSON file. Please check the file format.")
        return pd.DataFrame()

# Load the report
report_file = 'openvas_report.json'
data = load_data(report_file)

if data.empty:
    st.warning("No data available. Please run the scan first.")
else:
    # Streamlit app
    st.title("OpenVAS Security Audit Report")

    # Display summary statistics
    st.header("Summary")
    st.write("Total vulnerabilities detected:", len(data))
    st.write("Critical:", data[data['severity'] == 'Critical'].shape[0])
    st.write("High:", data[data['severity'] == 'High'].shape[0])
    st.write("Medium:", data[data['severity'] == 'Medium'].shape[0])
    st.write("Low:", data[data['severity'] == 'Low'].shape[0])

    # Display vulnerabilities by severity
    st.header("Vulnerabilities by Severity")
    fig, ax = plt.subplots()
    sns.countplot(data=data, x='severity', ax=ax)
    st.pyplot(fig)

    # Display vulnerabilities by host
    st.header("Vulnerabilities by Host")
    fig = px.histogram(data, x='host', color='severity', title='Vulnerabilities by Host')
    st.plotly_chart(fig)

    # Display detailed report
    st.header("Detailed Report")
    st.dataframe(data)

    # Allow user to download the report
    st.download_button(
        label="Download Report",
        data=data.to_csv().encode('utf-8'),
        file_name='openvas_report.csv',
        mime='text/csv',
    )
