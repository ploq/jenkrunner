JENKRUNNER
---

A simple tool for running Jenkins jobs from the command line.

Usage:
```console
usage: jenkrunner [-h] -j JOB_NAME [-s] [--show-time] --url JENKINS_URL --token
               JOB_TOKEN
               [argument [argument ...]]

positional arguments:
  argument              Arguments to Jenkins job. Is written as 'arg=val'.
                        Handles files with @filename

optional arguments:
  -h, --help            show this help message and exit
  -j JOB_NAME, --job JOB_NAME
  -s, --show
  --show-time
  --url JENKINS_URL
  --token JOB_TOKEN
```
