import os, sys
sys.path.append("..")

from queue import Queue
from threading import Thread

from splunk.splunkinterface import SplunkClient

from managers.logentrymanager import LogEntryManager
 
def ingestion(): 
    splunk = SplunkClient()
    entryManager = LogEntryManager.get_instance()

    # Cleansing process should convert all files into python objects(LogFile)
    # TODO: Get log files from LogFileManager
    for root, dir, files in os.walk("/home/eder/Desktop/pick/pick-tool-team07-runtime-terror/test/root"): 
        for file in files: 
            pathFile = root+"/"+file
            splunk.upload(pathFile)
            # TODO: Update LogFile to ingestionStatus completed

            results = splunk.results(pathFile)

            for result in results: 
                entryManager.addEntry(
                    result["host"], 
                    result["timestamp"], 
                    result["content"], 
                    result["source"], 
                    result["sourcetype"]
                )


    # job_logentires = []
    # while not queue.empty(): 
    #     job = ingestion_queue.get()
    #     print("uploading", job)
    #     splunk.upload(job)

    #     results = splunk.results(job)

    #     for result in results: 
    #         entry = LogEntry(
    #             result["host"], 
    #             result["timestamp"], 
    #             result["content"],
    #             result["source"], 
    #             result["sourcetype"]
    #         )
    #         job_logentires.append(entry)
    # print(job_logentires)
    # ingestion_queue.task_done()

if __name__ == '__main__': 
    ingestion()
    # t1 = Thread(target=cleansing, args=(ingestion_queue,))
    # t2 = Thread(target=ingestion, args=(ingestion_queue,))
    # t1.start()
    # t2.start()

    # ingestion_queue.join()