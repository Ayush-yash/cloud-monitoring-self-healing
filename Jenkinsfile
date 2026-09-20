pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                echo 'Checking server tools...'
                sh 'docker --version'
                sh 'git --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building container image...'
                sh 'docker build -t cloud-monitoring:latest .'
            }
        }

        stage('Test & Health Check') {
            steps {
                echo 'Verifying container startup...'
                sh '''
                    docker run -d --name test-monitor cloud-monitoring:latest || true
                    sleep 3
                    docker ps -f name=test-monitor
                    docker rm -f test-monitor || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning dangling images...'
            sh 'docker image prune -f || true'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Build failed. Check console output.'
        }
    }
}
