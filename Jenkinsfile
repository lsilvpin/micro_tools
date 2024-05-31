pipeline {
    agent {
        label 'slave-platao'
    }
    stages {
        stage ('Build in docker') {
            steps {
                sh 'bash ./docker-build.sh'
            }
        }
        stage ('Deploy in Docker') {
            steps {
                sh 'bash ./deploy-docker.sh'
            }
        }
        stage ('Deploy in kubernetes') {
            steps {
                sh 'bash ./deploy-kubernetes.sh'
            }
        }
        stage ('Test') {
            steps {
                sh 'bash ./test-is-up.sh'
            }
        }
    }
}