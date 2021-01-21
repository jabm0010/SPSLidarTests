import serverRequests as sreq
import utils
import time

sreq.resetDatabase()

#Create workspace
workspaceName = "Navarra"

workspace = {
    "name": workspaceName,
    "description": "Workspace with the models of Navarra",
    "gridSize":10000
}

sreq.postWorkspace(workspace)

#Create model 2017

modelName = "City of Pamplona"

model = {
    "name": modelName,
    "description": "Model of the city of Pamplona 01",
    "date": "2017-01-01T12:00:00Z",
    "bbox": {
        "southWestBottom": {
            "easting":"610000",
            "northing": "4740000",
            "zone": "30N"
        },
        "northEastTop": {
            "easting": "614000",
            "northing": "4744000",
            "zone": "30N"
        }
    },
    "dataBlockSize": 1000000,
    "dataBlockFormat": ".laz"
}

sreq.postModel(workspaceName, model)

#Put data

dataset_location = "D:\Drive\Pamplona\Training Areas\LiDAR_2017"
start = time.time()
files = utils.loadDirectory(dataset_location)
sreq.putDatasetToModel(workspaceName, modelName, files)
end = time.time()

print("Time spent in dataset processing dataset 2017: ", end-start)














