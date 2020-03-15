import argparse
import csv
import os
import wget
import xlrd

from dataset_pre_processing.uci.default_of_credit_card_clients.transform import main as transform_main


def main():
    options_parser = argparse.ArgumentParser(description="Download the data and transform with default values.")

    options_parser.add_argument("--directory", type=str, help="Output directory.")

    options = options_parser.parse_args()

    directory = options.directory
    if directory is None:
        directory = os.getcwd()

    excel_path = os.path.join(directory, "default of credit card clients.xls")
    csv_path = os.path.join(directory, "default of credit card clients.csv")

    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls",
        excel_path
    )
    print()

    workbook = xlrd.open_workbook(excel_path)
    sheet = workbook.sheet_by_name("Data")
    with open(csv_path, "w") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        for row_number in range(1, sheet.nrows):  # ignore first redundant row
            writer.writerow(sheet.row_values(row_number))

    transform_main(args=[
        csv_path,
        os.path.join(directory, "features.npy"),
        os.path.join(directory, "labels.npy"),
        os.path.join(directory, "metadata.json"),
        "--scaler=" + os.path.join(directory, "scaler.pickle")
    ])


if __name__ == "__main__":
    main()
