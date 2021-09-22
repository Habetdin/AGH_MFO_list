#!/bin/bash

rm live.txt &> /dev/null
rm dead.txt &> /dev/null

cat mirrors.txt | while read _host 
do
    if ping -c 3 "$_host" &> /dev/null; then
        _title=$(curl -Ls "http://$_host" | grep -o "<title>[^<]*" | head -n1 | tail -c+8)
        echo -e "# ${_title}\n${_host}\n" >> live.txt
    else
        echo -e "${_host}" >> dead.txt
    fi
done
