pipeline {
    agent any

    environment {
        UBUNTU_IP = '3.110.103.168'
        UBUNTU_USERNAME = 'ubuntu'
        ALMALINUX_IP = '13.127.249.159'
        ALMALINUX_USERNAME = 'ec2-user'
        WINDOWS_IP = '43.204.29.229'
        WINDOWS_USERNAME = 'Administrator'
        SSH_KEY = credentials('ubuntu-almalinux-ssh-key')
        WINDOWS_PASSWORD = credentials('windows-password')
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
                    report += "Output: ${almaLinuxOutput}\n\n"
                    
                    // Update Windows 11
                    def windowsExitCode = sh(script: """
                        ssh -o StrictHostKeyChecking=no ${WINDOWS_USERNAME}@${WINDOWS_IP} powershell -Command "
                        Install-Module PSWindowsUpdate -Force
                        Get-WindowsUpdate -Install -AcceptAll -AutoReboot
                        "
                    """, returnStatus: true)
                    
                    report += "Windows11: ${windowsExitCode == 0 ? 'Success' : 'Failure'}\n"
                    if (windowsExitCode != 0) {
                        report += "Error: Max retries reached. Unable to connect.\n\n"
                    }
                    
                    // Write report to file
                    writeFile file: 'Text_report.txt', text: report
                    archiveArtifacts artifacts: 'Text_report.txt', fingerprint: true
                }
            }
        }
    }
}
