## ----------------------------------------------------------------------------##
## Import Dependencies ##
import pandas as pd

from preprocessing import Preprocessing
preprocessor = Preprocessing()

from search import Search
seeker = Search()
## ----------------------------------------------------------------------------##

def create_data():
    """
    Builds upon earlier work delivering usable information on retrieving ejection fraction
    measurements and methods for HHC to develop a usable training set for experimentation
    with machine learning based alternatives to hard-coded search patterns.
    """
    ## ----------------------------------------------------------------------------##
    ## ----------------------------------------------------------------------------##
    ## Import Data ##

    # Import Data
    df = pd.read_csv("full_sample.csv")
    df = df.rename(columns={"Unnamed: 0" : "ID"}) # *
    df = df[["ID", "NOTE_TEXT"]] # *

    """ *
    Footnotes: 
        Line 18: Rename 'Unnamed' Column to 'ID' 
        Line 19: There's a third 'Unnamed' Column that only has 'nans', 
            so let's only keep 'ID' and 'NOTE_TEXT' from the original df
    """
    ## ----------------------------------------------------------------------------##
    ## ----------------------------------------------------------------------------##
    ## Clean Text ## 
    df['NOTE_CLEAN'] = df['NOTE_TEXT'].apply(preprocessor.clean)
    df['NOTE_CLEAN'] = df['NOTE_CLEAN'].apply(preprocessor.standard_spacing)

    ## Create add a 'Mentions' column of short phrases matching patterns ##
    df['MENTIONS'] = df['NOTE_CLEAN'].apply(preprocessor.find_pattern)
    df = df[["ID", "NOTE_CLEAN", "MENTIONS"]] # *
    # df = df.loc[df.astype(str)['MENTIONS'] != '[]'] # * 

    """ *
    Footnotes: 
        Line 35: We drop 'NOTE_TEXT' from the df
        Line 36: Uncomment to remove all records that didn't have a hit with 
            the search patterns
    """

    ## Clean Mentions Columns ## 
    # Clean the Mentions Columns by removing square brackets and single quotation marks 
    df['MENTIONS'] = df['MENTIONS'].apply(preprocessor.second_clean)
    ## ----------------------------------------------------------------------------##
    ## ----------------------------------------------------------------------------##
    ## Search Ejection Fraction Measurement Methods ## 
    df['METHOD'] = df['MENTIONS'].apply(seeker.find_method)

    ## ----------------------------------------------------------------------------##
    ## ----------------------------------------------------------------------------##
    ## Search for Measurement Values ## 
    df = seeker.attach_measurement(df)

    decision = input("Do you wish to save to csv? Y/N: ")
    if decision == "Y":
        df.to_csv("dataset.csv")
    else: 
        print("Operation complete.  Quitting.")

    return df

#create_data()