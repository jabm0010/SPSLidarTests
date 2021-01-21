import pylas
import serverRequests as sreq
import time
import utils
import shutil
import os
import json
from datetime import datetime

sreq.quiet = True

pathToFile = "D:\Drive\Pamplona\Training Areas\combined_2017.laz"
datasetLocation = "D:\Drive\Pamplona\Training Areas\LiDAR_2017"
folderToDelete = "C:\\Users\\UJA\\Desktop\\lazfiles\\Navarra_City of Pamplona"
workspaceName = "Navarra"
modelName = "City of Pamplona"

# MaxDatablockSizePercentages
percentages = [0.1, 1, 5, 10]
testsMaxDatablockSizes = []

with pylas.open(pathToFile) as fh:
    numberOfPoints = fh.header.point_count
    print("Points from header: ", fh.header.point_count)
    for p in percentages:
        testsMaxDatablockSizes.append(round(numberOfPoints * p / 100))

testsMaxDatablockSizes.append(50000)
testsMaxDatablockSizes.append(100000)
testsMaxDatablockSizes.append(500000)
testsMaxDatablockSizes.append(1000000)

f = open("results2.txt", "a")
f.write("TESTS\n")
f.write("------------------------------------------------\n")
f.write("Results for the dataset " + datasetLocation + "\n")


def createProcess(datablockSize):
    sreq.resetDatabase()

    workspace = {
        "name": workspaceName,
        "description": "Workspace with the models of Navarra",
        "gridSize": 10000
    }

    model = {
        "name": modelName,
        "description": "Model of the city of Pamplona 01",
        "date": "2017-01-01T12:00:00Z",
        "bbox": {
            "southWestBottom": {
                "easting": "610000",
                "northing": "4740000",
                "zone": "30N"
            },
            "northEastTop": {
                "easting": "614000",
                "northing": "4744000",
                "zone": "30N"
            }
        },
        "dataBlockSize": datablockSize,
        "dataBlockFormat": ".laz"
    }

    sreq.postWorkspace(workspace)
    sreq.postModel(workspaceName,model)

    if(os.path.isdir(folderToDelete)):
        f.write("Had to delete folder from client...\n")
        shutil.rmtree(folderToDelete, ignore_errors=True)

    files = utils.loadDirectory(datasetLocation)

    start = time.time()
    sreq.putDatasetToModel(workspaceName, modelName, files)
    end = time.time()

    f.write("Datablock max size: "+ str(datablockSize)+" time: "+ str((end - start))+"\n")


def retrieveProcess():
    workspaceName = "Navarra"
    modelName = "City of Pamplona"

    rootDBs = sreq.getDatablock(workspaceName, modelName, str(0), None)
    jsondata = json.loads(rootDBs)
    rootDB = jsondata[0]

    swBottom = rootDB["grid"]["southWestBottom"]
    neTop = rootDB["grid"]["northEastTop"]
    swBottomStr = swBottom["zone"] + str(swBottom["easting"]) + str(swBottom["northing"])
    neTopStr = neTop["zone"] + str(neTop["easting"]) + str(neTop["northing"])

    dict = {
        "southWest": swBottomStr,
        "northEast": neTopStr
    }

    start = time.time()
    sreq.getDatablockFile(workspaceName, modelName, str(0), dict)
    end = time.time()

    timeCounter = end - start

    filesCounter = 1
    childrenAvailable = True
    tmpNode = rootDB
    nextId = rootDB["children"][0]

    while (childrenAvailable):

        # Download file
        start = time.time()
        sreq.getDatablockFile(workspaceName, modelName, str(nextId), dict)
        end = time.time()
        timeCounter += (end - start)
        filesCounter += 1

        # Search next child
        text = sreq.getDatablock(workspaceName, modelName, str(nextId), dict)
        tmpNode = json.loads(text)
        children = tmpNode[0]["children"]
        if len(children) != 0:
            nextId = tmpNode[0]["children"][0]
        else:
            childrenAvailable = False

    averageTime = timeCounter / filesCounter

    f.write("Number of files: " + str(filesCounter)+"\n")
    f.write("Total time in download: " + str(timeCounter)+"\n")
    f.write("Average time of file: "+ str(averageTime)+"\n")

    files_in_directory = os.listdir()
    filtered_files = [file for file in files_in_directory if file.endswith(".laz")]
    for file in filtered_files:
        os.remove(file)


for maxDatablockSize in testsMaxDatablockSizes:
    createProcess(maxDatablockSize)
    retrieveProcess()
    f.write("------------------------------------------------\n")

