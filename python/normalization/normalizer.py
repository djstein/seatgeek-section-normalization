import csv
import re

class Normalizer(object):

    def __init__(self):
        self.manifest_data = {}
        

    def read_manifest(self, manifest):
        """reads a manifest file

        manifest should be a CSV containing the following columns
            * section_id
            * section_name
            * row_id
            * row_name

        Arguments:
            manifest {[str]} -- /path/to/manifest
        """
        with open(manifest, 'rU') as f:
            reader = csv.DictReader(f)
            for line in reader:
                if 'section_id' and 'row_id' in line:
                    section_id = line['section_id']
                    row_id = line['row_id']
                    section_name = line['section_name']
                    row_name = line['row_name']
                    if section_name in self.manifest_data:
                        self.manifest_data[section_name].update( { 'section_id': section_id, row_name:row_id } )
                    else:
                        self.manifest_data.update( { section_name: { 'section_id': section_id, row_name:row_id } } )


    def normalize(self, section, row):
        """normalize a single (section, row) input

        Given a (Section, Row) input, returns (section_id, row_id, valid)
        where
            section_id = int or None
            row_id = int or None
            valid = True or False

        Arguments:
            section {[type]} -- [description]
            row {[type]} -- [description]
        """
        
        # check if section is in self.manifest_data before looking for partial of section
        # make a regular expression that splits apart all portions of the section, then test for keys and if all parts of a key are found return that key
        
        # instantiate values for scope
        section_id = None
        keyv = None
        row_id = None
        valid = False

        # compile regular expressions
        reg_int = re.compile('\d+')
        reg_string = re.compile('([a-zA-Z]+)')
        reg_int_string = re.compile("([0-9]+)([a-zA-Z]+)")

        # lower the section text
        section = section.lower()
        split_section = section.split(" ")

        # Check if row only has one instance of integers
        int_search = reg_int.findall(row)
        if int_search and len(int_search) > 1:
            return(section_id, row_id, valid)
        elif int_search:
            row = str(int(int_search[0]))

        # for each value in the split section
        # determine if it is only an integer
        for i, val in enumerate(split_section):
            if reg_int_string.match(val):
                reg_search = reg_int_string.match(val)
            elif reg_int.match(val):
                reg_search = reg_int.match(val)
            elif reg_string.match(val):
                reg_search = reg_string.match(val)

            if reg_search and len(split_section) == 1 and reg_search.groups():
                split_section = str(reg_search.groups())
                break
            elif reg_search and len(split_section) == 1 and reg_search.group():
                split_section = [str(reg_search.group())]
            elif reg_search:
                split_section[i] = str(reg_search.group())

        print split_section
        print row

        for key in self.manifest_data.keys():
            lower_key = key.lower()
            split_key = lower_key.split(" ")

            if len(split_section) == 1 and (split_section[0] == split_key[0]):
                keyv = key
                break

            key_counter = 0
            section_counter = 0
            for part in split_key:
                if part in split_section:
                    key_counter += 1
                    section_counter += 1
                if (key_counter == len(split_key)) or (section_counter == len(split_section)):
                    keyv = key
                    break
            if keyv is not None:
                break

        # if there is a found key value, set section_id, row_id, and valid to corresponding values
        if keyv is not None:
            if row in self.manifest_data[str(keyv)]:
                section_id = int(self.manifest_data[str(keyv)]["section_id"])
                row_id = int(self.manifest_data[str(keyv)][str(row)])
                valid = True

        print "{} {} {}".format(section_id, row_id, valid)
        print "------------------------------------"
        return(section_id, row_id, valid)

#  time python genericgrader.py --manifest manifests/citifield_sections.csv --input samples/metstest.csv --lang python --verbose
# time python genericgrader.py --manifest manifests/dodgerstadium_sections.csv --input samples/dodgertest.csv --lang python --verbose
# ./python/normalize --manifest ../manifests/dodgerstadium_sections.csv --input ../samples/dodgertest.csv
# ./python/normalize --manifest ../manifests/citifield_sections.csv --input ../samples/metstest.csv