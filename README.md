# Red_Hat_Take_Home_John_Dunne
My solution for the 042234 continuous release automation take home for Red Hat.

This solution was written in Python using version 3.11.9 on Visual Studio Code (VSC) version 1.96.4

To run this program, make sure that you have installed Python 3.11.9 in your VSC environment, as well as the 'requests' module which is external.
To do this, run this command in VSC's terminal:
```
pip install requests
```

Once this is completed, you can run the program by clicking 'Run' -> 'Run Without Debugging' which is situated on the top UI bar of VSC.
The solution will appear in the built in terminal.




SOLUTION DETAILS:


My solution has various different parts which are modularly connected with one another. This allows for a solution which is easily changeable and expansive for future development if neccesary. The first part of the solution is the main section 
```
if __name__ == "__main__":
```
which is the heart of the program. This is where all the code is executed and outputs of functions are passed as inputs to other functions.
This section also consists of some important information such as 
```
repository_images = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk/keycloak-rhel9/images"
``` 
which is the API repository holding the Red Hat build of Keycloak’s container image history, and
```
text = json.loads(repo_Response.text)
```
which deseriealizes the JSON received from the API to a Python object so we can read it, and feed it to our functions for evaluation.


FUNCTIONS:


The first function in the solution is
```
def image_Times(text):
```
which is the function to determine the published_date of each image. This function along with many others are designed to retrieve a specific attribute of each image from the API response to determine the most recent image in each content stream for rhbk/keycloak-rhel9. This function is designed to retrieve the published_date of each image.




