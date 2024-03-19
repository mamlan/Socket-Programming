## how to test code
Assuming python is installed, the participant must run both the webserver and proxyserver files. This can be done in various
ways such as "python webserver.py" for example in the terminal.

No external files were used except for the socket file. 

The servers correctly work for all test cases provided by the professor as well as google.com and bing.com.

### it must be noted that when testing a specific url, it is important to leave out the 'http://www.' from the header. For example, say we wanted to access google.com. 

### doing a simple "localhost:8000/google.com" would retrieve the page instead of "localhost:8000/http://www.google.com"