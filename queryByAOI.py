import serverRequests as sreq
import utils
import json

workspaceName = "Navarra"
datasetName = "City of Pamplona"
areaOfInterest = {
    "south": 4742000,
    "west": 608000,
    "north": 4749000,
    "east": 612000,
}

def overlaps(bbox):
    x1 = bbox["southWestBottom"]["easting"] > areaOfInterest["east"]
    x2 = areaOfInterest["west"] > bbox["northEastTop"]["easting"]
    x3 = bbox["southWestBottom"]["northing"] > areaOfInterest["north"]
    x4 = areaOfInterest["south"] > bbox["northEastTop"]["northing"]

    noOverlap = x1 or x2 or x3 or x4
    return not noOverlap



def defineCellBox(gridCell):
    southWestComponent = gridCell["southWestBottom"]
    northEastComponent = gridCell["northEastTop"]
    swBottomStr = southWestComponent["zone"] + str(southWestComponent["easting"]) + str(southWestComponent["northing"])
    neTopStr = northEastComponent["zone"] + str(northEastComponent["easting"]) + str(northEastComponent["northing"])

    endPointCoordinateParameters = {
        "sw_coord": swBottomStr,
        "ne_coord": neTopStr
    }
    return endPointCoordinateParameters

def findOverlappingGridCells():
    dataset = sreq.getDatasetByName(workspaceName, datasetName)
    jsonzedDataset = json.loads(dataset.text)
    listOfOverlappingGridCells = []
    for gridCell in jsonzedDataset["rootDatablocks"]:
        if overlaps(gridCell):
            listOfOverlappingGridCells.append(defineCellBox(gridCell))

    return listOfOverlappingGridCells

overlappingGridCells = findOverlappingGridCells()



###Main method to invoke for download by area
def recoverByArea():
    overlappingGridCells = findOverlappingGridCells()
    for cell in overlappingGridCells:
        datablock = sreq.getDatablock(workspaceName, datasetName, str(0), cell)
        jsonizedDatablock = json.loads(datablock)
        if overlaps(jsonizedDatablock[0]["bbox"]):
            writeFile(workspaceName, datasetName, 0, cell)
            recursiveRecovery(jsonizedDatablock[0]["children"], cell)


###Recursive method to download children that fit the region defined for download of files
def recursiveRecovery(children, cell):

    for id in children:
        datablock = sreq.getDatablock(workspaceName, datasetName, str(id), cell)
        jsonziedDatablock = json.loads(datablock)
        if overlaps(jsonziedDatablock[0]["bbox"]):
            writeFile(workspaceName, datasetName, id, cell)
            recursiveRecovery(jsonziedDatablock[0]["children"],cell)


def writeFile(workspaceName, datasetName, id, endPointCoordinateParameters):
    file = sreq.getDatablockFile(workspaceName, datasetName, str(id), endPointCoordinateParameters)
    if file.status_code == 404:
        print("Node ", str(id), "does not exist")
    else:
        utils.writeFile(file, workspaceName, datasetName, str(id))



recoverByArea()