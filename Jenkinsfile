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
        stage ('Deploy') {
            steps {
                sh 'bash ./deploy.sh'
            }
        }
        stage ('Test') {
            steps {
                sh 'bash ./test-is-up.sh'
            }
        }
    }
}