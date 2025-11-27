#!groovy

pipeline {
    agent any

    environment {
        // 代理配置
        HTTPS_PROXY = 'http://100.68.169.226:3128'
        HTTP_PROXY = 'http://100.68.169.226:3128'
        NO_PROXY = '*.ivolces.com,*.volces.com'
        
        // Python配置
        VENV_DIR = "${WORKSPACE}/venv"
        PYTHON_VERSION = 'python3'

        // Docker镜像配置
        REGISTRY = 'ph-sw-cn-beijing.cr.volces.com'
        REGISTRY_HTTPS = 'https://ph-sw-cn-beijing.cr.volces.com'
        REGISTRY_NAMESPACE = 'jenkins'
        IMAGE_NAME = 'python-jenkins-pipeline'
        IMAGE_TAG = 'latest'
        CONTAINER_NAME= 'jenkins-flask'
    }

    stages {
        stage('Environment preparation') {
            steps {
                echo "-=- preparing project environment -=-"
                // Python dependencies
                sh '''
                    export no_proxy=*.ivolces.com,*.volces.com
                    
                    # 安装依赖
                    apt-get update
                    apt-get install -y python3.11-venv
                
                    # 创建虚拟环境
                    python3 -m venv venv
                    
                    # 激活虚拟环境
                    . venv/bin/activate
                    
                    # 升级 pip
                    pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
                    
                    # 安装依赖
                    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
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
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Create Docker network & Remove existing container') {
            steps {
                echo "-=- create Docker network -=-"
                sh '''
                    if docker network inspect ci > /dev/null 2>&1; then
                        echo "✅ Network 'ci' already exists"
                    else
                        docker network create ci
                        echo "✅ Network 'ci' created successfully"
                    fi
                    if docker ps -a | grep ${CONTAINER_NAME} > /dev/null 2>&1; then
                        echo "${CONTAINER_NAME} already exists, will remove it"
                        docker stop ${CONTAINER_NAME}
                        docker rm ${CONTAINER_NAME}
                    fi
                    
                '''
            }
        }
        

        stage('Run Docker image') {
            steps {
                echo "-=- run Docker image -=-"
                sh "docker run --name ${CONTAINER_NAME} --detach --rm --network ci -p 5001:5000 ${IMAGE_NAME}:${IMAGE_TAG}"
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
                '''
                // locust -f ./perf_test/locustfile.py --no-web -c 1000 -r 100 --run-time 1m -H http://172.18.0.3:5001
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

        stage('Push Docker image') {
            steps {
                echo "-=- push Docker image to hub -=-"
                script {
                    docker.withRegistry("${REGISTRY_HTTPS}", 'crrobot_for_jenkins') {
                        sh '''
                            set -e
                            
                            # 标记镜像
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
                            
                            # 推送镜像
                            docker push ${REGISTRY}/${REGISTRY_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}
                            
                            echo "✅ Docker image pushed successfully"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo "-=- remove deployment -=-"
            sh "docker stop ${CONTAINER_NAME}"
        }
    }
}
