pipeline {
    agent any
    
    environment {
        WINDOWS_IP = '35.154.183.221'
        WINDOWS_USERNAME = 'Administrator'
        WINDOWS_PASSWORD = 'H$=oTOr(ynBgdiO$fkfn&M%VM5)PG9ru'
        UBUNTU_IP = '3.110.158.205'
        UBUNTU_USERNAME = 'ubuntu'
        UBUNTU_KEYFILE = 'E:/KeyTask.pem'
        ALMALINUX_IP = '15.206.117.176'
        ALMALINUX_USERNAME = 'ec2-user'
        ALMALINUX_KEYFILE = 'E:/KeyTask.pem'
    }
    
    stages {
        stage('Update Windows VM') {
            steps {
                script {
                    sh '''
                    sshpass -p "$WINDOWS_PASSWORD" ssh $WINDOWS_USERNAME@$WINDOWS_IP "powershell.exe 'Get-WindowsUpdate -Install -AcceptAll -AutoReboot'"
                    '''
                }
            }
        }
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
