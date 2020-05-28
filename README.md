# authorizer-python

## Running
You can build and run everything on Docker. The cli.sh script will do that
for you:

```bash
$ ./cli.sh build  # build the docker image
$ ./cli.sh run    # to run the app
$ ./cli.sh test   # to run the tests
```

Alternatively, if you have python 3.6+ installed, you can run it directly.
No dependencies are required:

```bash
$ python3 authorizer/authorizer.py < resources/example.txt # to run with example input
$ python3 -m unittest tests/test_integration_authorizer.py -v #to run tests
```


Below is one way you can test the program in the command line:
```bash
$ ./cli.sh run < resources/example.txt
{"account":null,"violations":["account-not-initialized"]}
{"account":{"active-card":true,"available-limit":100.0},"violations":[]}
{"account":{"active-card":true,"available-limit":100.0},"violations":["account-already-initialized"]}
{"account":{"active-card":true,"available-limit":80.0},"violations":[]}
{"account":{"active-card":true,"available-limit":80.0},"violations":["insufficient-limit"]}
{"account":{"active-card":true,"available-limit":70.0},"violations":[]}
{"account":{"active-card":true,"available-limit":60.0},"violations":[]}
{"account":{"active-card":true,"available-limit":50.0},"violations":[]}
{"account":{"active-card":true,"available-limit":50.0},"violations":["high-frequency-small-interval","doubled-transaction"]}
{"account":{"active-card":true,"available-limit":50.0},"violations":["high-frequency-small-interval"]}
```
