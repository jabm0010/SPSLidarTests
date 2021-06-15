import serverRequests as sreq
import time
import utils


#Encapsulates the process of creation (post workspace + post dataset + put data)
def createProcess(workspace, dataset, pathToDatasetFiles, datablockSize, octreeSize, results):
    # Reset DB, insert workspace and dataset
    #sreq.resetDatabase()
    time.sleep(20)

    sreq.postWorkspace(workspace)
    sreq.postDataset(workspace["name"], dataset)
    sreq.modifyMaxDepthOctree(octreeSize)

    files = utils.loadDirectory(pathToDatasetFiles)
    start = time.time()
    sreq.putData(workspace["name"], dataset["name"], files)
    end = time.time()

    ###
    results[pathToDatasetFiles][datablockSize] += ((end - start),)

    write = "Dataset: " + pathToDatasetFiles + "\n" + \
            "Max depth: " + str(octreeSize) + "\n" + \
            "Datablock max size: " + str(datablockSize) + "\n" + \
            " time: " + str((end - start)) + "\n"
    print(write)

    return results
