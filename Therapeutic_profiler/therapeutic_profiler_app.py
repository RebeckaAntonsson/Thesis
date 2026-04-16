""""
therapeutic_profiler_app.py

Description:


User defined functions:
1.

2.

Non-standard modules: pandas, streamlit

Procedure:
    
    Main code

1.

2.


Decisions made:

Cases the code can hadle:

Cases the code cannot handle:

Input:

Output:

Usage: streamlit run therapeutic_profiler_app.py

Version: 1.00
Date: 10-04-2026
Author: Rebecka Antonsson

"""


import streamlit as st
import pandas as pd
import plotly.express as px
import compute_immunogenicity_scores as cis
from pathlib import Path
st.set_page_config(layout="wide")

# function: load netMHCpan EL output data
# if netMHC II pan print "You seem to have loaded the netMHC II pan file here, it should be netMHCpan"

# function: load netMHC II pan EL output data
# if netMHCpan print "You seem to have loaded the netMHCpan file here, it should be netMHC II pan"

# function: load waltz output data

# function: load biophi output data
# Only if the input is VHHs

# function: compute scores
# (maybe as separate script ?? bc really long?)


# function to compute scores netMHC II pan
def clean_df_send_to_compute_scores_netMHC_II_pan(netMHC_II_pan, seqname_netMHC_II_pan):
    
    # make both files into pandas df
    netMHC_II_pan_df = pd.read_csv(netMHC_II_pan)
    seqname_netMHC_II_pan_df = pd.read_csv(seqname_netMHC_II_pan)

    # map back sequence name
    netMHC_II_pan_df = netMHC_II_pan_df.merge(seqname_netMHC_II_pan_df[['seq #', 'sequence name']], how='left')
    # rename antibody name column and drop seq # column
    netMHC_II_pan_df = netMHC_II_pan_df.rename(columns={'sequence name': 'antibody'}).drop(columns=['seq #'])
    
    # Call function to compute scores
    scores_df = cis.compute_netMHC_II_percentile(netMHC_II_pan_df) 
    
    return scores_df

# load reference data, the 10 best selling antibodies and their predictive scores
@st.cache_data
def load_reference_data():
    from pathlib import Path
    import pandas as pd

    BASE_DIR = Path(__file__).resolve().parent
    return pd.read_csv(BASE_DIR /"10_best_sellingAB_cols_for_profiler.csv")



# function to plot scores
def plot_scores(combined_df):
    if combined_df is not None:

        st.subheader(
            "For each antibody: percentage of MHC class II–peptide interactions that are relatively strong binders"
        )

        fig = px.strip(
            combined_df,
            y="netMHC_II_pep15_percentile",
            color="source",
            hover_data=["antibody"],
            color_discrete_map={
                "User": "hotpink",
                "Reference": "blue"
            }
        )

        fig.update_traces(marker=dict(size=10))
        fig.update_layout(
            yaxis_title="% of the minibinder with immunogenetic scores",
            xaxis_title="",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)


# Function to create table with scores and antibody names
def scores_table(combined_df):
    score_col = "netMHC_II_pep15_percentile"

    combined_df = combined_df.sort_values(by=score_col, ascending=False)

    def highlight_rows(row):
        if row["source"] == "Reference":
            return ["background-color: rgba(0, 0, 255, 0.1)"] * len(row)  # light blue
        else:
            return ["background-color: rgba(255, 105, 180, 0.1)"] * len(row)  # light pink

    styled_df = combined_df.style.apply(highlight_rows, axis=1)

    with st.expander("Show detailed results table"):
        st.dataframe(styled_df, use_container_width=True)



