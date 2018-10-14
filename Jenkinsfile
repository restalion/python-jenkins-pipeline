#!groovy

pipeline {
    agent {
        docker {
            image 'python-jenkins-docker:0.2'
        }
    }

    stages {
        stage('Compile') {
            steps {
                echo "-=- compiling project -=-"
                sh "python3 --version"
                sh "python3 -m compileall ."
            }
        }

        stage('Unit tests') {
            steps {
                echo "-=- execute unit tests -=-"
                sh "python3 -m unittest discover -v"
                //sh "mvn test"
                //junit 'target/surefire-reports/*.xml'
                //jacoco execPattern: 'target/jacoco.exec'
            }
        }

        stage('Mutation tests') {
            steps {
                echo "-=- execute mutation tests -=-"
                // initialize mutation testing session
                sh "cosmic-ray init config.yml my_session"
                // execute mutation tests
                sh "cosmic-ray exec my_session"
                // get mutation test results
                sh "cosmic-ray dump  my_session | cr-report"    
            }
        }

        stage('Package') {
            steps {
                echo "-=- packaging project -=-"
                //sh "mvn package -DskipUTs=true"
                //archiveArtifacts artifacts: 'target/*.war', fingerprint: true
            }
        }

        stage('Build Docker image') {
            steps {
                echo "-=- build Docker image -=-"
                //sh "mvn docker:build"
            }
        }

        stage('Run Docker image') {
            steps {
                echo "-=- run Docker image -=-"
                //sh "docker run --name ci-deors-demos-petclinic --detach --rm --network ci deors/deors-demos-petclinic:latest"
            }
        }

        stage('Integration tests') {
            steps {
                echo "-=- execute integration tests -=-"
                //sh "mvn failsafe:integration-test failsafe:verify -DargLine=\"-Dtest.selenium.hub.url=http://selenium-hub:4444/wd/hub -Dtest.target.server.url=http://ci-deors-demos-petclinic:8080/petclinic\""
                //junit 'target/failsafe-reports/*.xml'
            }
        }

        stage('Performance tests') {
            steps {
                echo "-=- execute performance tests -=-"
                //sh "mvn jmeter:jmeter jmeter:results -Djmeter.target.host=ci-deors-demos-petclinic -Djmeter.target.port=8080 -Djmeter.target.root=petclinic"
                //perfReport sourceDataFiles: 'target/jmeter/results/petclinic.csv', errorUnstableThreshold: 0, errorFailedThreshold: 5, errorUnstableResponseTimeThreshold: 'petclinic.jtl:100'
            }
        }

        stage('Dependency vulnerability tests') {
            steps {
                echo "-=- run dependency vulnerability tests -=-"
                //sh "mvn dependency-check:check"
                //dependencyCheckPublisher failedTotalHigh: '30', unstableTotalHigh: '25', failedTotalNormal: '110', unstableTotalNormal: '100'
            }
        }

        stage('Code inspection & quality gate') {
            steps {
                echo "-=- run code inspection & quality gate -=-"
                //sh "mvn sonar:sonar -Dsonar.host.url=http://ci-sonarqube:9000/sonarqube"
            }
        }

        stage('Push Docker image') {
            steps {
                echo "-=- push Docker image -=-"
                //sh "mvn docker:push"
            }
        }
    }

    post {
        always {
            echo "-=- remove deployment -=-"
            //sh "docker stop ci-deors-demos-petclinic"
        }
    }
}