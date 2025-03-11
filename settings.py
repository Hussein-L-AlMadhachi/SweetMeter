import json

with open( "status.json" ) as f:
    content = f.read()
    self_status = json.loads( content )

with open( "configs.json" ) as f:
    content = f.read()
