from purchase_analyzer import *

def main():
    in_path = "purchases.txt"
    out_path = "report.txt"

    purchases = read_purchases(in_path)
    errors = count_errors(in_path)
    write_report(purchases, errors, out_path)

if __name__ == "__main__":
    main()