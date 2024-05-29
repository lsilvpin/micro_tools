pipeline {
    agent {
        label 'slave-platao'
    }
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
                sh 'bash ./test-is-up.sh platao 9000'
            }
        }
    }
}