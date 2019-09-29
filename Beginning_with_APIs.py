#!/home/anesta95/Manipulating_APIs/API_manipulation/bin/python
import requests
from twilio.rest import Client
#If you remember in our analogy (restaurant ordering from waiter) that we needed
#to send a request in order to get a response, in order to retrieve data we can
#use the GET request. A GET request takes the URL, in our case the url to
#Open Notify. Let's make a request and print what is returned. When we make
#a request to a url without the right endpoint, we get the html content as a
#response.

#End points are the location of the resources, by hitting the right end point
#we can retrieve the data we need.

request = requests.get('http://api.open-notify.org')
print(request.text)

#Along with the data we also recieve certain statuses, that tells us a bit about
#the response. For example if a request returns a status code 200 then
#everything is OK, if it returns 404 then the page or resource was not found.
#Let's print the status code of the above get request.

print(request.status_code)

#200 means everything is OK. Lets try to hit a fake end point that does not
#exist.

request2 = requests.get('http://api.open-notify.org/fake-endpoint')
print(request2.status_code)

#As expected we recieve a 404 error. This is exactly what happens when we enter
#the wrong url in the web, internally we are trying to hit an end point that
#doesn't exist or the resource was not found at this end point.

    #Data from the International Space Station
#Let's look at a practical example. Open Notify API serves a couple of end
#points to access the NASA data which is very cool! The endpoint /iss-now.json
#tells you the exact location of the space station right at this moment.
#Another /iss-pass.json endpoint returns the time at which the space station
#would do an overhead pass. Another interesting endpoint /astros.json returns
#the number of astronauts in space. Let's try find the number of people in
#space.

people = requests.get('http://api.open-notify.org/astros.json')
print(people.text)

#It may not look very readable but, if we look closely you can see that there
#are 3 people in space and we can also see their names along with a message
#"success".

#Let's try to make it more readable, earlier we introduced json, most APIs
#return a json, luckily requests has a built in json decode method, that can
#turn our data into a native python datatype and make it easier to read.

people_json = people.json()
print(people_json)

#It looks pretty much the same as before, but now we can make use of almighty
#python to garnish this data.

#To print the number of people in space
print("Number of people in space:",people_json['number'])

#To print the number of people in space using a for loop
for p in people_json['people']:
    print(p['name'])


#The result looks much better! Your results may differ, because this data is
#constantly being updated in real time.


#In this part we will work with another open API called datamuse. It is a word
#finding query engine, you can look for words using the API by specifying
#constraints. You can do things like find words that start with a certain
#letter, that rhymes with a certain word and so on.

#At this stage we introduce an important concept known as passing parameters
#to the url string, also known as query parameters. The request we place, is
#the query adn we can use parameters to apply constraints.

#We can do this in two ways. Let's do it with an example. Let's say that we can
#want to find the words that rhyme with the word 'jingle', we can directly
#pass this constraint in the url like this.

#https://api.datamuse.com/words?rel_rhy=jingle

#Here words, is the end point we are hitting and by placeing the '?' symbol we
#can apply the constraints, in this case we are asking the API to get the words
#that rhyme wiht the word 'jingle'. According to the documentation in datamuse
#rel_rhy is the keyword indicating to the API to get perfect rhymes for the
#word specified. Go ahead and copy/paste in your browser and you'll see
#a bunch of text with words that rhyme wiht jingle.

#Let's do the same thing but in a more pythonic way. We can define a variable
#called parameter and pass this along with the request.

parameter = {"rel_rhy":"jingle"}
request3 = requests.get('https://api.datamuse.com/words',parameter)

#By passing the parameter this way we are doing exactly the same thing we did
#before, using the url. Now, let's go ahead and print the first 3 words that
#rhyme with jingle.

rhyme_json = request3.json()
for i in rhyme_json[0:3]:
    print(i['word'])

#Do checkout this awesome API, coupled with the concept of query parameters
#and the guidance of a very well written API documentation, you can make more
#complex get requests.


    #Sending SMS from Python
#Let's shift a couple of gear up and try a practical use case, wherein we can
#make use of the exceptional twilio API to send an SMS from your python
#program.

#If you thought that was cool, hold on, let's take it up a notch, let's try
#to get the number of people in space using Open Notify and then send it to a
#friend using Twilio.

#We start by importing the required modules (done above)

account_sid = 'Your_info_here'
auth_token = 'Your_info_here'

#These variables above, allow twilio to authenticate if the request is being
#sent by you, replace the string with our account sid and authentication token
#that was noted earlier.

client = Client(account_sid, auth_token)

#This step ensures that you are authenticated correctly.

r = requests.get('http://api.open-notify.org/astros.json')
people = r.json()
number_iss = people['number']
Message = 'Bruh...the number of people in space right now is '+str(number_iss)

#This is just a reiteration of what we did earlier wiht Open Notify, we make a
#request to /astros.json endpoint, and decode the json. As we know that the
#number of people can be retrieved by accessing the ['number'] key. We store
#this number and formulate a message for our friend.

message = client.messages.create(
    to='Your_Number',
    from_="Your_other_number",
    body=Message)

print(message.sid)

#Now comes the centerpiece of our assignment, formulation the message and
#sending it. In here to is the number which you would like to send a message to,
#and from_ is the number that you created inside of twilio (By default you can
#only send a message to your number without any problem, if you would like to
#send it to your friend verify the number in twilio). Replace the values
#correctly, and in this step we also indicate what the body of the message
#should contain, in our case the text from our variable Message: Number of
#people in space now.