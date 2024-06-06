# Coworking Space Service Extension
The Coworking Space Service is a set of APIs that enables users to request one-time tokens and administrators to authorize access to a coworking space. This service follows a microservice pattern and the APIs are split into distinct services that can be deployed and managed independently of one another.

For this project, you are a DevOps engineer who will be collaborating with a team that is building an API for business analysts. The API provides business analysts basic analytics data on user activity in the service. The application they provide you functions as expected locally and you are expected to help build a pipeline to deploy it in Kubernetes.

## Getting Started

### Dependencies
#### Local Environment
1. Python Environment - run Python 3.6+ applications and install Python dependencies via `pip`
2. Docker CLI - build and run Docker images locally
3. `kubectl` - run commands against a Kubernetes cluster
4. `helm` - apply Helm Charts to a Kubernetes cluster

#### Remote Resources
1. AWS CodeBuild - build Docker images remotely
2. AWS ECR - host Docker images
3. Kubernetes Environment with AWS EKS - run applications in k8s
4. AWS CloudWatch - monitor activity and logs in EKS
5. GitHub - pull and clone code

### Setup
#### 1. Configure a Database
Set up a Postgres database using a Helm Chart.

1. Set up Bitnami Repo
```bash
helm repo add <REPO_NAME> https://charts.bitnami.com/bitnami
```

2. Install PostgreSQL Helm Chart
```
helm install <SERVICE_NAME> <REPO_NAME>/postgresql
```

This should set up a Postgre deployment at `<SERVICE_NAME>-postgresql.default.svc.cluster.local` in your Kubernetes cluster. You can verify it by running `kubectl svc`

By default, it will create a username `postgres`. The password can be retrieved with the following command:
```bash
export POSTGRES_PASSWORD=$(kubectl get secret --namespace default <SERVICE_NAME>-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

echo $POSTGRES_PASSWORD
```

