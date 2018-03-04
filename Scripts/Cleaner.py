import os
import re
import string


def main():
    directory = "../Data/testing_data"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            f = os.path.join(directory, filename)
            with open(f, 'r+') as file:
                mod_line = ''
                for line in file:
                    #print(line)
                    line = line.rstrip('\n')
                    line = line.replace(string.punctuation.replace('#', ''), '')

                    line = re.sub(r'\*', '', line)
                    line = re.sub(r'\+', '', line)
                    line = re.sub(r'\$', '', line)
                    line = re.sub(r'\%', '', line)
                    line = re.sub(r',', '', line)
                    line = re.sub(r'\'', '', line) # quotes removed
                    line = re.sub(r'-LRB-', '', line)
                    line = re.sub(r'-RRB-', '', line)

                    # line = re.sub("^\d+\s|\s\d+\s|\s\d+$", '', line) Removes only strings with all digits
                    # The below regex removes even if one of the string has a digit. Decimal point will remain
                    line = re.sub("\d", '', line)
                    mod_line += line
                    mod_line += "\n"

                    #print(line)
                    #print("#"*20)
                file.seek(0)
                file.write(mod_line)


if __name__ == "__main__":
    main()