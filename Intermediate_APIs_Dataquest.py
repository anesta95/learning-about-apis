#!/home/anesta95/Manipulating_APIs/API_manipulation/bin/python
import requests
import json

#1. INTRODUCTION

#We looked at a basic API in the last mission.
#That API didn't require authentication, but most do.
#Imagine that you're using the reddit API to pull a list of your private messages.
#It would be a huge privacy breach for reddit to give that information to anyone,
#so requiring authentication makes sense.

#APIs also use authentication to perform rate limiting.
#Developers typically use APIs to build interesting applications or services.
#In order to ensure that it remains available and responsive for all users,
#an API will prevent you from making too many requests in too short a time.
#We call this restriction rate limiting.
#It ensures that one user can't overload the API server by making too many
#requests too fast.

#In this mission, we'll explore the GitHub API and use it to pull some
#interesting data on repositories and users. GitHub is a site for hosting code.
#If you haven't looked at it, you should - it's a great place to share a portfolio.

#GitHub has user accounts (example),
#repositories that contain code (example),
#and organizations that companies can create (example).

#2. API AUTHENTICATION

#To authenticate with the GitHub API, we'll need to use an access token.
#An access token is a credential we can generate on GitHub's website.
#The token is a string that the API can read and associate with your account.

#Using a token is preferable to a username and password for a few reasons:

#Typically, you'll be accessing an API from a script.
#If you put your username and password in the script and someone manages to get
#their hands on it, they can take over your account.
#In contrast, you can revoke an access token to cancel an unauthorized person's
#access if there's a security breach.


#Access tokens can have scopes and specific permissions.
#For instance, you can make a token that has permission to write to your GitHub
#repositories and make new ones. Or, you can make a token that can only read
#from your repositories. Using read-access-only tokens in potentially insecure
#or shared scripts gives you more control over security.

#You'll need to pass your token to the GitHub API through an Authorization header.
#Just like the server sends headers in response to our request, we can send the
#server headers when we make a request. Headers contain metadata about the request.
#We can use Python's requests library to make a dictionary of headers,
#and then pass it into our request.

#We need to include the word token in the Authorization header,
#followed by our access token. Here's an example of an Authorization header:

#{"Authorization": "token 1f36137fbbe1602f779300dad26e4c1b7fbab631"}

#You should never share your token with anyone you don't want to have access to
#your account. We've revoked the token you'll be using throughout this mission,
#so it isn't valid anymore. Consider a token somewhat equivalent to a password,
#and store it securely

#Create a dictionary of headers containing our Autorization header
headers = {"Authorization": "token your token here"}

#Make a GET request to the GitHub API with our headers.
#This API will give details about my GitHub repos
response = requests.get("https://api.github.com/users/anesta95",
headers=headers)
#Print the content of the response. As you can see, this token corresponds to my
#account
print(response.json())

bio = response.json()["bio"]
print(bio)

#3. ENDPOINTS AND OBJECTS

#APIs usually let us retrieve information about specific objects in a database.
#On the previous screen, for example, we retrieved information about a specific
#user object, VikParuchuri. We could also retrieve information about other
#GitHub users through the same endpoint.
#For example, https://api.github.com/users/torvalds would get us information about Linus Torvalds.

#response = requests.get("https://api.github.com/users/torvalds", headers=headers)
#torvalds = response.json()

#You can use any username that you have API authentication access to at the
#end of endpoint https://api.github.com/users/ to access the JSON of their
#GitHub details.

#4. OTHER OBJECTS

#In addition to users, the GitHub API has a few other types of objects.
#For example, https://api.github.com/orgs/dataquestio will retrieve information
#about the Dataquest organization on GitHub.
#https://api.github.com/repos/octocat/Hello-World will give us information about
#the Hello-World repository that the user octocat owns.

#GitHub offers full documentation for all of the API's endpoints.

#response = requests.get("https://api.github.com/repos/octocat/Hello-World", headers=headers)
#hello_world = response.json()


#5. PAGINATION

#Sometimes, a request can return a lot of objects.
#This might happen when you're doing something like listing out all of a user's
#repositories, for example. Returning too much data will take a long time and
#slow the server down. For example, if a user has 1,000+ repositories,
#requesting all of them might take 10+ seconds.
#This isn't a great user experience, so it's typical for API providers to
#implement pagination. This means that the API provider will only return a
#certain number of records per page. You can specify the page number that
#you want to access. To access all of the pages, you'll need to write a loop.


#To get the repositories a user has starred (marked as interesting),
#we can use the following API endpoint:

#https://api.github.com/users/anesta95

