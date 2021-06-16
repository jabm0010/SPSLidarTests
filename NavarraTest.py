import serverRequests as sreq
import time
import utils
import itertools
import DatasetInsertion
import DataRecovery

sreq.quiet = True

######Configuration############
####Change paths of datasets and parameters####
# Datasets to test
dataset2011Training = "D:\\Datasets\\Drive\\Pamplona\\Training Areas\\LiDAR_2011"
dataset2017Training = "D:\\Datasets\\Drive\\Pamplona\\Training Areas\\LiDAR_2017"
dataset2017500MillPoints = "D:\\Datasets\\Drive\\Pamplona\\Combined5"
dataset20171000MillPoints = "D:\\Datasets\\Drive\\Pamplona\\Combined10"

datasets = []
#datasets.append(dataset2011Training)
#datasets.append(dataset2017Training)
#datasets.append(dataset2017500MillPoints)
datasets.append(dataset20171000MillPoints)


# Datablocks max size to use
testsMaxDatablockSizes = []
#testsMaxDatablockSizes.append(5000000)
#testsMaxDatablockSizes.append(2500000)
#testsMaxDatablockSizes.append(1000000)
#testsMaxDatablockSizes.append(500000)
testsMaxDatablockSizes.append(100000)
#testsMaxDatablockSizes.append(50000)
#testsMaxDatablockSizes.append(10000)

# MaxOctreeSizes
testsMaxOctreeSizes = []
testsMaxOctreeSizes.append(8)

parameters = list(itertools.product(datasets, testsMaxDatablockSizes, testsMaxOctreeSizes))

results = {}
for dataset in datasets:
    results[dataset] = {}
    results[dataset]["Fields"] = ("Insertion time", "Files downloaded",
                                       "Total Download Request Time", "Total Points Downloaded",
                                       "Avg Time of File Download", "Avg Time of Point Download")
    for testsMaxDatablockSize in testsMaxDatablockSizes:
        results[dataset][testsMaxDatablockSize] = tuple()

for parameter in parameters:

    workspace = {
        "name": "NavarraIII",
        "description": "Workspace with the datasets of Navarra",
        "cellSize": 10000
    }

    dataset = {
        "name": "PamplonaIII",
        "description": "Dataset of the city of Pamplona 01",
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
        "dataBlockSize": parameter[1],
        "dataBlockFormat": ".laz"
    }

    #results = DatasetInsertion.createProcess(workspace, dataset, parameter[0], parameter[1], parameter[2], results)
    #time.sleep(120)
    results = DataRecovery.retrieveProcess(workspace["name"], dataset["name"], parameter[0],parameter[1],results)

utils.createSheet("Navarra_Mongo_SSD", results)