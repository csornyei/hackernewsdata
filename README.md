# HackerNews Data Aggregator

This is my solution for the HackerNews data aggregator assignment. I used FastAPI to create a REST API.

## Starting

You can start the application with Docker. The application will be available at http://localhost:8000.

```bash
docker build -t hackernewsapi .
docker run -p 8000:8000 hackernewsapi
```

## Endpoints

- `/top-stories`: Returns the first 50 comments of the first 100 top stories. The amount of stories can be changed with the `story-count` query parameter.
- `/most-used-words`: Returns the 10 most used words for the first 100 comments of the top 30 stories. The amount of stories can be changed with the `story-count` query parameter. The amount of most used words can be changed with the `word-count` query parameter. If `word-count` is set to `all` all words will be returned.
- `/most-used-words-all`: Returns the 10 most used words for the first 10 stories. It also includes nested comments. The amount of stories can be changed with the `story-count` query parameter. The amount of most used words can be changed with the `word-count` query parameter. If `word-count` is set to `all` all words will be returned.

## Questions

### What has been the more difficult part?

The most difficult part was me is the amount of requests I need to send to get all the data. Because of this the application was very slow. I used the `ThreadPoolExecutor` to speed up the process and send the requests in parallel. This gave significant performance improvements, however implementing it with the recursive function turned out to more complex than I thought.

### What part of the system could be improved?

The performance of the application could be improved. I think the recursive function could be improved. I think I should've used some external library for sending the requests asynchronously instead of using the `ThreadPoolExecutor`. That could've made the code less complex and easier to read and implement. 

### How would you scale it, to be able to handle 1K calls per sec? and to handle 1M?

First thing I would add is some caching mechanism. I would cache the results of the requests for a certain amount of time. This would reduce the amount of requests to the HackerNews API. I would also add some kind of rate limiting to prevent the application from being overloaded. I think the application could be scaled by using a load balancer and multiple instances of the application. The load balancer would distribute the requests over the instances.

### How would you automate the testing?

I would create mock responses for each called endpoint and write unit tests for the API functions. I provided some unit tests for the utilities functions. Finally with the mock data I would create some integration tests for the API endpoints as well.

### How would you implement a continuous development system (pipelines) for this particular case?

I would create a pipeline that runs the tests and build a docker image for the application. The pipeline finally deploy the docker image for a test environment. If acceptance test is done on the test environment I would promote the docker image to deploy it to production environment.
However, I wouldn't choose this case to use in production. As each endpoint is blocking the server for longer time I would separate them into multiple serverless functions and provide the endpoint for those. This way all three endpoint could be used at the same time without blocking each other. 