<sup><sub>* The instructions are adapted from [Bitnami's PostgreSQL Helm Chart](https://artifacthub.io/packages/helm/bitnami/postgresql).</sub></sup>

3. Test Database Connection
The database is accessible within the cluster. This means that when you will have some issues connecting to it via your local environment. You can either connect to a pod that has access to the cluster _or_ connect remotely via [`Port Forwarding`](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)

* Connecting Via Port Forwarding
```bash
kubectl port-forward --namespace default svc/<SERVICE_NAME>-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432
```

* Connecting Via a Pod
```bash
kubectl exec -it <POD_NAME> bash
PGPASSWORD="<PASSWORD HERE>" psql postgres://postgres@<SERVICE_NAME>:5432/postgres -c <COMMAND_HERE>
```

4. Run Seed Files
We will need to run the seed files in `db/` in order to create the tables and populate them with data.

```bash
kubectl port-forward --namespace default svc/<SERVICE_NAME>-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432 < <FILE_NAME.sql>
```

### 2. Running the Analytics Application Locally
In the `analytics/` directory:

1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Run the application (see below regarding environment variables)
```bash
<ENV_VARS> python app.py
```

There are multiple ways to set environment variables in a command. They can be set per session by running `export KEY=VAL` in the command line or they can be prepended into your command.

* `DB_USERNAME`
* `DB_PASSWORD`
* `DB_HOST` (defaults to `127.0.0.1`)
* `DB_PORT` (defaults to `5432`)
* `DB_NAME` (defaults to `postgres`)

If we set the environment variables by prepending them, it would look like the following:
```bash
DB_USERNAME=username_here DB_PASSWORD=password_here python app.py
```
The benefit here is that it's explicitly set. However, note that the `DB_PASSWORD` value is now recorded in the session's history in plaintext. There are several ways to work around this including setting environment variables in a file and sourcing them in a terminal session.

3. Verifying The Application
* Generate report for check-ins grouped by dates
`curl <BASE_URL>/api/reports/daily_usage`

* Generate report for check-ins grouped by users
`curl <BASE_URL>/api/reports/user_visits`

## Project Instructions
1. Set up a Postgres database with a Helm Chart
2. Create a `Dockerfile` for the Python application. Use a base image that is Python-based.
3. Write a simple build pipeline with AWS CodeBuild to build and push a Docker image into AWS ECR
4. Create a service and deployment using Kubernetes configuration files to deploy the application
5. Check AWS CloudWatch for application logs

### Deliverables
1. `Dockerfile`
2. Screenshot of AWS CodeBuild pipeline
3. Screenshot of AWS ECR repository for the application's repository
4. Screenshot of `kubectl get svc`
5. Screenshot of `kubectl get pods`
6. Screenshot of `kubectl describe svc <DATABASE_SERVICE_NAME>`
7. Screenshot of `kubectl describe deployment <SERVICE_NAME>`
8. All Kubernetes config files used for deployment (ie YAML files)
9. Screenshot of AWS CloudWatch logs for the application
10. `README.md` file in your solution that serves as documentation for your user to detail how your deployment process works and how the user can deploy changes. The details should not simply rehash what you have done on a step by step basis. Instead, it should help an experienced software developer understand the technologies and tools in the build and deploy process as well as provide them insight into how they would release new builds.


### Stand Out Suggestions
Please provide up to 3 sentences for each suggestion. Additional content in your submission from the standout suggestions do _not_ impact the length of your total submission.
1. Specify reasonable Memory and CPU allocation in the Kubernetes deployment configuration
2. In your README, specify what AWS instance type would be best used for the application? Why?
3. In your README, provide your thoughts on how we can save on costs?

### Best Practices
* Dockerfile uses an appropriate base image for the application being deployed. Complex commands in the Dockerfile include a comment describing what it is doing.
* The Docker images use semantic versioning with three numbers separated by dots, e.g. `1.2.1` and  versioning is visible in the  screenshot. See [Semantic Versioning](https://semver.org/) for more details.

### Read me

### Steps to archive

# - Requirement
#   1/ Install the kubectl
#   2/ 

# 0 Pre-conditions
# - Build your own a docker image
#   1/ In this practice, i'm using python as an api service.
#   2/ In the folder 'analytics' create a dockerfile: 
#       The file it has the steps that needed to be done in order to run the code correctly such as: libraries, folder build, etc...
#       The command is be executed on the first run of the app.

# - Create a ECR repository
#   1/ Go to AWS Console, choose the service named "ECR" - "Elastic Container Repository".
#   2/ Choose the visibility of the repository, Private or Public.
#   3/ Name the repository.

# - Using codebuild for building the docker image and storing in ECR
#   1/ After the ECR created, you will need to create your owns of buildspec.yaml
#       This file is for telling the codebuild how to build your docker image from your local to aws and store in ECR.
#       You should focus on this variables such as:  
#               $AWS_DEFAULT_REGION, this one mean, where is your ECR? ex: us-east-1
#               $IMAGE_REPO_NAME:$IMAGE_TAG, this is the main docker you have built, Note: remember the path relative of the buildspec.yaml with #                docker file
#   2/ Now go to AWS console, created a codebuild
#       We're using github as a version control of the code we're using. Note: please remember auth the codebuild for accessing your github #       repository
#       We config the service, remember to put some environment variables (we defined in buildspec.yml)
#           $AWS_DEFAULT_REGION = us-east-1
#           $AWS_ACCOUNT_ID = the account you get in the right corner of the aws console.
#           $IMAGE_REPO_NAME = the name you defined in ECR
#           $IMAGE_TAG = latest
#       We can config the auto build base on pushing code or pull requests
#       Telling the codebuild to look for the file named "buildspec.yaml", the file should be located in side the root folder.

# 1 You need to have an EKS cluster
#   1/ Now you have the image of the api service we're going to use.
#       - Create your EKS (Elastic Kubernetes services)
#       - We're using the command like this one: 
#       ./eksctl create cluster --name {YOUR NAME}-cluster --region us-east-1 --nodegroup-name {YOUR NAME}-nodegroup --node-type t3.small --nodes 1 #           --nodes-min 1 --nodes-max 2 
#       - aws eks --region us-east-1 update-kubeconfig --name {YOUR NAME}-cluster
#       - kubectl config current-context
#       - kubectl config view
#   2/ Now you need to deploy your database
#       - In the folder 'database-local', we need to deploy this order
#           Step 1, kubectl apply -f pv.yaml / This one is for creating the storing location, type of storage
#           Step 2, kubectl apply -f pvc.yaml
#           Step 3, kubectl apply -f secret.yaml / This one helps us to store some private datas
#           Step 4, kubectl apply -f deployment.yaml / This is the main one.
#       - For accessing the database we're using the port-forward
#           Step 1, kubectl apply -f postgresql-service.yaml / This one for installing port forward
#           Step 2, Start-Process -NoNewWindow kubectl -ArgumentList "port-forward service/{YOUR}-postgresql-service 5433:5432" -PassThru (For #                     Windows)
#           Step 3, we're using pdAdmin tool for connecting the database and insert/edit data.
#   3/ Now you need to deploy your api service
#       -   kubectl apply -f secret.yaml (if you already installed it, you can skip this step).
#       -   kubectl apply -f config.yaml
#       -   kubectl apply -f coworking.yaml (the main one, get docer image That you created before).

# 2 Configue
# - In order to automate the process, we're using codepipeline.
#       This one is for the puspose such as:
#       When you push new codes to the github repository, it will be triggered and start to build the code in codebuild.
#       After code is done, the pipeline will deploy to the service you want (EKS may be, etc...)
#       So that, you can continue to deploy codes anytime you want.
# - For applying the configures. 
#       You can edit the yaml as you need, then using the command: kubectl apply -f {file_name}.yaml