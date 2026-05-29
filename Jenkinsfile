pipeline {
    agent any

    environment {
        DOCKER_HUB = credentials('dockerhub-credentials')
        IMAGE_NAME = "seojieun/todo-api"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh "echo ${DOCKER_HUB_PSW} | docker login -u ${DOCKER_HUB_USR} --password-stdin"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Update K8s Manifest') {
            steps {
                sh """
                    sed -i 's|image: .*todo-api:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|' k8s/deployment.yaml
                """
            }
        }

        stage('Commit & Push Manifest') {
            steps {
                sh """
                    git config user.email "jenkins@ci.local"
                    git config user.name "Jenkins CI"
                    git add k8s/deployment.yaml
                    git commit -m "chore: update image tag to ${IMAGE_TAG}"
                    git push origin main
                """
            }
        }
    }

    post {
        always {
            sh "docker logout"
        }
    }
}
