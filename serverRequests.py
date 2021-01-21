import requests
import json
import utils
from pprint import pprint


"""
Class that defines the methods for making petitions to the server
"""
quiet = False
server = "http://localhost:8080/";

"""
Get all workspaces
"""


def getWorkspace():
    endpoint = server + "spslidar/workspace"
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
    endpoint = server + "spslidar/workspace/" + workspaceName
    r = requests.get(endpoint)
    showResults(r)


"""
Post new workspace
"""


def postWorkspace(workspace):
    endpoint = server + "spslidar/workspace"
    r = requests.post(endpoint, json=workspace)
    showResults(r)


"""
Get all models from a workspace
"""


def getModelsFromWorkspace(workspaceName, coordinatesReqParam):
    endpoint = server + "spslidar/workspace/" + workspaceName + "/model"
    r = requests.get(endpoint)
    showResults(r)


"""
Gets a single model identified by its workspace and its own name
"""


def getModelByName(workspaceName, modelName):
    endpoint = server + "spslidar/workspace/" + workspaceName + "/model/" + modelName
    r = requests.get(endpoint)
    showResults(r)


"""
Posts new model
"""


def postModel(workspaceName, model):
    endpoint = server + "spslidar/workspace/" + workspaceName + "/model"
    r = requests.post(endpoint, json=model)
    showResults(r)


"""
Get datablock
"""


def getDatablock(workspaceName, modelName, id, coordinatesReqParam=None):
    endpoint = server + "spslidar/workspace/" + workspaceName + "/model/" + modelName + "/data/" + id
    if coordinatesReqParam is None:
        r = requests.get(endpoint)
    else:
        r = requests.get(endpoint, coordinatesReqParam)

    #showResults(r)
    return r.text



"""
Get datablock file
"""


def getDatablockFile(workspaceName, modelName, id, coordinatesReqParam):
    endpoint = server + "spslidar/workspace/" + workspaceName + "/model/" + modelName + "/data/" + id + "/laz"
    r = requests.get(endpoint, params=coordinatesReqParam)
    utils.writeFile(r, workspaceName, modelName, id)


"""
Assign dataset to model
"""


def putDatasetToModel(workspaceName, modelName, dataset):
    endpoint = server + "spslidar/workspace/" + workspaceName + "/model/" + modelName + "/data/laz"
    r = requests.put(endpoint, files=dataset)
    showResults(r)


"""
Generic method to print the statuds code recevied and the content
"""


def showResults(request):
    print("Status code returned: ", str(request.status_code))
    if quiet == False:
        try:
            jsondata = json.loads(request.text)
            pprint(jsondata)
        except:
            print(request.text)




"""
Reset database
"""

def resetDatabase():

    endpoint = server+"spslidar/database"
    r = requests.delete(endpoint)

    showResults(r)

"""
Get octree size
"""
def getOctreeSize(workspace, model):
    endpoint = server + "spslidar/workspace/"+workspace+"/model/"+model+"/size"
    r = requests.get(endpoint)
    return r.text

"""
Get max depth
"""
def getOctreeMaxDepth(workspace, model):
    endpoint = server + "spslidar/workspace/"+workspace+"/model/"+model+"/depth"
    r = requests.get(endpoint)
    return r.text


"""
Modify max depth defined for octrees
"""
def modifyMaxDepthOctree(size):
    endpoint = server + "spslidar/octree/"+size
    r = requests.put(endpoint)




