"""
Script to filter out the 10 best selling antibodies from a file with 222 antibodies.\
The scripts loads the file, filters out the 10 best selling antibodies and then outputs them as a csv file.
"""
import pandas as pd
from pathlib import Path

# Get the location of this script
BASE_DIR = Path(__file__).resolve().parent

# Load file with the antibody prediction data
antibodies_prediction_scores = pd.read_csv(BASE_DIR/"../Immonogenecity_tool_testing/model_selection/biophi_dataSet/all_predictors_222AB(biophidata).csv")

# Get the 10 best selling antibodies and save in a new df
antibodies_10_best_selling = antibodies_prediction_scores[antibodies_prediction_scores['antibody'].isin([
    'pembrolizumab', 'adalimumab','dupilumab', 'ustekinumab', 'daratumumab','nivolumab', 
    'risankizumab', 'ocrelizumab', 'vedolizumab', 'secukinumab'])].copy()

# Get the 10 antibodies with highest observed anti-drug antibodies
antibodies_high_ADA = antibodies_prediction_scores[antibodies_prediction_scores['antibody'].isin([
    'disitamab', 'moxetumomab', 'abagovomab', 'tarperprumig_alxn1820', 'naptumomab',
    'edrecolomab', 'racotumomab', 'zolimomab', '3f8', 'moab_81c6'])
    ]

# Filter out only the predictors that are used in the therapeutic profiler
antibodies_10_best_selling_therapeutic_profiler_cols = antibodies_10_best_selling[['antibody','ADA_percentage','netMHC_II_pep15_percentile', 'netMHC1_pep9_immunogenicity_score', 'biophi_KabKabStrict_score', ]]
antibodies_high_ADA_therapeutic_profiler_cols = antibodies_high_ADA[['antibody','ADA_percentage','netMHC_II_pep15_percentile', 'netMHC1_pep9_immunogenicity_score', 'biophi_KabKabStrict_score', ]]

# Save the 10 best selling antibodies as csv
antibodies_10_best_selling_therapeutic_profiler_cols.to_csv(BASE_DIR/"10_best_sellingAB_cols_for_profiler.csv", index=False)
antibodies_high_ADA_therapeutic_profiler_cols.to_csv(BASE_DIR/"antibodies_high_ADA_therapeutic_profiler_cols.csv", index=False)