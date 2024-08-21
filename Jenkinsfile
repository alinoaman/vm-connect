pipeline {
    agent any

    environment {
        UBUNTU_IP = '13.126.209.98'
        UBUNTU_USERNAME = 'ubuntu'
        ALMALINUX_IP = '13.127.245.214'
        ALMALINUX_USERNAME = 'ec2-user'
        WINDOWS_IP = '13.234.117.122'  // Replace with actual Windows 11 IP
        WINDOWS_USERNAME = 'Administrator'  // Replace with actual Windows username
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
                    def windowsExitCode = bat(script: """
                        powershell -Command "
                        \$secpasswd = ConvertTo-SecureString '${WINDOWS_PASSWORD}' -AsPlainText -Force
                        \$cred = New-Object System.Management.Automation.PSCredential ('${WINDOWS_USERNAME}', \$secpasswd)
                        Invoke-Command -ComputerName ${WINDOWS_IP} -Credential \$cred -ScriptBlock {
                            Install-Module PSWindowsUpdate -Force
                            Get-WindowsUpdate -Install -AcceptAll -AutoReboot
                        }"
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
