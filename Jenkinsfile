#!groovy

pipeline {
    agent any

    stages {
        stage('Environment preparation') {
            steps {
                echo "-=- preparing project environment -=-"
                // Python dependencies
                sh '''
                    # 安装依赖
                    apt-get update
                    apt-get install -y python3.11-venv
                
                    # 创建虚拟环境
                    python3 -m venv venv
                    
                    # 激活虚拟环境
                    . venv/bin/activate
                    
                    # 升级 pip
                    pip install --upgrade pip
                    
                    # 安装依赖
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Compile') {
            steps {
                echo "-=- compiling project -=-"
                sh '''
                . venv/bin/activate
                python -m compileall .
                '''
            }
        }

        stage('Unit tests') {
            steps {
                echo "-=- execute unit tests -=-"
                sh '''
                . venv/bin/activate
                pytest -v test
                '''
            }
        }

        stage('Create config') {
            steps {
                echo '-=- creating config.yml -=-'
                sh '''
                    # 使用 printf 确保没有隐藏字符
                    printf 'module: app\nbaseline: 10\nexclude-modules: []\ntest-runner:\n  name: unittest\n  args: test\nexecution-engine:\n  name: local\n' > config.yml
                    
                    echo "✅ config.yml created"
                    cat config.yml
                '''
            }
        }
        
        stage('Validate config') {
            steps {
                echo '-=- validating config.yml -=-'
                sh '''
                    . venv/bin/activate
                    python3 -c "import yaml; config = yaml.safe_load(open('config.yml')); print('✅ Config valid'); print(config)"
                '''
            }
        }


        stage('Mutation tests') {
            steps {
                echo "-=- execute mutation tests -=-"
                // initialize mutation testing session
                sh '''
                . venv/bin/activate
                '''
                # cosmic-ray init config.yml jenkins_session && cosmic-ray --verbose exec jenkins_session && cosmic-ray dump jenkins_session | cr-report
            }
        }

        stage('Package') {
            steps {
                echo "-=- packaging project -=-"
                echo "No packaging phase for python projects ..."
            }
        }

        stage('Build Docker image') {
            steps {
                echo "-=- build Docker image -=-"
                sh '''
                . venv/bin/activate
                docker build -t restalion/python-jenkins-pipeline:0.1 .
                '''
            }
        }

        stage('Run Docker image') {
            steps {
                echo "-=- run Docker image -=-"
                sh "docker run --name python-jenkins-pipeline --detach --rm --network ci -p 5001:5000 restalion/python-jenkins-pipeline:0.1"
            }
        }

        stage('Integration tests') {
            steps {
                echo "-=- execute integration tests -=-"
                sh '''
                . venv/bin/activate
                pytest -v int_test
                '''
            }
        }

        stage('Performance tests') {
            steps {
                echo "-=- execute performance tests -=-"
                sh '''
                . venv/bin/activate
                locust -f ./perf_test/locustfile.py --no-web -c 1000 -r 100 --run-time 1m -H http://172.18.0.3:5001
                '''
            }
        }

        stage('Dependency vulnerability tests') {
            steps {
                echo "-=- run dependency vulnerability tests -=-"
                sh '''
                . venv/bin/activate
                safety check
                '''
            }
        }

        stage('Code inspection & quality gate') {
            steps {
                echo "-=- run code inspection & quality gate -=-"
                sh '''
                . venv/bin/activate
                pylama
                '''
            }
        }

        stage('Push Docker image') {
            steps {
                echo "-=- push Docker image -=-"
                withDockerRegistry([ credentialsId: "werdar-wedartg-uiny67-adsuja0-12njkn3", url: "" ]) {
                    sh "docker push restalion/python-jenkins-pipeline:0.1"
                }
                
                //sh "mvn docker:push"
            }
        }
    }

    post {
        always {
            echo "-=- remove deployment -=-"
            sh "docker stop python-jenkins-pipeline"
        }
    }
}
