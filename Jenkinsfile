pipeline {
    agent any
    environment {
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
                    // Login to Azure using Managed Identity
                    sh 'az login --identity'

                    // Delete old container if it exists
                    sh 'az container delete --name enchiridion-server --resource-group EnchiridionTV-Production || true'

                    // Deploy to ACI
                    sh '''
                    az container create --resource-group EnchiridionTV-Production \
                        --name enchiridion-server \
                        --image macleann/enchiridion-server:latest \
                        --environment-variables \
                            MY_SECRET_KEY=$MY_SECRET_KEY \
                            TMDB_API_KEY=$TMDB_API_KEY \
                            GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
                            GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET \
                            DB_USER=$DB_USER \
                            DB_PASSWORD=$DB_PASSWORD \
                        --dns-name-label enchiridion-server \
                        --ports 8000
                    '''

                    // Obtain the public IP address of the newly created container
                    sh '''
                    BACKEND_CONTAINER_IP=$(az container show --resource-group EnchiridionTV-Production \
                        --name enchiridion-server \
                        --query ipAddress.ip \
                        --output tsv)
                    '''

                    // Obtain the public IP address of the front-end container
                    sh '''
                    FRONTEND_CONTAINER_IP=$(az container show --resource-group EnchiridionTV-Production \
                        --name enchiridion-client \
                        --query ipAddress.ip \
                        --output tsv)
                    || true
                    '''

                    // Log out from Azure CLI
                    sh 'az logout'

                    // Update Nginx configuration with the new IP addresses
                    sh '''
                    cp /etc/nginx/sites-available/default.template /etc/nginx/sites-available/default
                    sed -i "s/FRONTEND_CONTAINER_IP/${FRONTEND_CONTAINER_IP}/g" /etc/nginx/sites-available/default
                    sed -i "s/BACKEND_CONTAINER_IP/${BACKEND_CONTAINER_IP}/g" /etc/nginx/sites-available/default
                    sudo systemctl restart nginx
                    '''
                }
            }
        }
    }
}
