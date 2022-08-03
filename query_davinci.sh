#!/bin/bash
# AUTHOR:  Karsten SUhre
# DATE:    4 July 2022
# PURPOSE: test openAI Davinci
# USAGE:   insert your API code and run as a shell script
#          at the You: prompt enter your message, Davinci: is the response
# REFS:     https://beta.openai.com/docs/api-reference/making-requests
#          https://beta.openai.com/docs/api-reference/completions/create

set -

# set the openAI key
export OPENAI_API_KEY="enter your API key from https://beta.openai.com here"

clear

PROMPT=""
LASTPROMPT="$PROMPT"
while [ 1 ] ; do

  echo "You:"
  read INPUT
  PROMPT="${PROMPT}You:${INPUT}\nFriend:"
  #echo $PROMPT

  # sanitize the prompt
  PROMPT=`echo "$PROMPT" | sed 's/"//g'`

  # generate the query
  cat > query.json <<EOF
  {
    "model": "text-davinci-002",
    "prompt": "$PROMPT" ,
    "temperature": 0.9,
    "max_tokens": 128,
    "top_p": 1.0,
    "frequency_penalty": -0.5,
    "presence_penalty": -0.5,
    "stop": ["You:"]
  }
EOF

  # run the query
  curl https://api.openai.com/v1/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -d "`cat query.json`" > response.json 2> response.err

  # get the response
  if [ `grep -c '"error":' response.json` -ne 0 ] ; then 
    #cat response.json
    PROMPT="$LASTPROMPT"
    RESPONSE=""
    echo "Davinci: I failed to understand you last message. Please avoid special characters."
  else
    RESPONSE=`cat response.json | sed 's/.*"text":"//' | sed 's/",".*//' | sed 's/\\\\n//g'`
    echo "Davinci: $RESPONSE"
  fi

  # generate next prompt
  LASTPROMPT="$PROMPT"
  PROMPT="$PROMPT$RESPONSE"
  #echo $PROMPT

done
