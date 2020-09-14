# Shinji

## Requirements

1. Python 3.8
2. `pip install flask`

## Testing from Command Line

* `python main.py`, or
* in VSCode use Run Configuration `main.py`

## Running as Service

* `python -m flask run`, or
* in VSCode use Run Configuration `Flask`

### Service Endpoints
| Route | Method | Description | Parameters | Response |
|-|-|-|-|-|
| / | GET | Get all groups | N/A | JSON object of all groups and words |
| /save | GET | Save changes to a local file on the server | N/A | A JSON string of the error if an exception occurred, empty string otherwise. |
| /load | GET | Load groups from a local file on the server | N/A | A JSON string of the error if an exception occurred, empty string otherwise. |
| /add/&lt;group&gt;/&lt;word&gt; | GET | Adds a word to a specific group | <ul> <li>`group`: Name of the group for the word to be added to.</li> <li>`word`: The word to be added</li> </ul> | A JSON string of the error if an exception occurred, empty string otherwise. |
