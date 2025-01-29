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
which is the heart of the program. This is where all the code is executed.
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
which is the function to determine the published_date of each image. This function along with many others are designed to retrieve a specific attribute of each image from the API response to determine the most recent image in each content stream for rhbk/keycloak-rhel9. This function is designed to retrieve the published_date of each image, and return a list of the times, which is crucial information that we need. The next function is 
```
def versions(text):
```
which is the function that is designed to determine the version of each image, this function as well as the next function
```
def release(text):
```
which is a function to determine the release of each image, are both written similarly. This is due to them both being at the same level in 'data'. These functions return a list of the versions and releases respectively. 

The final two functions that retrieve information from the API are 
```
def vcs_Ref(text):
```
and
```
def fresh_Grade(text):
```
The former is written the same as the first two functions due to it being stored at the same level in 'data' as version and release. While the latter is written slightly differently. This is due to it being a key in 'data', and you do not need to access as many levels in the structure to retrieve the information. These functions both return a list of all 'vcs-ref'  and ''grade'.

The final two functions handle the sorting and printing logic for my solution. The first of these functions is
```
def find_Newest(times, res_vers, res_release, vcs_ref, fresh_grade):
```
which determines what our most recent image in each content stream is. This function takes all of the lists we generated from the previous functions, and merges them into a single dictionary, where each key is the version e.g 26.0, and the values store tuples of its published_date, release, vcs-ref and freshness_grade. I used the zip() function, a loop, and defaultdict() function to do this. I then converted the dictionary to a set then back to a list to remove duplicates in the dictionary due to architecture e.g ppc64le, amd64 for the same release. 

Then I sort the full dictionary to get the most recent time for each key 22, 26.0, 24. I do this by creating an empty dictionary which will hold the sorted information, then loop over the full dictionary using the key and pair, and then sort the entries by time, which is the first element of the tuple. This is then added into our new dictionary at each key as the most recent entry for the newest time for each version. This dictionary is then returned.

The final function which handles the printing of the solution is:
```
def printing(input_dict):
```
First of all, I create an empty list to store the answer for printing. Then I loop over the inputted dictionary using the key value pair x and y, and create a new dictionary which presents all the information for the most recent image in each content stream. This dictionary's values are changed each time based on our inputted dictionary, and are appended to the end of our list for printing. 

The printing process of the function works using the json module in Python. Here I convert Python to JSON using json.dumps(), and indent by 4 for pretty printing. The answer in correct JSON format is then printed to VSC's terminal.

!!! The printing process sometimes changes the vcsRef and freshnessGrade values each time the program is run. This is due to multiple versions e.g: ppc64le, amd64 are released at the same time. !!! 