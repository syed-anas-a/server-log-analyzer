# slice_logs.py

def slice_log_file(input_file, output_file, n=1000):
    """Copy the first n lines from input_file to output_file."""
    with open(input_file, "r") as infile, \
         open(output_file, "w") as outfile:

        for count, line in enumerate(infile, start=1):
            outfile.write(line)
            if count == n:
                break

if __name__ == "__main__":
    slice_log_file("access.log", "access_trimmed.log", 1000)
    print("✅ First 1000 lines saved to access_trimmed.log")