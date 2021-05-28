import serverRequests as sreq
import utils
import json

workspaceName = "Costa Rica"
datasetName = "Model 1"
datablocksIDs = [0, 1, 2, 3, 4]
cell = 1
areaOfInterest = {
    "south": 1159000,
    "west": 821950,
    "north": 1159506,
    "east": 829700,
}


def defineCellBox():
    dataset = sreq.getDatasetByName(workspaceName, datasetName)
    jsonzedDataset = json.loads(dataset.text)
    southWestComponent = jsonzedDataset["rootDatablocks"][cell]["southWestBottom"]
    northEastComponent = jsonzedDataset["rootDatablocks"][cell]["northEastTop"]
    swBottomStr = southWestComponent["zone"] + str(southWestComponent["easting"]) + str(southWestComponent["northing"])
    neTopStr = northEastComponent["zone"] + str(northEastComponent["easting"]) + str(northEastComponent["northing"])

    endPointCoordinateParameters = {
        "sw_coord": swBottomStr,
        "ne_coord": neTopStr
    }
    return endPointCoordinateParameters


###Main method to invoke for download of IDs
def recoverByDatablockIDs():
    endPointCoordinateParamters = defineCellBox()
    for id in datablocksIDs:
        writeFile(workspaceName, datasetName, id, endPointCoordinateParamters)


###Main method to invoke for download by area
def recoverByArea():
    endPointCoordinateParamters = defineCellBox()
    datablock = sreq.getDatablock(workspaceName, datasetName, str(0), endPointCoordinateParamters)
    jsonizedDatablock = json.loads(datablock)
    if overlaps(jsonizedDatablock[0]["bbox"]):
        writeFile(workspaceName, datasetName, 0, endPointCoordinateParamters)
        recursiveRecovery(jsonizedDatablock[0]["children"])


###Recursive method to download children that fit the region defined for download of files
def recursiveRecovery(children):
    endPointCoordinateParamters = defineCellBox()

    for id in children:
        datablock = sreq.getDatablock(workspaceName, datasetName, str(id), endPointCoordinateParamters)
        jsonziedDatablock = json.loads(datablock)
        if overlaps(jsonziedDatablock[0]["bbox"]):
            writeFile(workspaceName, datasetName, id, endPointCoordinateParamters)
            recursiveRecovery(jsonziedDatablock[0]["children"])


def writeFile(workspaceName, datasetName, id, endPointCoordinateParameters):
    file = sreq.getDatablockFile(workspaceName, datasetName, str(id), endPointCoordinateParameters)
    if file.status_code == 404:
        print("Node ", str(id), "does not exist")
    else:
        utils.writeFile(file, workspaceName, datasetName, str(id))


def overlaps(bbox):
    x1 = bbox["southWestBottom"]["easting"] > areaOfInterest["east"]
    x2 = areaOfInterest["west"] > bbox["northEastTop"]["easting"]
    x3 = bbox["southWestBottom"]["northing"] > areaOfInterest["north"]
    x4 = areaOfInterest["south"] > bbox["northEastTop"]["northing"]

    noOverlap = x1 or x2 or x3 or x4
    return not noOverlap


recoverByArea()