pipeline {
    agent any
    environment {
        DB_HOST = credentials('LOCAL_DB_HOST')
        DB_NAME = credentials('LOCAL_DB_NAME')
    }
    stages {
        stage('Build and Push Image') {
            steps {
                script {
                    // Login to DockerHub
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh 'docker login -u $USERNAME -p $PASSWORD'
                    }

                    // Build the image with the linux/amd64 platform flag
                    def app = docker.build("macleann/enchiridion-server", "--platform linux/amd64 .")

                    // Tagging with build number and 'latest'
                    def versionTag = "v${env.BUILD_NUMBER}"
                    def latestTag = "latest"

                    app.tag(versionTag)
                    app.tag(latestTag)

                    // Push both tags to DockerHub
                    app.push(versionTag)
                    app.push(latestTag)
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Placeholder for test commands
                    azureKeyVault([[envVariable: 'CLIENT_URL', name: 'CLIENT-URL', secretType: 'Secret'], [envVariable: 'DB_ENGINE', name: 'DB-ENGINE', secretType: 'Secret'], [envVariable: 'DB_PASSWORD', name: 'DB-PASSWORD', secretType: 'Secret'], [envVariable: 'DB_PORT', name: 'DB-PORT', secretType: 'Secret'], [envVariable: 'DB_USER', name: 'DB-USER', secretType: 'Secret'], [envVariable: 'GOOGLE_CLIENT_ID', name: 'GOOGLE-CLIENT-ID', secretType: 'Secret'], [envVariable: 'GOOGLE_CLIENT_SECRET', name: 'GOOGLE-CLIENT-SECRET', secretType: 'Secret'], [envVariable: 'MY_SECRET_KEY', name: 'MY-SECRET-KEY', secretType: 'Secret'], [envVariable: 'TMDB_API_KEY', name: 'TMDB-API-KEY', secretType: 'Secret'], [envVariable: 'WWW_CLIENT_URL', name: 'WWW-CLIENT-URL', secretType: 'Secret']]) {
                        echo 'Running back-end tests...'
                        sh 'pipenv install'
                        sh 'pipenv run python manage.py test'
                    }
                }
            }
        }
        stage('Deploy to Azure') {
            steps {
                echo 'Logging into Azure'
                withCredentials([azureServicePrincipal('azure-creds')]){
                    sh 'az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID'
                }

                // Restarting the web app to pull the latest image
                echo 'Deploying to Azure'
                sh 'az webapp restart --name enchiridion-api --resource-group enchiridion-prod'
                
                echo 'Logging out'
                sh 'az logout'
            }
        }
    }
}

