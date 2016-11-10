# seatgeek_section_normalization
Normalize the naming conventions applied by the various sellers and map the listings to a *canonical* list of sections and rows that we know to actually exist in the stadium.

# Explination of Normalizer

## Dictionary: manifest_data
To store the data from a venue's manifest data, a dictionary will be created named <b>manifest_data</b>
The structure of the manifest_data dictionary will be as such:

```
{
  section_name (var): {
  
    'section_id' (str): section_id (var),
    
    row_name (var): row_id (var), 
  }  
}
```
The dictionary will be structured in this way as in the function normalize the section name and row name are supplied. These can be used to find the appropriate key pairs to return section_id and row_id.
Assumptions with this assignment for why a nested dictionary is an acceptable include:
- The largest venue in the world is currently the [Indianapolis Motor Speedway with a capacity of about 257,325] (https://en.wikipedia.org/wiki/List_of_sports_venues_by_capacity). Knowing this, our manifest_data would not exceed 300,000 entries (row_id)
- The sample csv files contained 2385 and 4315 entries, which we assume are medium sized datasets that are typically supplied. If a concert hall is used, there may only be a few hundered (if that).

## Function: __init__(self)
Instantiates a dictionary called <b>manifest_data</b> within a Normalizer object.

## Function: read_manifest(self, manifest)
The function <b>read_manifest</b> begins by creating a new reader of the csv document provided for a venue. This will loop through each line of the document placing it data for <b>section_id, row_id, section_name, and row_name</b> into the <b>self.manifest_data</b> dictionary.
If an entry with the same section_name already exisits, an addition to the section_name dictionary will include a new 'section_id': section_id and row_name: row_id entry.

## Function: normalize(self, section, row)
The normalize function has many parts that run for the section and row supplied to check if a corresponding section_id, row_id can be returned.
- First values used within for loops and if statements are instantiated [Lines 51-54]
- Regular expressions for finding integers, strings, and integers with strings combined are compiled [Lines 57-59]
- The section name supplied is then lowered to ensure consistancy, then split by white space delimiter [Lines 62-63]
- The row supplied it is first checked if it is a range of rows, if so return invalid immediately. If not the row is also scrubbed to ensure it is an interger represented in string format. ie. 02 -> '2' [Line 67-71]
- The section data split_section is then cleaned using the regular expressions and then remaking split_section [Lines 75-89]

  - Check if the value is an integer, a string, or integer with a string with the regular expressions
  - First, check if there is only one value in split_string (typically a integer) and if the regular expression match was split into an integer and string
  - Second, check if there is only one value in split_string and only one value was returned via the regular expression match
  - Third, if the split string is multiple values (typically a name of a section with a number attached) change each value of array to it's scrubbed component

- Now that the section name and row name have been cleaned, begin looking for the corresponding key in the dictionary.