# function to produce result plot and table for VHHs
def result_VHH(biophi_output_df):
    # read it as pandas df 
    biophi_output_df = pd.read_excel(biophi_output_df)
    #select usefull columns
    biophi_output_df = biophi_output_df[["Antibody", "OASis Identity"]].copy()
    
    # Create result plot

    st.subheader(
        "Biophi score plot"
        )

    fig = px.strip(
        biophi_output_df,
        y="OASis Identity",  # or "score" if standardized
        hover_data=["Antibody"],
    )

    # Add horizontail line at OASis Identity 0.8
    fig.add_hline(
        y=0.8,
        line_dash="dash",
        line_color="red"
    )

    # add information if you hover the dots
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(
        yaxis_title="OASis Identity score",
        xaxis_title="",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # Make result table

    # Sort (lowest first)
    biophi_output_df = biophi_output_df.sort_values(by="OASis Identity", ascending=True)

    # Styling function
    def highlight_rows(row):
        if row["OASis Identity"] > 0.8:
            return ["background-color: rgba(255, 0, 0, 0.1)"] * len(row)  # light red
        else:
            return ["background-color: rgba(0, 255, 0, 0.1)"] * len(row)  # light green

    styled_df = biophi_output_df.style.apply(highlight_rows, axis=1)

    # Show in expandable section
    with st.expander("Show OASis Identity table"):
        st.dataframe(styled_df, use_container_width=True)

# Main script

def main():
    # Start program and print the first information, using streamlit

    st.header("Therapeutic Profiler")
     
    # Ask user to input if they want to predict VHH or minibinders
    st.write("Are you predicting VHHs or minibinders today?")

    # Initialize state
    if "protein_type" not in st.session_state:
        st.session_state.protein_type = None

    # Buttons
    col1, col2 = st.columns(2)

    # initialize protein type

    with col1:
        if st.button("VHH"):
            st.session_state.protein_type = "VHH"

    with col2:
        if st.button("Minibinder"):
            st.session_state.protein_type = "Minibinder"

    if st.session_state.protein_type == "VHH":
        st.write("Make predictions for your VHH's with BioPhi here: https://biophi.dichlab.org/humanization/humanness/")
        st.write("Select OASis prevalence threshold: strict (≥90% subjects)")
        st.write("Run prediction and the export the entire table")
        biophi = st.file_uploader("Upload your biophi output file here", type=["xlsx"])
        
        # Button to confirm input
        if st.button("Done"):
            if biophi is None or biophi is None:
                st.warning("Please upload both files before continuing.")
            else:
                st.success("Files uploaded. Running analysis...")

            st.session_state["scores_df"] = biophi

    if "scores_df" in st.session_state:
        # Function that checks biophi file
        # like, correct settings, no NaNs, correct file type, etc etc. 
        # call function that plots results for biophi
        result_VHH(st.session_state["scores_df"])

            

    # Show selection
    if st.session_state.protein_type == "Minibinder":

        col1, col2, col3 = st.columns(3, gap = "large")

        with col1:
            st.subheader("netMHC II pan Percentile")
            # call function for this result
            st.write("Make predictions for your Minibinders with netMHC II pan here: https://nextgen-tools.iedb.org/pipeline?tool=tc2")
            st.write("Use default settings and the 27 human allele panel")
            netMHC_II_pan = st.file_uploader("Upload netMHC II pan output file here:", type=["csv"])
            seqname_netMHC_II_pan = st.file_uploader("Upload the sequence table here:", type=["csv"])
            
            # Button to confirm input
            if st.button("Done"):
                if netMHC_II_pan is None or seqname_netMHC_II_pan is None:
                    st.warning("Please upload both files before continuing.")
                else:
                    st.success("Files uploaded. Running analysis...")

                # clean df and compute scores
                netMHC_II_pan_scores_df = clean_df_send_to_compute_scores_netMHC_II_pan(netMHC_II_pan, seqname_netMHC_II_pan)

                st.session_state["scores_df"] = netMHC_II_pan_scores_df


            if "scores_df" in st.session_state:
                # Call function to get the reference data (the 10 best selling antibodies)
                ref_df = load_reference_data()

                scores_df = st.session_state["scores_df"].copy()
                scores_df["source"] = "User"

                ref_df = load_reference_data().copy()
                ref_df["source"] = "Reference"
                combined_df = pd.concat([scores_df, ref_df], ignore_index=True)
                # Call function to plot scores
                plot_scores(combined_df)
                # Add table with scores and antibody names
                scores_table(combined_df)


        with col2:
            st.subheader("netMHCpan Immunogenicity")
            # call function for this result
           

        with col3:
            st.subheader("Waltz aggregation")
            # call function for this result
        
        
if __name__ == "__main__":
    main()

