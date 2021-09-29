import serverRequests as sreq
import time
import utils
import json
import os


def retrieveProcess(workspaceName, datasetName, pathToDatasetFiles, datablockSize, results):
    global numberOfPointsToSurpass
    global filesDownloaded
    global totalPointsDownloaded
    global totalDownloadRequestTime
    global f

    numberOfPointsToSurpass = 20000000
    filesDownloaded = 0
    totalPointsDownloaded = 0
    totalDownloadRequestTime = 0

    rootDBs = sreq.getDatablock(workspaceName, datasetName, str(0), None)
    jsondata = json.loads(rootDBs)

    for rootDB in jsondata:
        traverseOctree(rootDB, workspaceName, datasetName)

        if totalPointsDownloaded > numberOfPointsToSurpass:
            ###
            results[pathToDatasetFiles][datablockSize] += (
                filesDownloaded, totalDownloadRequestTime, totalPointsDownloaded,
                totalDownloadRequestTime / filesDownloaded, totalDownloadRequestTime / totalPointsDownloaded)

            writeNumberOfFiles = "Number of files: " + str(filesDownloaded) + "\n"
            print(writeNumberOfFiles)

            writeTotalTimeDownload = "Total time in download: " + str(totalDownloadRequestTime) + "\n"
            print(writeTotalTimeDownload)

            writePointsDownload = "Number of points downloaded: " + str(totalPointsDownloaded) + "\n"
            print(writePointsDownload)

            writeAvgTimeOfFileDownload = "Average time of file: " + str(
                totalDownloadRequestTime / filesDownloaded) + "\n"
            print(writeAvgTimeOfFileDownload)

            writeAvgTimeOfPoint = "Average time of point: " + str(
                totalDownloadRequestTime / totalPointsDownloaded) + "\n"
            print(writeAvgTimeOfPoint)

            files_in_directory = os.listdir()
            filtered_files = [file for file in files_in_directory if file.endswith(".laz")]
            for file in filtered_files:
                os.remove(file)

            return results


def traverseOctree(rootDB, workspaceName, datasetName):
    # Define the local Grid of the nodes
    swBottom = rootDB["cell"]["southWestBottom"]
    neTop = rootDB["cell"]["northEastTop"]
    swBottomStr = swBottom["zone"] + str(swBottom["easting"]) + str(swBottom["northing"])
    neTopStr = neTop["zone"] + str(neTop["easting"]) + str(neTop["northing"])

    dict = {
        "sw_coord": swBottomStr,
        "ne_coord": neTopStr
    }

    return downloadFile(0, dict, workspaceName, datasetName)


def downloadFile(nextId, dict, workspaceName, datasetName):
    global numberOfPointsToSurpass
    global filesDownloaded
    global totalPointsDownloaded
    global totalDownloadRequestTime

    text = sreq.getDatablock(workspaceName, datasetName, str(nextId), dict)
    tmpNode = json.loads(text)
    start = time.time()
    sreq.getDatablockFile(workspaceName, datasetName, str(nextId), dict)
    end = time.time()
    totalDownloadRequestTime += (end - start)
    filesDownloaded += 1
    totalPointsDownloaded += int(tmpNode[0]["size"])
    time.sleep(0.1)

    children = tmpNode[0]["children"]

    for child in children:
        if totalPointsDownloaded < numberOfPointsToSurpass:
            downloadFile(child, dict, workspaceName, datasetName)
        else:
            pass


def databaseStats(workspaceName, datasetName):
    writeNumberOfDblocksGenerated = "Number of datablocks generated: " + sreq.getOctreeSize(workspaceName,
                                                                                            datasetName) + "\n"
    print(writeNumberOfDblocksGenerated)

    writeMaxDepthInOctree = "Max depth in octree: " + sreq.getOctreeMaxDepth(workspaceName, datasetName) + "\n"
    print(writeMaxDepthInOctree)

    writeDatabaseSize = "Database size: " + sreq.getDatabaseSize() + "\n"
    print(writeDatabaseSize)
