pipeline {
    environment {
     boolean CLONE_REPO_ON_REMOTE = true
     DEPLOYMENT_SERVER = "gipsbrian@134.209.69.5"
    }
    
    agent any

    stages {
        stage('Initializing ibl-request-router pipeline.....') {
            steps {
                echo 'Cloning and deploying repo.......'
            }
        }
        stage('Clone ibl-request-router rep to the remote server.....') {
           steps {
                sshagent(['sshkey-gips-dev-server-1','sshkey-sandbox-1']) {
                    //make ibl-jenkins-deployment-scripts dir on remote host
                    catchError(message: 'Repo already exists on the remote server') {
                        // try and clone the repo
                        sh '''
                            ssh -t -t ${DEPLOYMENT_SERVER} -o StrictHostKeyChecking=no "cd \\$(tutor config printroot)/env/build/openedx/requirements/ibl-request-router; 
                            git pull origin koa-tutor-plugin; 
                            ls -l"
                        '''
                        script {CLONE_REPO_ON_REMOTE = false}
                    }
                    catchError(message: 'Repo does not exists on the remote server') {
                        script {
                            if(!CLONE_REPO_ON_REMOTE){
                                sh '''
                                    ssh -t -t ${DEPLOYMENT_SERVER} -o StrictHostKeyChecking=no "cd \\$(tutor config printroot)/env/build/openedx/requirements;
                                    git clone -b koa-tutor-plugin git@gitlab.com:deeplms/ibl-request-router.git; 
                                    ls -l"
                                 '''
                            }else{
                                echo 'Repo already exists on the remote host........'
                            }
                        }
                    }                       
                }
            } 
        }
        
    }
}