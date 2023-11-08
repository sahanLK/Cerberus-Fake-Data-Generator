import argparse
import json
from typing import Any
import string
import random


parser = argparse.ArgumentParser(
   prog="Cerberus Fake Data",
   description="Generate fake data for given Cerberus schema",
   epilog="It's all Fake"
)
parser.add_argument('-s', '--schema')
args = parser.parse_args()



class CerberusFakeData:
   def __init__(self, schema: string) -> None:
      self.schema = json.loads(schema)
   
   def __get_value(self, required: bool, min_length: int, max_length: int, data_type: Any):
      if not required:
         return ""
      if data_type == 'string':
         return "".join(random.choices(string.ascii_lowercase + string.digits, k=max_length))
      if data_type == 'number':
         return "".join(random.choices(string.digits, k=max_length))
      
   def __generate_data(self, schema: dict) -> dict:
      output = {}

      for key, val in schema.items():
         if not isinstance(val, dict):
            continue

         if not 'schema' in val.keys():
            required = val.get('required')
            max_length = val.get('maxlength', 0)
            min_length = val.get('minlength', 0)
            data_type = val.get('type')
            output[key] = self.__get_value(required, min_length, max_length, data_type)
         else:
            output[key] = self.__generate_data(val['schema'])
      return output
   
   def get_mock_data(self) -> dict:
      return self.__generate_data(self.schema)



if __name__ == "__main__":
   obj = CerberusFakeData(args.schema)
   data = obj.get_mock_data()
   print(data)
