pipeline {
    agent any

    environment {
        UBUNTU_IP = '13.126.209.98'
        UBUNTU_USERNAME = 'ubuntu'
        ALMALINUX_IP = '13.127.245.214'
        ALMALINUX_USERNAME = 'ec2-user'
        SSH_KEY = credentials('ubuntu-almalinux-ssh-key')
    }

    stages {
        stage('Update Machines') {
            steps {
                script {
                    def report = "Update Report - ${new Date().format('yyyy-MM-dd HH:mm:ss')}\n\n"
                    
                    // Update Ubuntu
                    def ubuntuExitCode = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${UBUNTU_USERNAME}@${UBUNTU_IP} '
                        sudo DEBIAN_FRONTEND=noninteractive apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
                        '
                    """, returnStatus: true)
                    
                    def ubuntuOutput = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${UBUNTU_USERNAME}@${UBUNTU_IP} '
                        sudo DEBIAN_FRONTEND=noninteractive apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
                        '
                    """, returnStdout: true).trim()
                    
                    report += "Ubuntu-server: ${ubuntuExitCode == 0 ? 'Success' : 'Failure'}\n"
                    report += "Output: ${ubuntuOutput}\n\n"
                    
                    // Update AlmaLinux
                    def almaLinuxExitCode = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${ALMALINUX_USERNAME}@${ALMALINUX_IP} '
                        sudo dnf update -y
                        '
                    """, returnStatus: true)
                    
                    def almaLinuxOutput = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${ALMALINUX_USERNAME}@${ALMALINUX_IP} '
                        sudo dnf update -y
                        '
                    """, returnStdout: true).trim()
                    
                    report += "AlmaLinux9: ${almaLinuxExitCode == 0 ? 'Success' : 'Failure'}\n"
                    report += "Output: ${almaLinuxOutput}\n"
                    
                    // Write report to file
                    writeFile file: 'Text_report.txt', text: report
                    archiveArtifacts artifacts: 'Text_report.txt', fingerprint: true
                }
            }
        }
    }
}
