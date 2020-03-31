import os

import splunklib.client as client
import splunklib.results as results 

# Should we create an instance of the following class for each 
# log file we upload? If so, will that be a problem where multiple instances
# are making a connection to splunk simultaneously? 
class SplunkClient(object): 
    HOST = "localhost"
    PORT = 8089

    # These attributes is based on the splunk admin account. 
    # Should probably store this information in a config file 
    # and also request this information from the user. 
    USERNAME = "eirodriguez5"
    PASSWORD = "RodH@ker2110"

    # TODO: Need to verify if every "Assesment" will need a new index.
    INDEX = "test_app"

    def __init__(self): 
        self.connect()

    def connect(self): 
        try: 
            self.service = client.connect(
                host=self.HOST, 
                port=self.PORT, 
                username=self.USERNAME, 
                password=self.PASSWORD
            )
        except Exception as e: 
            # TODO: Handle this case
            print(str(e))

    def upload(self, file, team=None): 
        if self.service == None: 
            self.connect()

        try: 
            index = self.service.indexes[self.INDEX]
        except Exception as e: 
            # TODO: Handle this case
            print(str(e))
            index = self.createIndex(self.INDEX)

        # TODO: Setup full path to file from event config
        # For now trust that we are given the full path

        try: 
            filename = os.path.basename(file)
            index.upload(file, **{"rename-source":filename})
        except e: 
            print(str(e))

    def createIndex(self, name): 
        return self.service.indexes.create(name)

    # The definition of this function kind of specified that there will only
    # be one instance of Splunk that will manage all uploads and resutls for all files
    def results(self, file, team=None): 
        filename = os.path.basename(file)
        search = "search source=\"%s\" index=\"%s\"" % (filename, self.INDEX)
        job = self.service.jobs.create(search, preview=True)
        while True: 
            while not job.is_ready(): 
                print("Job is not ready")

            if job["isDone"] == "1":
                print("Job done")
                break
         
        reader = results.ResultsReader(job.results())
        res = []
        # Only get necessary data
        for result in reader: 
            entry = dict()
            entry["timestamp"] = result["_time"]
            entry["content"] = result["_raw"]
            entry["host"] = result["host"]
            entry["source"] = result["source"]
            entry["sourcetype"] = result["sourcetype"]
            res.append(entry)
        return res

        

if __name__ == '__main__': 
    splunk = SplunkClient()
    # splunk.upload("/home/eder/Desktop/pick/pick-tool-team07-runtime-terror/test/root/Red/syslog")
    #splunk.results("/home/eder/Desktop/pick/pick-tool-team07-runtime-terror/test/root/Red/syslog")