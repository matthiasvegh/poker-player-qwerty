#!/bin/bash

json_file=example_flop.json

if [ "$#" -eq "1" ]; then
    json_file=$1
fi

curl -d "action=bet_request&game_state=$(cat $json_file)" http://localhost:9000
