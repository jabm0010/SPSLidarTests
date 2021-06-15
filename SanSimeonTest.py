import DatasetInsertion
import DataRecovery
import utils

SanSimeonDataset = "D:\Datasets\OpenTopography\San Simeon"
datablockSize = 100000

workspace = {
    "name": "California",
    "description": "Workspace with the datasets of California",
    "cellSize": 10000
}

dataset = {
    "name": "San Simeon",
    "description": "Dataset of San Simeon",
    "dateOfAcquisition": "2017-01-01T12:00:00Z",
    "boundingBox": {
        "southWestBottom": {
            "easting": "606000",
            "northing": "4736000",
            "zone": "30N"
        },
        "northEastTop": {
            "easting": "614000",
            "northing": " 4744000",
            "zone": "30N"
        }
    },
    "dataBlockSize": datablockSize,
    "dataBlockFormat": ".laz"
}

datasets = []
datasets.append("San Simeon")
testsMaxDatablockSizes = []
testsMaxDatablockSizes.append(datablockSize)

results = {}
for _dataset in datasets:
    results[dataset] = {}
    results[dataset]["Fields"] = ("Insertion time", "Files downloaded",
                                       "Total Download Request Time", "Total Points Downloaded",
                                       "Avg Time of File Download", "Avg Time of Point Download")
    for testsMaxDatablockSize in testsMaxDatablockSizes:
        results[dataset][testsMaxDatablockSize] = tuple()



results = DatasetInsertion.createProcess(workspace,dataset,SanSimeonDataset, datablockSize, 16, results)
results = DataRecovery.retrieveProcess(workspace["name"], dataset["name"], SanSimeonDataset, datablockSize, results)

utils.createSheet("Mongo", results)

