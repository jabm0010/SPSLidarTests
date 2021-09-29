import serverRequests as sreq

workspaceName = "Costa Rica"
datasetName = "Model 1"
filePath = "C:\\Users\\UJA\\PycharmProjects\\SPSLidarTests\\SPSLidarTests\\files\\Costa Rica\\Model 1\\modified.laz"

coordinates = {
    "sw_coord":"16N8200001150000",
    "ne_coord": "16N8300001160000"
}

#sreq.getDatablockFile(workspaceName, datasetName,"0", coordinates, True)
fileToUpload = [("file", (filePath, open(filePath, 'rb'), 'application/octet-stream'))]

#sreq.editData(workspaceName, datasetName, "0", coordinates, fileToUpload)

sreq.getDatablockFile(workspaceName, datasetName, "0", coordinates, version="2", write = True)