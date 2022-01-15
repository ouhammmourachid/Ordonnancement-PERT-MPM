
class Stage:
    def __init__(self ,name :str):
        self.name = name
        self.erliest_date = 0
        self.latest_date = 0
    def __str__(self):
        return self.name+f'[{self.erliest_date},{self.latest_date}]'




class Task:
    def __init__(self ,name :str ,duration :int,background :list,start_stage :Stage ,end_stage :Stage):
        self.name = name
        self.duration = duration
        self.start_stage = start_stage
        self.end_stage = end_stage
        self.background = background
    def add_antecedent(self,anticedent):
        self.antecedent += [anticedent]
    def set_start_stage(self,start_stage):
        self.start_stage = start_stage
    def set_start_stage(self,end_stage):
        self.end_stage = end_stage
    def __str__(self):
        if not self.name.endswith('"') :
            return  "---------------"+self.name+"("+str(self.duration)+")--------------->"
        else:
            return  "- - - - - - - - "+self.name+"("+str(self.duration)+")- - - - - - - ->"

    

class Pert:
    total_task = 0
    total_stage = 2
    __fictif_taske = 0
    def __init__(self ):
        self.end = Stage("end")
        self.start = Stage("start")
        self.all_stages = {"start":self.start,"end":self.end}
        self.all_taskes = dict()
        self.fictif_taskes =dict()
    def create_stage(self,name):
        stage = Stage(name)
        self.all_stages[name]=stage
        self.total_stage += 1
        return stage
    def create_task(self,name,duration,antecedent,start_stage,end_stage):
        task = Task(name,duration,antecedent,start_stage,end_stage)
        self.all_taskes[name] =task
        self.total_task +=1
    
    def create_PERT_graph(self,table):
        for row in table:
            self.create_task(row[0],row[1],row[2],self.start,self.end)
        count = 1
        for task in self.all_taskes.values():
            if task.background!=[]:
                not_yet = []
                for previous_task in task.background:
                    count,not_yet,new_stage=self.add_connection(previous_task,count,not_yet,task)

                if new_stage==None :
                    task.start_stage = self.all_taskes[not_yet[0]].end_stage
                    for h in not_yet[1:]:
                        if self.all_taskes[h].end_stage == self.end:
                            self.all_taskes[h].end_stage = task.start_stage
                        else:
                            fictif_task = Task(f+'2"',0,[task.name],self.all_taskes[h].end_stage,task.start_stage)
                            self.fictif_taskes[f+'2"'] = fictif_task
                            Pert.__fictif_taske += 1
                    not_yet = []
                for f in not_yet:
                    fictif_task = Task(f+'1"',0,[task.name],self.all_taskes[f].end_stage,new_stage)
                    self.fictif_taskes[f+'1"'] = fictif_task
                    Pert.__fictif_taske += 1
        self.__erliest_date(self.start)
        self.end.latest_date = self.end.erliest_date
        self.__latest_date(self.end) 

    def __print(self,task):
        return str(task.start_stage)+str(task)+str(task.end_stage)
    def print_pert(self):
        for task in self.all_taskes.values():
            print(self.__print(task))
        for task in self.fictif_taskes.values():
            print(self.__print(task))

    def add_connection(self,previous_task,count,not_yet,task):
        new_stage = None
        if self.all_taskes[previous_task].end_stage == self.end:
            new_stage = self.create_stage("stage : "+str(count)+" ")
            count += 1
            self.all_taskes[previous_task].end_stage = new_stage
            task.start_stage = new_stage
        else:
            not_yet.append(previous_task)
        return count,not_yet,new_stage

    def __erliest_date(self,start):
        if start == self.end:
            return None
        for task in self.all_taskes.values():
            if task.start_stage == start:
                task.end_stage.erliest_date = self.__MAX(task.end_stage)
        for task in self.all_taskes.values():
            if task.start_stage == start:
                self.__erliest_date(task.end_stage)
        for task in self.fictif_taskes.values():
            if task.start_stage == start:
                task.end_stage.erliest_date = self.__MAX(task.end_stage)
        for task in self.fictif_taskes.values():
            if task.start_stage == start:
                self.__erliest_date(task.end_stage)
        
    def __latest_date(self,end):
        if end == self.start :
            return None
        for task in self.all_taskes.values():
            if task.end_stage == end:
                task.start_stage.latest_date = self.__MIN(task.start_stage)
        for task in self.fictif_taskes.values():
            if task.end_stage == end:
                task.start_stage.latest_date = self.__MIN(task.start_stage)
        for task in self.all_taskes.values():
            if task.end_stage == end:
                self.__latest_date(task.start_stage)
        for task in self.fictif_taskes.values():
            if task.end_stage == end:
                self.__latest_date(task.start_stage)

    def __MIN(self,stage):
        MIN = self.end.erliest_date
        for task in self.all_taskes.values():
            if task.start_stage == stage and task.end_stage.latest_date-task.duration <= MIN:
                MIN = task.end_stage.latest_date-task.duration
        for task in self.fictif_taskes.values():
            if task.start_stage == stage and task.end_stage.latest_date-task.duration <= MIN:
                print(task.start_stage.latest_date,task.end_stage.latest_date)
                MIN = task.end_stage.latest_date-task.duration
        return MIN
    def __MAX(self,stage):
        MAX = 0
        for task in self.all_taskes.values():
            if task.end_stage == stage and task.start_stage.erliest_date+task.duration >= MAX:
                MAX = task.start_stage.erliest_date+task.duration
        for task in self.fictif_taskes.values():
            if task.end_stage == stage and task.start_stage.erliest_date+task.duration >= MAX:
                MAX = task.start_stage.erliest_date+task.duration
        return MAX
    def total_margin(self):
        dic =dict()
        for task in self.all_taskes.values():
            dic[task.name] = task.end_stage.latest_date - task.start_stage.erliest_date - task.duration
        return dic
    def free_margin(self):
        dic = dict()
        for task in self.all_taskes.values():
            dic[task.name] = task.end_stage.erliest_date - task.start_stage.erliest_date - task.duration
        return dic
    def critical_path(self):
        for task in self.total_margin():
            if self.total_margin()[task]==0:
                print(self.__print(self.all_taskes[task]))

tache =[["A",2,[]],["B",8,[]],["C",5,["A"]],["D",2,["B"]],["E",6,["B"]],["F",5,["E"]],["G",3,["A","D"]]]
pert = Pert()
pert.create_PERT_graph(tache)
print(pert.total_margin())
print(pert.free_margin())
pert.critical_path()