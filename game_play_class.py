import json
import random
class GamePlay:
    def __init__(self,hints_file_path="./drawing_hints.json",number_of_options=3):
        self.hints_file_path=hints_file_path
        self.number_of_options=number_of_options
        
    def load_hints(self):      
        with open(self.hints_file_path) as json_file:
            json_data = json.load(json_file)
            return json_data
            
    def return_options(self):
        all_hints=self.load_hints()
        return random.sample(all_hints,self.number_of_options)
     
# gp=GamePlay()
# opts=gp.return_options()
        
# print(opts)
