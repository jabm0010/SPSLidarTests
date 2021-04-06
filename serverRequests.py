import requests
import json
import utils
from pprint import pprint
from requests_toolbelt import MultipartEncoder

"""
Class that defines the methods for making petitions to the server
"""
quiet = False
server = "http://localhost:8080/";

"""
Get all workspaces
"""
def getWorkspace():
    endpoint = server + "spslidar/workspaces"
    r = requests.get(endpoint)
    result = r.text

    lines = result.splitlines()
    for line in lines:
        jsonline = json.loads(line)
        pprint(jsonline)


"""
Get single workspace identified by its name
"""


def getWorkspaceByName(workspaceName):
    endpoint = server + "spslidar/workspaces/" + workspaceName
    r = requests.get(endpoint)
    showResults(r)


"""
Post new workspace
"""


def postWorkspace(workspace):
    endpoint = server + "spslidar/workspaces"
    r = requests.post(endpoint, json=workspace)
    showResults(r)


"""
Get all datasets from a workspace
"""


def getDatasetsFromWorkspace(workspaceName, coordinatesReqParam):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets"
    r = requests.get(endpoint)
    showResults(r)


"""
Gets a single dataset identified by its workspace and its own name
"""


def getDatasetByName(workspaceName, datasetName):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName
    r = requests.get(endpoint)
    showResults(r)


"""
Posts new dataset
"""


def postDataset(workspaceName, dataset):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets"
    r = requests.post(endpoint, json=dataset)
    showResults(r)


"""
Get datablock
"""


def getDatablock(workspaceName, datasetName, id, coordinatesReqParam=None):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName + "/datablocks/" + id
    if coordinatesReqParam is None:
        r = requests.get(endpoint)
    else:
        r = requests.get(endpoint, coordinatesReqParam)

    return r.text


"""
Get datablock file
"""


def getDatablockFile(workspaceName, datasetName, id, coordinatesReqParam):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName + "/datablocks/" + id + "/data"
    r = requests.get(endpoint, params=coordinatesReqParam)
    #utils.writeFile(r, workspaceName, datasetName, id) #Write downloaded files if wanted


"""
Assign dataset to dataset
"""


def putData(workspaceName, datasetName, dataset):
    endpoint = server + "spslidar/workspacesendpoint = server + "spslidar/octree/" + str(size)
    r = requests.put(endpoint)


"""
Get database size
"""

def getDatabaseSize():
    endpoint = server + "spslidar/database"
    r = requests.get(endpoint)
    return r.text
