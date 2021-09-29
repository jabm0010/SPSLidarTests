import serverRequests as sreq
import FunctionalityTests.WorkspaceTests as wtest
import copy
import FunctionalityTests.TestUtils as tu

southWestBottom = {
    "easting": "829000",
    "northing": "1158000",
    "zone": "16N"
}

northEastTop = {
    "easting": "830000",
    "northing": "1159000",
    "zone": "16N"
}


georefBox = {
    "southWestBottom": southWestBottom,
    "northEastTop": northEastTop
}


dataset = {
    "name":"Torredonjimeno",
    "description": "Dataset of Torredonjimeno",
    "dateOfAcquisition": "2020-11-24T12:10:00Z",
    "boundingBox":georefBox,
    "dataBlockSize": 100000,
    "dataBlockFormat": "LAZ",

}

ws = wtest.workspace["name"]

def initializeWorkspace():
    sreq.resetDatabase()
    sreq.postWorkspace(wtest.workspace, show=False)


def testAddDataset():
    initializeWorkspace()
    sreq.postDataset(ws, dataset)

    initializeWorkspace()
    datasetWithIncorrectDate = copy.deepcopy(dataset)
    datasetWithIncorrectDate["dateOfAcquisition"] = "2020-11-24T13212:00"
    sreq.postDataset(ws, datasetWithIncorrectDate)

    initializeWorkspace()
    datasetWithNullDatablockSize = copy.deepcopy(dataset)
    datasetWithNullDatablockSize["dataBlockSize"] = None
    sreq.postDataset(ws, datasetWithNullDatablockSize)

def testGetDatasetByName():
    initializeWorkspace()
    sreq.postDataset(ws, dataset)
    getDataset200 = sreq.getDatasetByName(ws, dataset["name"]).status_code
    tu.evaluateTest(getDataset200, 200)

    getDataset404 = sreq.getDatasetByName(ws, "Error").status_code
    tu.evaluateTest(getDataset404, 404)


def testGetDatasetBySpatialWindow():
    initializeWorkspace()
    sreq.postDataset(ws, dataset)

    res1 = sreq.getDatasetsFromWorkspace(ws, None)
    print("RES1")
    tu.printResult(res1)

    coordinates1 = {}
    coordinates1["sw_coord"] = "16N8295001158500"
    coordinates1["ne_coord"] = "16N8297501158700"
    res2InnerQueryWindow = sreq.getDatasetsFromWorkspace(ws, coordinates1)
    print("RES2")
    print(res2InnerQueryWindow.status_code)
    tu.printResult(res2InnerQueryWindow)

    coordinates2 = {}
    coordinates2["sw_coord"] = "31N8295001158500"
    coordinates2["ne_coord"] = "31N8297501158600"
    res3NotFound1UTMZoneOut = sreq.getDatasetsFromWorkspace(ws, coordinates2)
    print("RES3")
    tu.printResult(res3NotFound1UTMZoneOut)

    coordinates3 = {}
    coordinates3["sw_coord"] = "16N8295001158500"
    coordinates3["ne_coord"] = "17N8297501158600"
    res4DifferentUTMZones = sreq.getDatasetsFromWorkspace(ws, coordinates3)
    print("RES4")
    tu.printResult(res4DifferentUTMZones)


    coordinates4 = {}
    coordinates4["sw_coord"] = "16N8150001158500"
    coordinates4["ne_coord"] = "16N8175001158600"
    res5NotOverlappingWindow = sreq.getDatasetsFromWorkspace(ws, coordinates4)
    print("RES5")
    tu.printResult(res5NotOverlappingWindow)

    coordinates5 = {}
    coordinates5["sw_coord"] = "16N8210001158500"
    coordinates5["ne_coord"] = "16N8225001158600"
    res6NotOverlappingWindow = sreq.getDatasetsFromWorkspace(ws, coordinates5)
    print("RES6")
    tu.printResult(res6NotOverlappingWindow)

    coordinatesWithDates1 = {}
    coordinatesWithDates1["from_date"] = '2020-08-24T12:10'
    coordinatesWithDates1["to_date"] = '2022-11-24T12:10'
    res7DatasetInDateRange = sreq.getDatasetsFromWorkspace(ws, coordinatesWithDates1)
    print("RES7")
    tu.printResult(res7DatasetInDateRange)


    coordinatesWithDates2 = {}
    coordinatesWithDates2["from_date"] = '2020-08-24T12:10'
    coordinatesWithDates2["to_date"] = '2020-10-24T12:10'
    res8DatasetOutOfRange = sreq.getDatasetsFromWorkspace(ws, coordinatesWithDates2)
    print("RES8")
    tu.printResult(res8DatasetOutOfRange)

    coordinatesWithDates3 = {}
    coordinatesWithDates3["from_date"] = '2020-08-24T12:10'
    coordinatesWithDates3["to_date"] = '2020-10-24T12:10'
    coordinatesWithDates3["sw_coord"] = '16N8295001158500'
    coordinatesWithDates3["ne_coord"] = '16N8297501158700'
    res9DatasetInGeoRangeButOutOfTimeRange = sreq.getDatasetsFromWorkspace(ws, coordinatesWithDates3)
    print("RES9")
    tu.printResult(res9DatasetInGeoRangeButOutOfTimeRange)


    coordinatesWithDates4 = {}
    coordinatesWithDates4["from_date"] = '2020-08-24T12:10'
    coordinatesWithDates4["to_date"] = '2022-10-24T12:10'
    coordinatesWithDates4["sw_coord"] = '17N8095001158500'
    coordinatesWithDates4["ne_coord"] = '17N8097501158700'
    res10DatasetOutOfGeoRangeButInTimeRange = sreq.getDatasetsFromWorkspace(ws, coordinatesWithDates4)
    print("RES10")
    tu.printResult(res10DatasetOutOfGeoRangeButInTimeRange)


testGetDatasetBySpatialWindow()