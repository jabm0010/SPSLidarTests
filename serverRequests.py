import requests
import json
import utils
from pprint import pprint
from requests_toolbelt import MultipartEncoder

"""
Class that defines the methods for making petitions to the server
"""
quiet = True
server = "http://localhost:8080/";

session = requests.Session()
session.auth = ("user", "user")

"""
Get all workspaces
"""


def getWorkspace():
    endpoint = server + "spslidar/workspaces"
    r = session.get(endpoint)
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
    r = session.get(endpoint)
    showResults(r)


"""
Post new workspace
"""


def postWorkspace(workspace, show = True):
    endpoint = server + "spslidar/workspaces"
    r = session.post(endpoint, json=workspace)
    if show:
        showResults(r)
    return r


"""
Get all datasets from a workspace
"""


def getDatasetsFromWorkspace(workspaceName, coordinatesReqParam):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets"
    r = session.get(endpoint, params = coordinatesReqParam)
    return r


"""
Gets a single dataset identified by its workspace and its own name
"""


def getDatasetByName(workspaceName, datasetName):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName
    r = session.get(endpoint)
    showResults(r)
    return r


"""
Posts new dataset
"""


def postDataset(workspaceName, dataset):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets"
    r = session.post(endpoint, json=dataset)
    showResults(r)


"""
Get datablock
"""


def getDatablock(workspaceName, datasetName, id, coordinatesReqParam=None):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName + "/datablocks/" + id
    if coordinatesReqParam is None:
        r = session.get(endpoint)
    else:
        r = session.get(endpoint, params=coordinatesReqParam)

    return r.text


"""
Get datablock file
"""


def getDatablockFile(workspaceName, datasetName, id, coordinatesReqParam, version = None, write=False):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName + "/datablocks/" + id + "/data"
    if version != None:
        coordinatesReqParam["version"] = version
    r = session.get(endpoint, params=coordinatesReqParam)
    if write:
        utils.writeFile(r, workspaceName, datasetName, id)  # Write downloaded files if wanted

    return r


def getCompleteDataset(workspaceName, datasetName):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName + "/data"
    r = session.get(endpoint)
    utils.writeFile(r, workspaceName, datasetName, "0")


"""
Assign dataset 
"""


def putData(workspaceName, datasetName, dataset):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName + "/data"
    mp_encoder = MultipartEncoder(fields=dataset)
    print(mp_encoder.content_type)
    r = session.put(endpoint, data=mp_encoder, headers={"Content-Type": mp_encoder.content_type})
    showResults(r)
    return r


"""
Datablock window query
"""
def getDatablocksByWindowQuery(workspaceName, datasetName, coordinatesReqParam):
    endpoint = server + "spslidar/workspaces/"+workspaceName+"/datasets/"+datasetName+"/datablocks"
    r = session.get(endpoint, params=coordinatesReqParam)
    return r


"""
File window query
"""
def getFilesByWindowQuery(workspaceName, datasetName, coordinatesReqParam):
    endpoint = server + "spslidar/workspaces/"+workspaceName+"/datasets/"+datasetName+"/datablocks/data"
    r = session.get(endpoint, params=coordinatesReqParam)
    utils.writeFile(r, workspaceName, datasetName, "0")
    return r


"""
Edit file
"""
def editData(workspaceName, datasetName, id, coordinatesReqParam, file):
    endpoint = server + "spslidar/workspaces/" + workspaceName + "/datasets/" + datasetName +  "/datablocks/" + id + "/data"
    mp_encoder = MultipartEncoder(fields=file)
    r = session.patch(endpoint, data=mp_encoder, headers={"Content-Type": mp_encoder.content_type},params=coordinatesReqParam)
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
    endpoint = server + "spslidar/database"
    r = session.delete(endpoint)

    showResults(r)


"""
Get octree size
"""


def getOctreeSize(workspace, dataset):
    endpoint = server + "spslidar/workspaces/" + workspace + "/datasets/" + dataset + "/size"
    r = session.get(endpoint)
    return r.text


"""
Get max depth
"""


def getOctreeMaxDepth(workspace, dataset):
    endpoint = server + "spslidar/workspaces/" + workspace + "/datasets/" + dataset + "/depth"
    r = session.get(endpoint)
    return r.text


"""
Modify max depth defined for octrees
"""


def modifyMaxDepthOctree(size):
    endpoint = server + "spslidar/octree/" + str(size)


"""
Get database size
"""


def getDatabaseSize():
    endpoint = server + "spslidar/database"
    r = session.get(endpoint)
    return r.text
