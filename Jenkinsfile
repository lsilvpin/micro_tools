pipeline {
    agent any
    stages {
        stage ('Build') {
            steps {
                sh 'bash ./docker-build.sh'
            }
        }
        stage ('Run') {
            steps {
                sh 'bash ./docker-run.sh'
            }
        }
        stage ('Test') {
            steps {
                sh 'bash ./test-is-up.sh'
            }
        }
    }
}