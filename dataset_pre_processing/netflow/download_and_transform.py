import wget

from dataset_pre_processing.netflow.transform import main as transform_main


def main():
    wget.download(
        "https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-45/capture20110815.pcap.netflow.labeled"
    )
    print()

    transform_main(args=[
        "capture20110815.pcap.netflow.labeled",
        "features.npy",
        "labels.npy",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
