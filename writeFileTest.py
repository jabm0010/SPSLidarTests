import requests
import utils

server = "http://localhost:8080/";
workspaceName = "Navarra"
modelName = "City of Pamplona"
id = 0

dict = {
    "southWest": "30N6000004730000",
    "northEast": "30N6100004740000"
}


endpoint = server + "spslidar/workspace/" + workspaceName + "/model/" + modelName + "/data/" + str(id) + "/laz"
r = requests.get(endpoint, params=dict)
utils.writeFile(r, workspaceName, modelName, str(id))
