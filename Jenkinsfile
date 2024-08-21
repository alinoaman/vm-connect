pipeline {
    agent any

    environment {
        UBUNTU_IP = '65.2.80.117'
        UBUNTU_USERNAME = 'ubuntu'
        ALMALINUX_IP = '3.109.152.1'
        ALMALINUX_USERNAME = 'ec2-user'
        SSH_KEY = credentials('ubuntu-almalinux-ssh-key')
    }

    stages {
        stage('Update Machines') {
            steps {
                script {
                    def report = "Update Report - ${new Date().format('yyyy-MM-dd HH:mm:ss')}\n\n"
                    
                    // Update Ubuntu
                    def ubuntuResult = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${UBUNTU_USERNAME}@${UBUNTU_IP} '
                        sudo DEBIAN_FRONTEND=noninteractive apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
                        '
                    """, returnStatus: true, returnStdout: true)
                    
                    report += "Ubuntu-server: ${ubuntuResult.status == 0 ? 'Success' : 'Failure'}\n"
                    report += "Output: ${ubuntuResult.stdout}\n"
                    report += "Error: ${ubuntuResult.stderr}\n\n"
                    
                    // Update AlmaLinux
                    def almaLinuxResult = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${ALMALINUX_USERNAME}@${ALMALINUX_IP} '
                        sudo dnf update -y
                        '
                    """, returnStatus: true, returnStdout: true)
                    
                    report += "AlmaLinux9: ${almaLinuxResult.status == 0 ? 'Success' : 'Failure'}\n"
                    report += "Output: ${almaLinuxResult.stdout}\n"
                    report += "Error: ${almaLinuxResult.stderr}\n"
                    
                    // Write report to file
                    writeFile file: 'Text_report.txt', text: report
                    archiveArtifacts artifacts: 'Text_report.txt', fingerprint: true
                }
            }
        }
    }
}
