from tinydb import TinyDB, Query
from tinydb.operations import delete
import  os, json, array

db = TinyDB("db.json")

for f in os.listdir("./assets/"):
    if f.endswith(".wav"):
        q = Query()
        if len(db.search(q.filename == str(f))) == 0:
            db.insert({"filename": str(f)})

class Database():
    def getMax(list):
        max = 0
        for item in list:
            if item > max:
                max = item

        return max

    def getFiles(self):
        return json.dumps(db.all())
    
    def addSchedule(seulf, body):
        schedule = json.loads(body)
        q = Query()
        record = db.get(q.filename == schedule["filename"])

        # como validar json de entrada? schedule['schedule'] não existindo, dá pau

        if record:
            try:
                max = 1
                for scheduleFor in record["schedules"]:
                    if scheduleFor["id"] > max:
                        max = scheduleFor["id"]

                schedule["schedule"]["id"] = max + 1
                record["schedules"].append(schedule["schedule"])
            except KeyError:
                schedule["schedule"]["id"] = 1
                record["schedules"] = [schedule["schedule"]]

            db.update(record, q.filename == schedule["filename"])
            return json.dumps(db.get(q.filename == schedule["filename"]))
        else:
            return '{"erro": "Registro não encontrado"}'
    
    def removeSchedule(self, parameters):
        q = Query()
        record = db.get(q.filename == parameters["filename"][0])
        if record:
            scheduleFound = None
            for schedule in record["schedules"]:
                if (str(schedule["id"]) == str(parameters["scheduleId"][0])):
                    scheduleFound = schedule
            
            if scheduleFound:
                record["schedules"].remove(scheduleFound)
                db.update(record, q.filename == parameters["filename"][0])
                return json.dumps(db.get(q.filename == parameters["filename"][0]))
            else:
                return '{"erro": "Registro não encontrado"}'
        else:
            return '{"erro": "Registro não encontrado"}'