## ArvanCloud Backend Challenge

This is the repository containing the implementation for ArvanCloud backend developers challenge.


# Installation

Install docker on your host and then in the project root run:
```
docker compose up --build -d
```

# Testing
I used pytest, unittest for testing so you can make a python virtual environment and install the requirements and use the following

run the following in the root for executing all tests:
```
pytest
```

# What's next?
After running the project main route of services becomes available through the host 8001 port and you can access OpenAPI docs through it.
```
localhost:8001/docs
```

Two other subservices are also available with two next ports:
```
localhost:8002/docs
localhost:8003/docs
```

# Disclaimer
This piece of code comes with absolutely no warranty. Because of challenge time limit probably so many parts are still broken and need to be fixed.
I'll work on it if theere is any extension for deadline.