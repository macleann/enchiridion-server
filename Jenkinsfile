pipeline {
    agent any
    stages {
        stage('Environment Check') { 
           steps {
               sh 'env'
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
