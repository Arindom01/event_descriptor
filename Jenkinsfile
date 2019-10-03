import groovy.io.*
import hudson.FilePath;
import jenkins.model.Jenkins;

node('serverless') {
        checkout scm

        stage('Unit Test') {
            sh "#!/bin/bash \n" + 
                "virtualenv -p python3.7 venv \n" + 
                "source venv/bin/activate \n" +
                "pip3 install -r requirements.txt --target ./packages \n" + 
                "pytest --capture=sys"
            
            
        }

        stage('Build') {
            echo 'Building..'
            sh "#!/bin/bash \n" + 
                "virtualenv -p python3.7 venv \n" + 
                "source venv/bin/activate \n" +
                "pip3 install -r requirements.txt --target ./packages \n"



            sh "npm install"
            sh "echo ${PATH}"
            sh "export PATH=/usr/bin/python3:${PATH}"
            sh "echo ${PATH}"
            sh "serverless package --package 'event_descriptor.zip' --stage 'dev' --account 100000000000"
            sh "zip -r 'event_descriptor.zip' event_descriptor"
        }


        stage('Deploy to Artifactory') {
          
        }

        stage('Deploy to AWS') {
          
        }

      }
}
