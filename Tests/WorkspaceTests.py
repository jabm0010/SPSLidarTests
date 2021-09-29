import serverRequests as sreq
import copy
import Tests.TestUtils as tu

workspace = {
    "name": "Jaen",
    "description": "Workspace of the province of Jaén",
    "cellSize": 10000
}


def testAddWorkspace():
    sreq.resetDatabase()
    sreq.postWorkspace(workspace)
    print("-------------------------------")
    #409 Duplicate
    sreq.postWorkspace(workspace)
    print("-------------------------------")
    #400 Invalid workspace
    sreq.resetDatabase()
    nullNameWorkspace = copy.deepcopy(workspace)
    nullNameWorkspace["name"] = None
    sreq.postWorkspace(nullNameWorkspace)
    print("-------------------------------")

    #201 Created
    sreq.resetDatabase()
    nullDescriptionWorkspace = copy.deepcopy(workspace)
    nullDescriptionWorkspace["description"] = None
    sreq.postWorkspace(nullDescriptionWorkspace)
    print("-------------------------------")

    #400 Invalid workspace
    sreq.resetDatabase()
    nullCellsizeWorkspace = copy.deepcopy(workspace)
    nullCellsizeWorkspace["cellSize"] = None
    sreq.postWorkspace(nullCellsizeWorkspace)
    print("-------------------------------")

    #400 Invalid workspace
    sreq.resetDatabase()
    lessThanMinCellSizeWorkspace = copy.deepcopy(workspace)
    lessThanMinCellSizeWorkspace["cellSize"] = 50
    sreq.postWorkspace(lessThanMinCellSizeWorkspace)
    print("-------------------------------")

    #400 Invalid workspace
    sreq.resetDatabase()
    moreThanMaxCellSizeWorkspace = copy.deepcopy(workspace)
    moreThanMaxCellSizeWorkspace["cellSize"] = 50000000000000000
    sreq.postWorkspace(moreThanMaxCellSizeWorkspace)
    print("-------------------------------")


    #400 Invalid workspace
    sreq.resetDatabase()
    moreFieldsThanExpected = copy.deepcopy(workspace)
    moreFieldsThanExpected["abc"] = "abc"
    sreq.postWorkspace(moreFieldsThanExpected)
    print("-------------------------------")


def testGetWorkspaces():
    sreq.resetDatabase()
    sreq.getWorkspace()
    print("-------------------------------")

    sreq.postWorkspace(workspace,show=False)
    sreq.getWorkspace()
    print("-------------------------------")

    workspace2 = copy.deepcopy(workspace)
    workspace2["name"] = "Cordoba"
    sreq.postWorkspace(copy.deepcopy(workspace2), show=False)

    sreq.getWorkspace()
    print("-------------------------------")


def testGetWorkspaceByName():
    sreq.resetDatabase()
    sreq.postWorkspace(workspace,show=False)

    sreq.getWorkspaceByName("Cordoba")
    sreq.getWorkspaceByName("Jaen")


#testAddWorkspace()
#testGetWorkspaces()
#testGetWorkspaceByName()
