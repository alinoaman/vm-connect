pipeline {
    agent any

    environment {
        UBUNTU_IP = '13.126.209.98'  // Replace with your Ubuntu VM's IP
        ALMALINUX_IP = '13.127.245.214'  // Replace with your AlmaLinux VM's IP
        SSH_KEY = credentials('ubuntu-almalinux-ssh-key')  // Replace with your Jenkins credential ID for the PEM key
    }

    stages {
        stage('Fetch OS Information') {
            steps {
                script {
                    def ubuntuInfo = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ubuntu@${UBUNTU_IP} '
                        echo "OS: Ubuntu"
                        echo "Kernel: \$(uname -r)"
                        echo "Shell: \$SHELL"
                        echo "Package Manager: apt"
                        echo "Desktop Environment: \$XDG_CURRENT_DESKTOP"
                        '
                    """, returnStdout: true).trim()
                    
                    def almaLinuxInfo = sh(script: """
                        ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ec2-user@${ALMALINUX_IP} '
                        echo "OS: AlmaLinux"
                        echo "Kernel: \$(uname -r)"
                        echo "Shell: \$SHELL"
                        echo "Package Manager: dnf"
                        echo "Desktop Environment: \$XDG_CURRENT_DESKTOP"
                        '
                    """, returnStdout: true).trim()
                    
                    writeFile file: 'ubuntu_info.txt', text: ubuntuInfo
                    writeFile file: 'almalinux_info.txt', text: almaLinuxInfo
                    
                    def combinedInfo = "Ubuntu Information:\n${ubuntuInfo}\n\nAlmaLinux Information:\n${almaLinuxInfo}"
                    writeFile file: 'combined_info.txt', text: combinedInfo
                    
                    archiveArtifacts artifacts: '*.txt', fingerprint: true
                }
            }
        }
    }
}
