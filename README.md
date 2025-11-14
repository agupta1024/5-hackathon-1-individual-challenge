[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/xHqCZWar)
# Hackathon #1
Welcome to your first hackathon of Machine Learning System Design!
This hackathon is designed to test your knowledge on the topics covered so far in the course: data acquisition, APIs, data storage, object models, and basic statistics.

## Brief:
Consider the empirical distribution represented by the number of stargazers (stars) in each repository in the organisation, https://github.com/google.

Your task is to **build a server** whose endpoints distribute the following information, with the following API specification.
All responses should be returned in JSON format.

> [!NOTE]
> You have 2 hours to complete this hackathon.


## API specification
`GET /healthz` - returns a simple health check message.
Example response:
```json
{
  "status": "healthy"
}
```
`GET {org}/stars` - returns a set of key-value pairs containing the number of stargazers for each repository in the organisation.
Example response:
```json
{
  "repo1": 123,
  "repo2": 456,
  "repo3": 789
}
```
`GET {org}/avg` - returns the average number of stargazers per repository.
Example response:
```json
{
  "average": 1234.56
}
```
`GET {org}/std` - returns the standard deviation of the number of stargazers.
Example response:
```json
{
  "std": 234.56
}
```
`GET {org}/min` - returns the minimum number of stargazers for a repository.
Example response:
```json
{
  "min": 12
}
```
`GET {org}/max` - returns the maximum number of stargazers.
Example response:
```json
{
  "max": 34567
}
```
`GET {org}/argmin` - returns the name of the repository with the minimum number of stargazers.
Example response:
```json
{
  "argmin": "example-repo-name"
}
```
`GET {org}/argmax` - returns the name of the repository with the maximum number of stargazers.
Example response:
```json
{
  "argmax": "example-repo-name"
}
```
where `{org}` is a path parameter representing the GitHub organisation name (e.g., `google`).


## Scoring

> [!CAUTION]
> Make sure you run your server on port **8000**!

Your work will be autograded using the following commands:
```bash
conda env create -f environment.yml -n daps-hackathon-1  # install env
conda activate daps-hackathon-1 # activate env
pip install -r requirements.txt # install dependencies
python main.py # spawn the server
```


Scores will be assigned based on the following criteria:
| Criterion                             | Weight | Details                                                                                                        |
| ------------------------------------- | -----: | -------------------------------------------------------------------------------------------------------------- |
| Correct endpoints for `google` org    |    40% | 5% per endpoint.                                                                                               |
| Generalise to any GitHub organisation |    20% | Implementation should work for organisations beyond just `google`.                                             |
| Caching                               |    10% | Making the same request twice should perform at least 50% faster the second time.                              |
| Error handling                        |    10% | Return appropriate HTTP status codes and messages (e.g., **400** for bad requests, **500** for server errors). |
| Code quality                          |    20% | Score = 2.0 × pylint score (out of 10)                                                                         |



> [!TIP]
> Consider splitting your work in three major subtasks:
> 1. **Data acquisition/Storage**: fetching the data from the GitHub API and storing it in a database.
> 2. **Data processing/Backend**: computing the required statistics from the stored data.
> 3. **API/Frontend**: building the server and implementing the endpoints.
> 5. ...
> 4. Error handling?
> 5. Caching?
> 6. ...?
