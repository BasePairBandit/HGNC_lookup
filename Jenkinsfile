pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t hgnc_lookup:test .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm hgnc_lookup:test pytest hgnc_lookup_app/tests/'
            }
        }
    }
}
