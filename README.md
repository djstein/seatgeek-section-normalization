# seatgeek_section_normalization
Normalize the naming conventions applied by the various sellers and map the listings to a *canonical* list of sections and rows that we know to actually exist in the stadium.

[GITHUB LINK](https://github.com/djstein/seatgeek_section_normalization/blob/master/README.md)

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

- Now that the section name and row name have been cleaned, begin looking for the corresponding key in the dictionary. The key examined is then lowered and split. Immediately if the section name and key are the same, set the keyv (key value variable) to the key and break. Begin then exaimining if the split_key has parts contained in the split_section. When all values are found regardless of order the function sets the keyv to key and breaks. [Lines 99-109]
- Finally once the keyv is set, it attempts to find the cleaned row name within the section name dictionary. Once found, the section_id, row_id, and valid are set. [Lines 112-118]

# !!! Improvements !!!
I personally found that under a time constraint it was going to be too extremely complicated to determine any and all edge cases supplied in the dodgertest.csv. Many section names supplied included integers with characters attached and these characters had no 100% corrolation with a particular section name in the mainfest_data. While I was able to achieve splitting of the integers and string, it would create an extremely high time complexity within Lines 75-89 by checking against the split key's data value's first characters.
I believe there are two solutions to ensure this time complexity is lowered for abbreviations and exceptionally long section names:
1. When users enter data to the csv, that data is not included unless it is first cleaned via strong form validation or API validation
2. Applying the use of a learning database. Coupling each venue's csv file manifest with a second csv or xml set that has a compiled list of common terms and their abbrevations. When an abbreviation is found that is not understood by the normalize it can either check in these steps:
  - Determining if each letter (in a int/string pair) is found within the section name key (will return many results however)
  - Stop progress on the in use thread and prompt the user to input what an abbreviation means, rechecking keys and adding the value to the database
  - OR while higher complexity, when a new abbreviation is found it can attempt to check each section name's dictionary to determine if the row name is found. This may return multiple results, but the key name can then be weighted with the abbreviation after the fact and added to the database as an association.
  
This solution would be needed to determine values such as the dodgertest.csv line 998, 44FD,E,212,4,True. The 44FD is supposed to correspond to 212,Field Box 44,4,E (line 3203 on dogerstadium_sections.csv). However FD does not relate to the Field Box string extremely efficiently, it could also fit to Right Field Pavilion, etc.
