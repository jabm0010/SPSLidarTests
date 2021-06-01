import serverRequests as sreq
import time
import utils

datasetToPut = "C:\\Datasets\\Drive\\Pamplona\\Combined5"
datablockSize = 1000000
workspaceName = "Navarra"
datasetName = "City of Pamplona"


def uploadDataset():
    # Reset DB, insert workspace and dataset
    sreq.resetDatabase()
    time.sleep(20)
    global f

    workspace = {
        "name": workspaceName,
        "description": "Workspace with the datasets of Navarra",
        "cellSize": 10000
    }

    dataset = {
        "name": datasetName,
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
        "dataBlockSize": datablockSize,
        "dataBlockFormat": ".laz"
    }

    sreq.postWorkspace(workspace)
    sreq.postDataset(workspaceName, dataset)

    files = utils.loadDirectory(datasetToPut)
    start = time.time()
    sreq.putData(workspaceName, datasetName, files)
    end = time.time()

    write = "Dataset: " + datasetName + "\n" + \
            "Datablock max size: " + str(datablockSize) + "\n" + \
            " time: " + str((end - start)) + "\n"
    print(write)


uploadDataset()
