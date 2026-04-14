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

# function to plot scores
def plot_scores(scores_df):
    if scores_df is not None:

        st.subheader(
            "For each antibody: percentage of MHC class II–peptide interactions that are relatively strong binders"
        )

        fig = px.strip(
            scores_df,
            y="netMHC_II_pep15_percentile",  # or "score" if standardized
            hover_data=["antibody"],
        )

        fig.update_traces(marker=dict(size=10))
        fig.update_layout(
            yaxis_title="Score",
            xaxis_title="",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)


# Function to create table with scores and antibody names
def scores_table(scores_df):
    # automatically pick the score column (everything except 'antibody')
    score_col = [col for col in scores_df.columns if col != "antibody"][0]

    scores_df = scores_df.sort_values(by=score_col, ascending=False)

    with st.expander("Show detailed results table"):
        st.dataframe(scores_df)

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

    # Show selection
    if st.session_state.protein_type == "VHH":
        st.write("Make predictions for your VHHs with netMHCpan: link\n" \
        "Use default settings and the 27 human allele panel")
        netMHC_II_pan = st.file_uploader("Upload netMHC II pan output file here", type=["csv"])
        seqname_netMHC_II_pan = st.file_uploader("Upload the sequence table here", type=["csv"])
        
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
        # Call function to plot scores
        plot_scores(st.session_state["scores_df"])
        # Add table with scores and antibody names
        scores_table(st.session_state["scores_df"])
    

        
        
if __name__ == "__main__":
    main()

