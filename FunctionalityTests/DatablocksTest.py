import FunctionalityTests.TestUtils as tu
import FunctionalityTests.WorkspaceTests as wtest
import FunctionalityTests.DatasetsTest as dtest
import serverRequests as sreq
import utils

wsName = wtest.workspace["name"]
dsName = dtest.dataset["name"]


def initializeWorkspaceAndDataset():
    sreq.resetDatabase()
    sreq.postWorkspace(wtest.workspace)
    sreq.postDataset(wsName, dtest.dataset)


def insertData():
    initializeWorkspaceAndDataset()
    pathToDataset = "C:\\Users\\UJA\\Desktop\\Pruebas\\Test2"
    files = utils.loadDirectory(pathToDataset)

    res = sreq.putData("ABC", "DEF", files)
    print(res.status_code)
    files = utils.loadDirectory(pathToDataset)

    sreq.putData(wsName, dsName, files)


def windowQueryDatablocks():
    #insertData()
    coordinates = {}
    coordinates["sw_coord"] = '16N8298001150300'
    coordinates["ne_coord"] = '16N8340001170000'
    print("Result window query datablocks")
    result = sreq.getDatablocksByWindowQuery(wsName, dsName, coordinates)

def windowQueryFiles():
    insertData()
    coordinates = {}
    coordinates["sw_coord"] = '16N8298001150300'
    coordinates["ne_coord"] = '16N8340001170000'
    print("Result window query datablocks")
    result = sreq.getFilesByWindowQuery(wsName, dsName, coordinates)



def getCompleteDataset():
    insertData()
    sreq.getCompleteDataset(wsName, dsName)


insertData()