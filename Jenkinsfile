pipeline {
    agent any
    environment {
        // Fetching environment variables from Jenkins
        AZURE_CREDS = credentials('jenkins-azure-identity')
        // Fetching environment variables from Azure Key Vault
        MY_SECRET_KEY = credentials('MY-SECRET-KEY')
        TMDB_API_KEY = credentials('TMDB-API-KEY')
        GOOGLE_CLIENT_ID = credentials('GOOGLE-CLIENT-ID')
        GOOGLE_CLIENT_SECRET = credentials('GOOGLE-CLIENT-SECRET')
        DB_USER = credentials('DB-USER')
        DB_PASSWORD = credentials('DB-PASSWORD')
    }
    stages {
        stage('Build and Push Image') {
            steps {
                script {
                    // Login to DockerHub and build the image
                    withDockerRegistry([ credentialsId: "docker-hub-creds", url: "" ]) {
                        def app = docker.build("macleann/enchiridion-server")

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
        stage('Test') {
            steps {
                script {
                    // Placeholder for test commands
                    echo 'Running back-end tests...'
                    // Add test commands here
                }
            }
        }
        stage('Deploy to ACI') {
            steps {
                script {
                    // Azure CLI commands to deploy to ACI
                    withCredentials([azureServicePrincipal('jenkins-azure-identity')]) {
                        sh '''
                        az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID
                        az account set --subscription $AZURE_SUBSCRIPTION_ID
                        az container create --resource-group EnchiridionTV-Production \
                            --name enchiridion-server-${env.BUILD_NUMBER} \
                            --image macleann/enchiridion-server:${latestTag} \
                            --environment-variables \
                                MY_SECRET_KEY=${MY_SECRET_KEY} \
                                TMDB_API_KEY=${TMDB_API_KEY} \
                                GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID} \
                                GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET} \
                                DB_USER=${DB_USER} \
                                DB_PASSWORD=${DB_PASSWORD} \
                            --dns-name-label enchiridion-server-${env.BUILD_NUMBER} \
                            --ports 8000
                        az logout
                        '''
                    }
                }
            }
        }
    }
}
