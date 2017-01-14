# 多算法的文本分类系统

### **更多详见[TextMining](https://github.com/lining0806/TextMining)**

***

## 关于分词
**英文分词，采用nltk工具包进行分词**  

	pip install nltk 

**中文分词，采用jieba工具包进行分词**  

	pip install jieba 

**jieba分词**

	dict 主词典文件 
	user_dict 用户词典文件，即分词白名单 

**user_dict为分词白名单**
* 如果添加的过滤词（包括黑名单和白名单）无法正确被jieba正确分词，则将该需要添加的单词及词频加入到主词典dict文件中或者用户词典user_dict，一行一个（词频也可省略）  
