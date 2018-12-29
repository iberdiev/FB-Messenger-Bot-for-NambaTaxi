# FB-Messenger-Bot-for-NambaTaxi
Facebook Messenger Bot that build on Django. Handles with quick taxi ordering.
## Running via Docker container
1. Go to root directory and build an image
```
docker build -t <image> . 
```
2. Run docker container
```
docker run -d -p 8000:8000 <image>
```
3. Browse http://127.0.0.1:8000/
