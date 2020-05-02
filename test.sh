#!/bin/bash

function p { 
    sleep $1 
    printf '\n\n\n' 
}

function test { 
    clear 
    echo $1 ; echo ""
    out=$( echo $2 $3 $4 $5 $6 $7 $8 )
    echo $out
    p 1 
    $2 $3 $4 $5 $6 $7 $8
    echo "success ? y or n" 
    read -r suc
    if [ $suc == "n" ] ; then
        fail+=[$out]
    else
        pass+=[$out]
    fi
}


function end {
    p 1 : clear
    echo "FAILED" > test.txt 
    for i in "${fail[@]}"; do echo $i >> test.txt ; done
    echo "" ; echo "PASSED" >> test.txt
    for i in "${pass[@]}"; do echo $i >> test.txt ; done
    sed -e 's/\[//' -e 's/]\[/\n/g' -e 's/]//g'< test.txt > testresults.txt
    files=(test.txt steve.tf y.tf n.tf)
    for i in "${files[@]}" ; do if [ -f $i ]; then rm $i ; fi ; done
    clear 
    cat testresults.txt
}

function killlast {
   sleep 10
   kill $(ps -s $$ -o pid=)
}

function tests {
    test "SHOULD SHOW A NICE WELCOME" "./iac2tf"
    test "SHOULD COMPLAIN OF NO FILE" "./iac2tf" "-f"
    test "SHOULD ASK FOR A FILE NAME" "./iac2tf" "-f" "/home/bob/present/proj/WorksArea/CloudFormation/site.json" 
    test "SHOULD INDICATE - output flag seen but output name not found - Please provide a name for this S3" "./iac2tf" "-f" "/home/bob/present/proj/WorksArea/CloudFormation/site.json" "-o"
    test "SHOULD COMPLETE A FILE NAMED steve" "./iac2tf" "-f" "/home/bob/present/proj/WorksArea/CloudFormation/site.json" "-o" "steve"
    test "SHOULD INDICATE - THIS TYPE OF FILE CANNOT BE PROCESSED PLUS THAT IT IS A TXT FILE" "./iac2tf" "-f" "/home/bob/present/proj/WorksArea/CloudFormation/site" "-o" "steve"
    test "SHOULD INDICATE - THIS TYPE OF FILE CANNOT BE PROCESSED PLUS THAT IT IS A TXT FILE" "./iac2tf" "-f" "/home/bob/present/proj/WorksArea/CloudFormation/site.txt" "-o" "steve"
    test "SHOULD INDICATE - THIS TYPE OF FILE CANNOT BE PROCESSED PLUS THAT IT IS A HTML FILE" "./iac2tf" "-f" "/home/bob/present/proj/WorksArea/CloudFormation/site.html" "-o" "steve"
    test "SHOULD COMPLAIN OF NO SCRIPT INPUT" "./iac2tf" "-s"
    test "PASSED A FILE ON A SCRIPT COMMAND - SHOULD PROCESS CORRECTLY ASKING FOR A NAME" "./iac2tf" "-s" "/home/bob/present/proj/WorksArea/CloudFormation/site.json" 
    test "SHOULD SHOW HELP" "./iac2tf" "-h"
    test "SHOULD SHOW HELP" "./iac2tf" "--help"
    test "SHOULD ASK IF --HELP IS WHAT YOU MEANT" "./iac2tf" "-help"
    bash iac2tf -gui & sleep 6 ; guidie=$( ps -fax | grep 'python3 gu[i]' | awk '{print $1}' ) ; sleep 1 ; kill -9 $guidie ; test "DID THE GUI START, LOGO SHOW AND IT END?" "echo 'GUI RAN SUCCESSFULLY?'"
}

function main {
    tests
    end
}

pass[]
fail[]
main