#We can add two pagination query parameters to it - page, and per_page. page is
#the page we want to access, and per_page is the number of records we want to see
#on each page. Typically, API providers enforce a cap on how high per_page can be,
#because setting it to an extremely high value defeats the purpose of pagination.

params = {"per_page": 50, "page": 1}
response2 = requests.get("https://api.github.com/users/anesta95/starred",
headers=headers, params=params)

page1_repos = response2.json()
print(page1_repos)


#6. USER-LEVEL ENDPOINTS

#So far, we've looked at endpoints where we need to explicitly provide the
#username of the person whose information we're looking up.
#For example, we used https://api.github.com/users/anesta95/starred to pull
#up the repositories that anesta95 starred.

#Since we've authenticated with our token, the system knows who we are,
#and can show us some relevant information without us having to specify our username.


#Making a GET request to https://api.github.com/user will give us information
#about the user the authentication token is for.

#There are other endpoints that behave like this.
#They automatically provide information or allow us to take actions as the authenticated user.

r = requests.get("https://api.github.com/user", headers=headers)
user = r.json()
print(user)

#7. POST REQUESTS

#So far, we've been making GET requests.
#We use GET requests to retrieve information from a server (hence the name GET).
#There are a few other types of API requests.

#For example, we use POST requests to send information (instead of retrieve it),
#and to create objects on the API's server.
#With the GitHub API, we can use POST requests to create new repositories.


#Different API endpoints choose what types of requests they will accept.
#Not all endpoints will accept a POST request, and not all will accept a GET request.
#You'll have to consult the API's documentation to figure out which endpoints accept which types of requests.


#We can make POST requests using requests.post. POST requests almost always include data,
#because we need to send the data the server will use to create the new object.


#We pass in the data in a way that's very similar to what we do with query parameters and GET requests:

#payload = {"name": "test"}
#requests.post("https://api.github.com/user/repos", json=payload)

#The code above will create a new repository named test under the account of the
#currently authenticated user. It will convert the payload dictionary to JSON,
#and pass it along with the POST request.

#Check out GitHub's API documentation for repositories to see a full list of
#what data we can pass in with this POST request. Here are just a couple data points:

#name -- Required, the name of the repository
#description -- Optional, the description of the repository


#A successful POST request will usually return a 201 status code indicating that
#it was able to create the object on the server. Sometimes, the API will return
#the JSON representation of the new object as the content of the response.

# Create the data we'll pass into the API endpoint.
#While this endpoint only requires the "name" key, there are other optional keys.

payload = {"name": "learning-about-apis"}

# We need to pass in our authentication headers!
response3 = requests.post("https://api.github.com/user/repos", json=payload,
headers=headers)
status = response3.status_code
print(status)


#8. PUT/PATCH REQUESTS

#Sometimes we want to update an existing object, rather than create a new one.
#This is where PATCH and PUT requests come into play.

#We use PATCH requests when we want to change a few attributes of an object,
#but don't want to resend the entire object to the server.
#Maybe we just want to change the name of our repository, for example.


#We use PUT requests to send the complete object we're revising as a replacement
#for the server's existing version.

#In practice, API developers don't always respect this convention.
#Sometimes API endpoints that accept PUT requests will treat them like PATCH requests,
#and not require us to send the whole object back.


#We send a payload of data with PATCH requests, the same way we do with POST requests:

#payload = {"description": "The best repository ever!", "name": "test"}
#response = requests.patch("https://api.github.com/repos/VikParuchuri/test",
#json=payload)

#The code above will change the description of the test repository to
#The best repository ever! (we didn't specify a description when we created it).
#We provide the name also, since the GitHub API specification says this is a required field.

#A successful PATCH request will usually return a 200 status code.

payload2 = {"description": "A collection of API exploration tutorials.",
"name":"learning-about-apis"}

response4 = requests.patch('''https://api.github.com/repos/anesta95/
learning-about-apis''', headers=headers, json=payload2)

print(response4.status_code)


#9. DELETE REQUESTS

#The final major request type is the DELETE request.
#The DELETE request removes objects from the server.
#We can use the DELETE request to remove repositories.

#response = requests.delete("https://api.github.com/repos/VikParuchuri/test")


#The above code will delete the test repository from GitHub.

#A successful DELETE request will usually return a 204 status code indicating
#that it successfully deleted the object.

#Use DELETE requests carefully - it's very easy to remove something important by accident.

response5 = requests.delete('''https://api.github.com/repos/anesta95/
learning-about-apis''', headers=headers)

status = response5.status_code
print(status)