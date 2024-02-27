pipeline {
    agent any
    stages {
        stage('Build and Push Image') {
            steps {
                script {
                    // Login to DockerHub and build the image with the linux/amd64 platform flag because this is building on my ARM64 machine
                    withDockerRegistry([ credentialsId: "docker-hub-creds", url: "https://index.docker.io/v2/" ]) {
                        docker.withServer('desktop-linux') {
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
            }
        }
        stage('Test') {
            steps {
                script {
                    // Placeholder for test commands
                    echo 'Running back-end tests...'
                    sh 'python manage.py test'
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
