#!/bin/bash

# This starts the uvicorn server, which in turn
# runs the code in get_dp_health.py. The syntax is :
# uvicorn path:appName
#
# So that
# uvicorn get_dp_health:getDPhealthApp
# means look in get_dp_health.py and start the application getDPhealthApp in there
#
# Set up UV if it is not already there
if [ ! -f uv.lock ]
then
 ./setup_uv.sh
fi

# Run the server under UV management.
uv run uvicorn get_dp_health:getDPhealthApp --host localhost --port 8004 --workers 5 --timeout-graceful-shutdown 10

exit 0

