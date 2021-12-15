# CDSLab User

This API constitutes the user management module in CDSLab.

---
## Environment Setup
We recommend using a local python environment with _virtualenv_ tool, to avoid
messing with the global installation. In the following process we will go
through the process of creating such environment (generally known as
_virtual environment_), it will be named *.venv*

### Creation of Virtual Environment

```shell
python -m venv .venv # You could name environment as you want.
source .venv/bin/activate
python -m pip install -r requirements.txt
```

---
## Configuration Files


### Environment Configuration

The `.env` file will have all configurations to run applications, you have to
create file and write own configuration, you can check all variables in file 
_.env_example_ and write you own configuration.

---
## Run Application
Once, you write all configurations, you should be ready to start your
application, the best way to run is through uvicorn module in you virtual
environment.

```shell
uvicorn main:app --host 0.0.0.0 --port 5000
```
and thats all, you are ready.

