import csv
import wget
import xlrd

from dataset_pre_processing.default_credit_card.transform import main as transform_main


def main():
    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls",
        "default_credit_card_clients.xls"
    )
    print()

    workbook = xlrd.open_workbook("default_credit_card_clients.xls")
    sheet = workbook.sheet_by_name("Data")
    with open("default_credit_card_clients.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        for row_number in range(1, sheet.nrows):  # ignore first redundant row
            writer.writerow(sheet.row_values(row_number))

    transform_main(args=[
        "default_credit_card_clients.csv",
        "features.npy",
        "labels.npy",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
