import json
import utils.PrintLog as PrintLog



with open( "status.json" ) as f:
    content = f.read()
    self_status = json.loads( content )



configs = {}

with open( "configs.json" ) as f:
    configs = json.loads( f.read() )


