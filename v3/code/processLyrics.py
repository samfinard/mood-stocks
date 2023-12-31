"""
1. convert to lower case
2. remove non punctuation, non character entries
3. scan for regex patterns ('contributors', 'get tickets')

Basically try to get as close to what we already have as possible
* should record compression ratio of file size
"""

import pandas as pd
import re
from tqdm import tqdm
tqdm.pandas()

def lower_remove_nonChar(df):
    df['lyrics'] = df['lyrics'].str.lower()

    def keep(char): # only keep lowercase letters, spaces, apostrophes, hyphens
                    # period comma, exclamation mark, semicolon, or colon
        o = ord(char)
        return (o == 32 or o == 33 or o == 40 
                or (44 <= o and o <= 46) 
                or o == 58 or o == 59 or o == 63 
                or (96 <= o and o <= 122)
                or (66 <= o and o <= 91))
   
    def remove_fluff(text):
        if pd.isna(text):  # Check if the text is NaN
            return ""  # Return an empty string for NaN values
        return ''.join(char if keep(char) else ' ' for char in text)
    
    df['lyrics'] = df['lyrics'].progress_apply(remove_fluff)
    
    def replace_multiple_spaces(text):
        return re.sub(' +', ' ', text)
    
    df['lyrics'] = df['lyrics'].apply(replace_multiple_spaces)
    return df

def main():
    df = pd.read_csv("/Users/samfinard/src/1PA/Final-Project/v3/output.csv", low_memory=False)
    df = lower_remove_nonChar(df)



    df.to_csv("output2.csv", index=False)
    # df = pd.read_csv("/Users/samfinard/src/1PA/Final-Project/v3/output.csv", low_memory=False)
    
if __name__ == "__main__":
    main()
