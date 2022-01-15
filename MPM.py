import numpy as np

class Task:
    def __init__(self,name :str ,duration = 0):
        self.name = name
        self.duration = duration
        self.erliest_date = 0
        self.latest_date = 0
        self.total_margin = 0
        self.free_margin = 0
    def __str__(self):
        return self.name+"[ "+str(self.erliest_date)+" , "+str(self.latest_date)+" , "+str(self.total_margin)+" , "+str(self.free_margin)+" ]"

class Link:
    def __init__(self,start_task :Task,end_task :Task,duration = 0):
        self.duration = duration
        self.start_task = start_task
        self.end_task = end_task

    def __str__(self):
        return str(self.start_task)+"---------------("+str(self.duration)+")------------>"+str(self.end_task)


class Mpm:
    def __init__(self):
        self.all_taskes = dict()
        self.all_linkes = list()
    def create_MEM_graph(self,table):
        start =Task("start")
        self.all_taskes["start"] = start
        for row in table:
            task = Task(row[0],row[1])
            self.all_taskes[row[0]] = task
            if row[2] ==[]:
                link = Link(start,task)
                self.all_linkes.append(link)
            for data in row[2]:
                link = Link(self.all_taskes[data],task,self.all_taskes[data].duration)
                self.all_linkes.append(link)
        lis = list(self.all_taskes.keys())
        lis.remove("start")
        for row in table:
            for i in row[2]:
                if i in lis:
                    lis.remove(i)
        end = Task("end")
        self.all_taskes["end"] = end
        for task in lis:
            link = Link(self.all_taskes[task],end,self.all_taskes[task].duration)
            self.all_linkes.append(link)
        self.__erliest_date(start)
        self.all_taskes["end"].latest_date = self.all_taskes["end"].erliest_date
        self.__latest_date(end)
        self.total_margin()
        self.free_margin()

    def __erliest_date(self,start):
        if start == self.all_taskes["end"]:
            return None
        for link in self.all_linkes:
            if link.start_task == start :
                link.end_task.erliest_date = self.__MAX(link.end_task)
        for link in self.all_linkes:
            if link.start_task == start :
                self.__erliest_date(link.end_task)
    def __latest_date(self,end):
        if end == self.all_taskes["start"]:
            return None
        for link in self.all_linkes:
            if link.end_task == end :
                link.start_task.latest_date = self.__MIN(link.start_task)
        for link in self.all_linkes:
            if link.end_task == end:
                self.__latest_date(link.start_task)

    def print_mpm(self):
        for link in self.all_linkes:
            print(str(link))
    def __MAX(self,start):
        MAX = 0
        for link in self.all_linkes:
            if link.end_task == start and link.start_task.erliest_date + link.duration >= MAX:
                MAX = link.start_task.erliest_date + link.duration
        return MAX
    def __MIN(self,end):
        MIN = self.all_taskes["end"].erliest_date
        for link in self.all_linkes:
            if link.start_task == end and link.end_task.latest_date - link.duration <= MIN:
                MIN = link.end_task.latest_date - link.duration
        return MIN
    def total_margin(self):
        for task in self.all_taskes.values():
            task.total_margin = task.latest_date-task.erliest_date
    def free_margin(self):
        for task in self.all_taskes.values():
            MIN = np.inf
            for link in self.all_linkes:
                if link.start_task == task and link.end_task.erliest_date - task.erliest_date -link.duration <= MIN :
                    MIN = link.end_task.erliest_date - task.erliest_date -link.duration
            task.free_margin = MIN
    def critical_path(self):
        for link in self.all_linkes:
            if link.start_task.total_margin == 0 and link.end_task.total_margin == 0:
                print(str(link))

tache =[["A",6,[]],["B",2,[]],["C",7,["B"]],["D",8,["B"]],["E",3,["A","C"]],["F",4,["E","D"]]]  


T=Mpm()
T.create_MEM_graph(tache)
T.critical_path()