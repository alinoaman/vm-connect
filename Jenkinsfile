pipeline {
    agent any

    environment {
        UBUNTU_IP = '3.110.136.138'
        UBUNTU_USERNAME = 'ubuntu'
        UBUNTU_KEYFILE = 'E:/KeyTask.pem'
        ALMALINUX_IP = '65.1.132.224'
        ALMALINUX_USERNAME = 'ec2-user'
        ALMALINUX_KEYFILE = 'E:/KeyTask.pem'
    }

    stages {
        stage('Update Ubuntu VM') {
            steps {
                script {
                    sh '''
                    ssh -i $UBUNTU_KEYFILE $UBUNTU_USERNAME@$UBUNTU_IP "sudo apt-get update && sudo apt-get upgrade -y"
                    '''
                }
            }
        }
        stage('Update AlmaLinux VM') {
            steps {
                script {
                    sh '''
                    ssh -i $ALMALINUX_KEYFILE $ALMALINUX_USERNAME@$ALMALINUX_IP "sudo dnf update -y"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'The update process has finished.'
        }
    }
}
