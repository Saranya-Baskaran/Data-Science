import os
import fileinput
import string

def main():
    directory = "../Data/training_data"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            f = fileinput.input(os.path.join(directory, filename))

            for line in f:
                # Stripping new line
                line = line.rstrip('\n')
                line = line.replace(string.punctuation.replace('#', ''), '')
                line = " ".join(line.split())
                if "London#L" in line:
                    print(filename)

if __name__ == "__main__":
    main()
