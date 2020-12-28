from pymongo import *
import json
 
 
class JsonToMongo(object):
    def __init__(self, jsfile):
        # ask zjj for host and port 
        self.host = 'localhost'
        self.port = 0000
        self.jsfile = jsfile
 
    def __open_file(self):
        self.file = open(self.jsfile, 'r')
        self.client = MongoClient(self.host, self.port)
        self.db = self.client["paperDB"]
        self.collection = self.db["paperCollection"]
 
    def __close_file(self):
        self.file.close()
 
    def write_database(self):
        self.__open_file()
 
        data = json.load(self.file)

        for item in data:
            try:
                self.collection.insert_one(item)
                print("success " + str(item["_id"]))
            except Exception as e:
                print(e)
                print("fail " + str(item["_id"]))

        self.__close_file()
 
 
if __name__ == '__main__':
    jsfile = "/data/zjj/code/search/test.json"
    j2m = JsonToMongo(jsfile)
    j2m.write_database()

    # with open(jsfile, "r", encoding="utf-8") as fin:
    #     js = json.load(fin)
    
    # with open("format.json", "w", encoding="utf-8") as fout:
    #     output = json.dumps(js, ensure_ascii=False, indent=2, separators=(',', ': '))
    #     fout.write(output)   
