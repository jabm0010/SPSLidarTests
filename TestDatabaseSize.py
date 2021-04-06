import serverRequests as sreq
import time
import utils
import os
import json
import itertools
from pymongo import MongoClient

sreq.quiet = True

######Configuration############
# Datasets to test
dataset2011Training = "C:\\Datasets\\Drive\\Pamplona\\Training Areas\\LiDAR_2011"
dataset2017Training = "C:\\Datasets\\Drive\\Pamplona\\Training Areas\\LiDAR_2017"
dataset2017500MillPoints = "C:\\Datasets\\Drive\\Pamplona\\Combined5"
dataset20171000MillPoints = "C:\\Datasets\\Drive\\Pamplona\\Combined10"
dataset20173000MillPoints = "C:\\Datasets\\Drive\\Pamplona\\LiDAR_2017"
dataset20173000MillPoints = "C:\\Datasets\\Drive\\Pamplona\\CombinedAll"

datasets = []
#datasets.append(dataset2011Training)
#datasets.append(dataset2017Training)
datasets.append(dataset20171000MillPoints)
datasets.append(dataset2017500MillPoints)
# datasets.append(dataset20173000MillPoints)

# Datablocks max size to use
testsMaxDatablockSizes = []
#testsMaxDatablockSizes.append(5000000)
#testsMaxDatablockSizes.append(2500000)
#testsMaxDatablockSizes.append(1000000)
#testsMaxDatablockSizes.append(500000)
#testsMaxDatablockSizes.append(100000)
#testsMaxDatablockSizes.append(50000)
testsMaxDatablockSizes.append(10000)

# MaxOctreeSizes
testsMaxOctreeSizes = []
testsMaxOctreeSizes.append(8)
# testsMaxOctreeSizes.append(16)

parameters = list(itertools.product(datasets, testsMaxDatablockSizes, testsMaxOctreeSizes))
######################################

global f
workspaceName = "Navarra"
modelName = "City of Pamplona"


def createProcess(datasetToPut, datablockSize, octreeSize):
    # Reset DB, insert workspace and model
    sreq.resetDatabase()
    time.sleep(20)
    global f

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
    sreq.postModel(workspaceName, model)
    sreq.modifyMaxDepthOctree(octreeSize)

    files = utils.loadDirectory(datasetToPut)
    start = time.time()
    sreq.putDatasetToModel(workspaceName, modelName, files)
    end = time.time()

    write = "Dataset: " + datasetToPut + "\n" + \
            "Max depth: " + str(octreeSize) + "\n" + \
            "Datablock max size: " + str(datablockSize) + "\n" + \
            " time: " + str((end - start)) + "\n"
    f.write(write)
    print(write)




#### Main loop ####
for parameter in parameters:

    #global f
    f = open(str(parameter[0]) + str(parameter[1]) + str(parameter[2]) + ".txt", "a")
    f.write("TEST")

    createProcess(parameter[0], parameter[1], parameter[2])
    time.sleep(60)

    client = MongoClient("localhost")
    db = client.spslidar
    call = db.command("dbstats")

    #Stats to obtain
    database = call['db']
    datasize = call['dataSize'] / (1024 *1024)
    storageSize = call['storageSize'] / (1024*1024)
    objects = call['objects']
    collections = call['collections']
    avgObjSize = call['avgObjSize'] / (1024*1024)

    strDatabase = 'Database:', str(database)
    strObjects = 'Objects:', str(objects)
    strCollections = 'Collections:', str(collections)
    strDataSize = 'Data size:', str(datasize) + 'Mb'
    strStorageSize = 'Storage size', str(storageSize) + 'Mb'
    strAvgObjSize = 'Avg Obj Size:', str(avgObjSize)+ 'Mb'

    #Collection stats
    ###Chunks
    callCollChunks = db.command("collStats", "fs.chunks")
    chunksDataSize = callCollChunks["size"]  / (1024*1024)
    chunksStorageSize = callCollChunks["storageSize"] / (1024*1024)
    chunksTotalIndexSize = callCollChunks["totalIndexSize"] / (1024*1024)

    schunksDataSize = "Chunks Data Size: ", str(chunksDataSize)
    schunksStorageSize =  "Chunks Storage Size: ", str(chunksStorageSize)
    schunksTotalIndexSize = "Chunks Indexes Size; ", str(chunksTotalIndexSize)
    ###Files
    callCollFiles = db.command("collStats", "fs.files")
    filesDataSize = callCollFiles["size"] / (1024*1024)
    filesStorageSize = callCollFiles["storageSize"]  / (1024*1024)
    filesTotalIndexSize = callCollFiles["totalIndexSize"] / (1024*1024)

    sfilesDataSize = "Files Data Size: ", str(filesDataSize)
    sfilesStorageSize =  "Files Storage Size: ", str(filesStorageSize)
    sfilesTotalIndexSize = "Files Indexes Size; ", str(filesTotalIndexSize)
    ###Datablocks
    callCollDblocks = db.command("collStats", "Navarra_datablocks")
    dblockDataSize = callCollDblocks["size"] / (1024*1024)
    dblockStorageSize = callCollDblocks["storageSize"] / (1024*1024)
    dblockTotalIndexSize = callCollDblocks["totalIndexSize"] / (1024*1024)

    sdblockDataSize = "Dblock Data Size: ", str(dblockDataSize)
    sdblockStorageSize = "Dblock Storage Size: ", str(dblockStorageSize)
    sdblockTotalIndexSize = "Dblock Indexes Size; ", str(dblockTotalIndexSize)

    print('\n')
    print(strDatabase)
    f.write(str(strDatabase))
    print(strObjects)
    f.write(str(strObjects))
    print(strCollections)
    f.write(str(strCollections))
    print(strDataSize)
    f.write(str(strDataSize))
    print(strStorageSize)
    f.write(str(strStorageSize))
    print(strAvgObjSize)
    f.write(str(strAvgObjSize))
    print('\n')


    #print('\n')
    #print(strDatabase)
    #print(strObjects)
    #print(strCollections)
    #print(strDataSize)
    #print(strStorageSize)
    #print(strAvgObjSize)
    #print("Chunks Collection")
    #print(schunksDataSize)
    #print(schunksStorageSize)
    #print(schunksTotalIndexSize)
    #print("Files Collection")
    #print(sfilesDataSize)
    #print(sfilesStorageSize)
    #print(sfilesTotalIndexSize)
    #print("Datablocks Collection")
    #print(sdblockDataSize)
    #print(sdblockStorageSize)
    #print(sdblockTotalIndexSize)
    #print('\n')

    print("----------------")









