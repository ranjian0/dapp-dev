# Learning DAPP development 

## Environment setup

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ 
$ python -c "from solcx import install_solc; install_solc(version='latest')"
$ export GANACHE_URL="http://127.0.0.1:7545"
$ export WEB3_INFURA_PROJECT_ID="<your project id>"
```


## Deploy a contract

```shell
$ python deploy.py --folder lottery --chain ganache
```

if chain is 'ganache', ensure the environment variable 'GANACHE_URL' is set
otherwise set the environment variable 'WEB3_INFURA_PROJECT_ID'

## Run some tests

```shell
$ pytest lottery/tests
```