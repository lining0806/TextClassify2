**英文分词，采用nltk工具包进行分词**  
pip install nltk 
**中文分词，采用jieba工具包进行分词**  
pip install jieba 
**stopwords_chs和stopwords_eng为过滤词黑名单**    
* 可以随时添加要过滤的单词，一行一个  
* 如果添加的过滤词无法正确被jieba分词，则同样方法将该需要过滤的词及词频加入到主词典dict文件中或者用户词典user_dict，一行一个（词频也可省略）  


**Ubuntu下pil numpy scipy matplotlib的安装：**  

    sudo apt-get update
    sudo apt-get install git g++
    sudo apt-get install python-dev python-setuptools
    
    sudo easy_install Cython 
    sudo easy_install pil
    sudo apt-get install libatlas-base-dev # 科学计算库
    sudo apt-get install gfortran # fortran编译器
    sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev
    export BLAS=/usr/lib/libblas/libblas.so 
    export LAPACK=/usr/lib/lapack/liblapack.so 
    export ATLAS=/usr/lib/atlas-base/libatlas.so
    sudo apt-get install python-numpy
    sudo apt-get install python-scipy
    sudo apt-get install python-matplotlib
    
    sudo easy_install jieba
    sudo easy_install scikit-learn
    sudo easy_install simplejson
    sudo easy_install pymongo


**CentOS下pil numpy scipy matplotlib的安装：**  

    离线安装Python
    sudo yum install python-setuptools
    sudo yum install gcc-gfortran 
    sudo yum install blas-devel
    sudo yum install lapack-devel
    进入numpy解压目录
    sudo python setup.py build
    sudo python setup.py install
    进入scipy解压目录
    sudo python setup.py build
    sudo python setup.py install
    进入matplotlib目录
    sudo yum install libpng-devel
    sudo python setup.py build
    sudo python setup.py install
    
    sudo easy_install jieba
    sudo easy_install scikit-learn
    sudo easy_install simplejson
    sudo easy_install pymongo
