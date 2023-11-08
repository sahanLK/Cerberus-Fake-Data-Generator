
import json
from typing import Any
import string
import random


schema = """{"processingCode":{"required": true, "type": "string", "maxlength":6}, "transactionDetails":{"required":true,"type":"dict","schema":{"amount":{"required":true,"type":"number","max":1.0E10},"transactionDateTimeGmt":{"required":true,"type":"string","minlength":10,"maxlength":10},"timeLocal":{"required":true,"type":"string","minlength":6,"maxlength":6},"dateLocal":{"required":true,"type":"string","minlength":4,"maxlength":4}, "type":{"required":true,"type":"string"}}}, "merchantDetails":{"required":true,"type":"dict","schema":{"id":{"required":true,"type":"string","maxlength":15},"type":{"required":true,"type":"string","minlength":4,"maxlength":4}, "amountTransactionFee":{"required":true,"type":"number"},"amountSettlementFee":{"required":true,"type":"number"}}},"posDetails":{"required":true,"type":"dict","schema":{"terminalId":{"required":true,"type":"string","maxlength":8},"conditionCode":{"required":true,"type":"string","maxlength":2}}}, "EFTTLVData":{"required":true,"type":"dict","schema":{"destinationBankCode":{"required":true,"type":"string","maxlength":5},"originatingBankCode":{"required":true,"type":"string","maxlength":5}, "transactionCode":{"required":true,"type":"string","maxlength":2}}}, "accountFrom":{"required":true,"type":"string","maxlength":99}, "accountTo":{"required":true,"type":"string","maxlength":99}, "stan":{"required":true,"type":"string","minlength":6,"maxlength":6},"rrn":{"required":true,"type":"string","minlength":12,"maxlength":12},"acquirerId":{"required":true,"type":"string","maxlength":11}, "additionalTeriminalData":{"required":true,"type":"string","maxlength":6}, "currencyCode":{"required":true,"type":"string","minlength":3,"maxlength":3}}"""


def get_value(required: bool, min_length: int, max_length: int, data_type: Any):
   if not required:
      return ""
   if data_type == 'string':
      return "".join(random.choices(string.ascii_lowercase + string.digits, k=max_length))
   if data_type == 'number':
      return "".join(random.choices(string.digits, k=max_length))


def get_mock_request(schema: dict):
   output = {}

   for key, val in schema.items():
      if not 'schema' in val.keys():
         required = val.get('required')
         max_length = val.get('maxlength', 0)
         min_length = val.get('minlength', 0)
         data_type = val.get('type')
         output[key] = get_value(required, min_length, max_length, data_type)
      else:
         output[key] = get_mock_request(val['schema'])
   return output


d = json.loads(schema)
out = get_mock_request(d)
print(out)
