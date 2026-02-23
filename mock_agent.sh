#!/bin/bash
while true; do
  read -p "> " input
  if [[ $input == "exit" ]]; then break; fi
  echo "Agent: I am a helpful AI. You said: $input"
done
