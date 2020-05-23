import re
import logging

#pattern to extract appropriate names from string
extract_pattern = r'[^\w][Dd](?:.{0,2})[Bb](?:.{0,2})[Aa][^\w]'

#pattern to striping off extract characters from string.
replace_pattern = r'(\s+|_)'

#storing specials characters to variable to reuse later in the code.
special_characters = r' .,/*-|():'

#Compiling and saving resulting regex object in variable for reuse.
prog = re.compile(extract_pattern)

def clean_names(raw_names):
  """
    Takes list of raw names, split legal and DBA names.
    
    Returns
    -------
    list of pairs.
  """

  clean_names = []
  for name in raw_names:
    
    logging.info("spilt legal and DBA names ...")
    splits = prog.split(name)
    
    logging.info("process and cleaning up strings with special characters ...")
    left = re.sub(replace_pattern, ' ', splits[0].strip(special_characters))
    right = re.sub(replace_pattern, ' ', splits[1].strip(special_characters)) if len(splits) > 1 else None
    
    logging.info("storing clean names ...")
    clean_names.append((left, right))
  
  return clean_names