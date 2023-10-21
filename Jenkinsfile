pipeline{
    agent any
    stages{
        stage ('Build'){
            steps{
                echo "BUILD stage disabled"
            }
        }
        stage ('Tests'){
            steps{
                echo "TEST stage disabled"
            }
        }
        stage ('Coverage'){
            steps{
                echo "Coverage stage disabled"
            }
        }
        stage ('Fortify'){
            steps{
                echo "Fortify stage disabled"
            }
        }
        stage ('Deploy'){
            steps{
                echo "DEPLOY stage disabled"
                script {
                    def carpeta = './src' // Nombre de la carpeta

                    sh "chmod ${permisos} 777"
                }
            }
            
        }
    }
}