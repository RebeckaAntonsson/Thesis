#  Compute the scores for different tools

""" This script is used to compute the scores for different tools. The scores are computed for the following tools:
- netMHC1
- netMHC II
- waltz
The scores are computed for the following features:
- netMHC1 percentile score
- netMHC1 imunogenicity score
- netMHC1 pre process score
- netMHC II percentile score
- netMHC II imunogenicity score
- netMHC II -np cleavage probability



"""

# netMHC1 percentile score
df = (
    df.assign(immunogenic=df['netmhcpan_el percentile'] <= 1) # flags rows where percentile is below 1
          .groupby('sequence name')['immunogenic'] # calculates mean of immunogenic for each antibody, gives the fraction
          .mean()
          .mul(100) # multiplies by 100 to get percentage
          .reset_index(name='netMHC1_pep9_percentile')
    )


# netMHC1 imunogenicity score

# netMHC1 pre process score

# netMHC II percentile score

# netMHC II imunogenicity score

# netMHC II -np cleavage probability

# netMHC II -np cleavage probability percentile rank

# waltz score




# netMHC1_EL_pep9 percentile score

# Immunogenentic is defened as scored <= 1%
# Here I calculate the percantage of peptide-HLA allele combinations (rows) that have a percentile score below 1. 


# netMHC1_EL_pep9 Immunogenicity score 

# Immunogenentic is defened as scored larger than 0
# Here I calculate the percantage of peptide-HLA allele combinations (rows) that have a immunogenicity score above 0. 
netMHC1_pep9_immunogenicity_score = (
    netMHC1_defaultSettings.assign(immunogenic=netMHC1_defaultSettings['immunogenicity score'] > 0) # flags rows where percentile is above 0
          .groupby('sequence name')['immunogenic'] # calculates mean of immunogenic for each antibody, gives the fraction
          .mean()
          .mul(100) # multiplies by 100 to get percentage
          .reset_index(name='netMHC1_pep9_immunogenicity_score')
    )

# netMHC1_EL_pep9 Preprocessing score

# Immunogenentic is not defined
# Here I simply calculate the mean score for each antibody. 
netMCH1_pep9_preProcess = netMHC1_defaultSettings.groupby('sequence name')['processing total score'].mean().reset_index().rename(columns={'processing total score': 'netMHC1_pep9_preProcess'})



# netMHC_II_EL_pep15

# Percentile score

# Immunogenentic is defened as scored <= 10%
# Here I calculate the percantage of peptide-HLA allele combinations (rows) that have a percentile score below 10. 
netMHC_II_pep15_percentile = (
    netMHC_II_defaultSettings.assign(immunogenic=netMHC_II_defaultSettings['netmhciipan_el percentile'] <= 10) # flags rows where percentile is below 10
          .groupby('sequence name')['immunogenic'] # calculates mean of immunogenic for each antibody, gives the fraction
          .mean()
          .mul(100) # multiplies by 100 to get percentage
          .reset_index(name='netMHC_II_pep15_percentile')
    )

# Immunogenicity score

# Immunogenentic is not defined
# Here I simply calculate the mean score for each antibody. 
netMHC_II_pep15_immunogenicity_score = netMHC_II_defaultSettings.groupby('sequence name')['immunogenicity score'].mean().reset_index().rename(columns={'immunogenicity score':'netMHC_II_pep15_immunogenicity_score'})

# Pre-proocessing score
# MHC class 2 has 2 preprocessing scores of interest: mhcii-np cleavage probability score and mhcii-np cleavage probability percentile rank

# mhcii-np cleavage probability

# remove the rows with the cleavage probability score of '-' before calculating the mean
netMHC_II_EL_pep15 = netMHC_II_defaultSettings[netMHC_II_defaultSettings['mhcii-np cleavage probability score'] != '-']
# make the column with the cleavage probability score into a numeric column
netMHC_II_EL_pep15['mhcii-np cleavage probability score'] = pd.to_numeric(netMHC_II_EL_pep15['mhcii-np cleavage probability score'])
# Compute score
# Immunogenentic is not defined
# Here I simply calculate the mean score for each antibody. 
netMHC_II_pep15_preProcess_cleavProb = netMHC_II_EL_pep15.groupby('sequence name')['mhcii-np cleavage probability score'].mean().reset_index().rename(columns={'mhcii-np cleavage probability score': 'netMHC_II_pep15_preProcess_cleavProb'})

# mhcii-np cleavage probability percentile rank

# remove the rows with the cleavage probability percentile rank of '-' before calculating the mean
netMHC_II_EL_pep15 = netMHC_II_EL_pep15[netMHC_II_EL_pep15['mhcii-np cleavage probability percentile rank'] != '-']
# make the column with the cleavage probability percentile rank into a numeric column
netMHC_II_EL_pep15['mhcii-np cleavage probability percentile rank'] = pd.to_numeric(netMHC_II_EL_pep15['mhcii-np cleavage probability percentile rank'])
# compute score
# Immunogenentic is not defined
# Here I simply calculate the mean score for each antibody. 
netMHC_II_pep15_preProcess_cleavProbPercentile = netMHC_II_EL_pep15.groupby('sequence name')['mhcii-np cleavage probability percentile rank'].mean().reset_index().rename(columns={'mhcii-np cleavage probability percentile rank': 'netMHC_II_pep15_preProcess_cleavProbPercentile'})

