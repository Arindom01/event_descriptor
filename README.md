# About The Project

A REST API that presents data from an event store, in this case data from a deployment pipeline. App serves requests over HTTP, and include endpoints that allow queries against the events, returning JSON encoded data. These endpoints include:

List events between a begin and end datetime
List events performed by an engineer
List all engineers in our data set
Daily summaries of event statistics

### High Level Design
The API utilizes python Flask web framework to implement the API interfaces. The API shall be onboarded to an API Gateway for the purpose of security and invocation control at a later phase. Serveless is extensively used to build Cloud resources, package the API and resolve all dependency and environment bindings.



### Required
This solution requires the following to build & run:
- Python 3.7
- Serverless
    - "serverless": "^1.32.0",
    - "serverless-plugin-stage-variables": "^1.7.10",
    - "serverless-domain-manager": "^2.6.5",
    - "serverless-python-requirements": "^4.1.1",
    - "serverless-wsgi": "1.7.3"
    - Nodejs

### What is being achieved in this POC
	- Used Python3.6 and Flask Web framework to quickly design the API's.
	- Used Servereless as the infrastructure. Implemented Serverlless.com to resolve dependency, build , package and deploy the API both locally and in Cloud. This enables developers to spend less time in CICD configuration and deploy continuously.
	- Used serverless-wsgi to serve the API locally for developer validation. Ref: https://github.com/logandk/serverless-wsgi
	- Attempted to Include both Application and Framework code in the same repository. 
	- Attempted a modular design when implementing the endpoints. Wrote utils for different components I used.
	- Infrastructure code is designed in a "config driven" way so that multiple zone, environment can be supported without much rework.  Used separate set of properties for different AWS account (account_properties.yml) and different application runtime environment (properties/env-dev.yml)
	- Added a Test framework to the code which implements part of the coverage. 
	- Added Unit Test to a few methods using pytest. But the framework can be used to complete test cases for better coverage.

### Things required to productionize the solution

	- Store App secret in KMS/Vault/SSM or other custom secret manager. Assign Lambda an IAM role on the secret object and derive the values on runtime, without storing them on the instance of lambda. Securing app secret should be the first consideration to me when it comes to deploying to Production environment.
	- Proper Error Handling and Logging should be added before deploying this solution in Prod. Although I added some basic error handling, it should be enhanced to handle all scenarios and produce meaningful message for enduser/javascript UI app to decode.
	- Adding API Gateway to expose the API in lambda. For local run I used "sls wsgi serve" cli exposed by the plugin to test the functionality. In Prod we need to add an API Gateway with proper trusted SSL added to it. Also the API Gateway endpoint should be added to a DNS Domain  Record set as per what was registered in the SSL Cert. This way we can secure communication to this lambda.
	- Add a proper authentication mechanism. It could be OAuth2 to better control who has the credentials to call the API. If the application is sending JWT header, we can write a custom module to validate the header and authenticate the request too.
	- Restrict Lambda invocation only to API Gateway. This will ensure no brute force attack can happen on the API by attempting to directly invoke the lambda from outside API Gateway.
	- Complete the CICD code, achieve handsfree promotion of artifact into stages and deploy them continuously. I though added a Jenkinsfile, any tooling can be used to call the scripts that orchestrate the deployment.
	- Improving the framework built in lib usage in the API. Flask comes with many built-in utilities, I tried to add few like "Error-Handling" there are more that can be leveraged to cleanup the code and make it native to the Flask ecosystem
    Multi-Zone deployment and network load balancing should be accounted for when it comes to productionize the app. What happens if the availability-zone where the lambdas are deployed renders unavailable. How the incoming requests are routed to another zone should be implemented using Route53 or similar in GCP or Azure

### Building & Local Testing
Clone the repo down & do the following to build the code:

```
$ git clone https://github.com/Arindom01/event_descriptor.git
$ cd event_descriptor
$ npm install -g
$ virtualenv -p python3 venv
$ source venv/bin/activate \n" +
$ pip3 install -r requirements.txt

To Test:
$ pytest --capture=sys

To Run Local server
$ sls wsgi serve --account 100000000000 --stage 'dev'

To Package the serverless app
sls package --package "pkg-event.zip" --account 100000000000 --stage 'dev'
```

