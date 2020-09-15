# Service
The backend for the word grouping exercise.

## Live Demo
https://shinji-project.azurewebsites.net/

On the first run, if there is no persistent data storage made yet, you will get an error message in response.
This is intentional: the application by default uses the persistent data to initialize the service.
You should visit the following URL to initialize the service with the test data.

https://shinji-project.azurewebsites.net/init

## Requirements

1. Python 3.8
2. `pip install flask`
3. `pip install flask-cors`

## Testing from Command Line

`main.py` was originally used to test the logic without HTTP requests.

* `python main.py`, or
* in VSCode use Run Configuration `main.py`

## Running as Service

Running Flask will start the web service application in `app.py`.

* `python -m flask run`, or
* in VSCode use Run Configuration `Flask`

## Service Endpoints
All service endpoints are using HTTP GET method.
I understand this is not compliant with the HTTP specification and it is easy to be corrected.
However, it is just done so as a proof of concept to develop this prototype.

| Route | Method | Description | Parameters | Response |
|-|-|-|-|-|
| `/init` | GET | Initializes the service with default test data | N/A | A JSON string of the error if an exception occurred, empty string otherwise. |
| `/` | GET | Get all groups | N/A | JSON object of all groups and words |
| `/save` | GET | Save changes to a local file on the server | N/A | A JSON string of the error if an exception occurred, empty string otherwise. |
| `/load` | GET | Load groups from a local file on the server | N/A | A JSON string of the error if an exception occurred, empty string otherwise. |
| `/group/<group>` | GET | Get a specific group | `group`: Name of the group to be fetched. | JSON object of the group if it exists, empty object otherwise. |
| `/add/<group>/<word>` | GET | Adds a word to a specific group | <ul> <li>`group`: Name of the group for the word to be added to.</li> <li>`word`: The word to be added</li> </ul> | A JSON string of the error if an exception occurred, empty string otherwise. |
| `/createGroup/<group>` | GET | Add a group to the data |`group`: Name of the group to be fetched. | A JSON string of the error if an exception occurred, empty string otherwise. |
| `/deleteGroup/<group>` | GET | Delete a group. A group must be empty to be deleted. |`group`: Name of the group to be deleted. | A JSON string of the error if an exception occurred, empty string otherwise. |

## Summary of the Code
I have tried to leave comments in the source when necessary.
Generally, the code is straightforward and I have tried to used descriptive variable names to make it easy to follow.
I personally prefer longer but more descriptive variable/function names than adding comments.

Notice that the implementation allows for scalability, however,
it is assumed that this exercise will not deal with large amounts of data.
In a realistic scenario, if the amount of data is large, the implementation should make use of faster data providers and data streams, and/or paging.

The logic of this application is implemented under two main modules:
* **Parser**: this module deals with the input file. Although very minimal, it provides extensibility of the software.
For example, if the next edition of the input file, uses JSON format, the logic can be added/encapsulated in this module.
* **GroupService**: this module acts as an intermediary component between the consumer (e.g., CLI, HTTP handler, etc.) and the data.
It attempts to implement a service layer design pattern.
The consumer, therefore, does not ever see the actual data source.
The main member of this class is `groups` which is the post-processed data.
