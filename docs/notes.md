# Notes

## Self reflection

1. Does your solution solve the company’s pain points? What are they?
  - Yes, it does. The company has a problem with the manual deployment of the application. The solution automates the deployment process.
  - The company had no tracking of the experiments and models. The solution automates the tracking and registry of the models.
  - The company had no monitoring of the application. The solution proposes a solution.
  - The task had no CI/CD. The solution proposes a solution.
  - A frontend can be easily integrated with the API.
2. What tools did you use? Why did you select them?
  - MLFlow: to track and register the models. Centralizes all the experiments in one place.
  - FastAPI: to serve the model. It is fast and easy to use. Generate all the documents!
  - Pydantic: to validate the input data. It is easy to use and integrates well with FastAPI.
  - GCP: it is easier to setup than other cloud providers.
  - Github Actions: to automate the CI/CD. It is easy to use and integrates well with Github.
  - Docker: to containerize the application. It is easy to use and integrates well with Github Actions.
  - GCP Cloud Run: to deploy the application. It is easy to use and integrates well with Docker.
3. What model would you use for this use case? Why?
  - The candidate models did not perform well the task, but the selected one was the best. It has the highest F1-score, ROC AUC & Recall.
  - The model is not static. It can be updated with a new model that has better performance without the need to redeploy the application.
4. How does the API handle out-of-range or unknown (invalid) features?
  - Fails: the pydantic validation fails and returns a 422 error.
5. How does the API handle missing features?
  - Fails: the pydantic validation fails and returns a 422 error.


## Other

- Features: I ended up using all the categorical features and added the respective pydantic validation. In the future, I would like to use the numerical features as well.

- CI CD split into different files: I found this as a good practice to keep the procedures in different files. This way, it is easy to maintain and update the procedures.
  - But, there is a side-effect: the CD requires the CI to be run first and finish on success.
  - If there is any failure in CD it is impossible to make it work from a branch. I mean: if you modify the CD file in a branch, github will continue to run the version that is in the main branch.
  - That is the reason behind many pull requests that are just to fix the CD file. But, had no success and failed the CD.
  - And commiting directly in the main branch is not an option when it has protection rules.
- I had no idea that stress-test can be done automatically with locust library. This was a great learning indeed! Cheers!
