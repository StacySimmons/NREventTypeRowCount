# NR Event Type Row Count
A Python script to retrieve all Event Types in a New Relic account and return the row count for each
```
usage: main.py [-h] -a ACCOUNTID [-o OUTPUTFILE] [-p] apikey

Query a New Relic RPM for all Event Types and their row counts

positional arguments:
  apikey                New Relic Query API Key

optional arguments:
  -h, --help            show this help message and exit
  -a ACCOUNTID, --accountid ACCOUNTID
                        New Relic RPM Account ID
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        File name to report results
  -p, --printoutput     Print output file to screen in addition to file
```

