import os
import re
class ProcessData:
    def __init__(self):
        self.input_path='data/corpus'
        self.output_LabelPath='data/result-label.txt'
        self.output_SplitPath='data/result-split.txt'
        self.lines=self.get_lines()
    #获取data/corpus路径下所有语料文件
    def get_paths(self):
        file_names=os.listdir(self.input_path)
        print(file_names)
        full_paths=[]
        for file_name in file_names:
            full_path=os.path.join(self.input_path+'/',file_name)
            full_paths.append(full_path)
        return full_paths
    #获取所有行，用‘\t’分割数据
    def get_lines(self):
        full_paths=self.get_paths()
        lines=[]
        for full_path in full_paths:
            with open(full_path, 'r', encoding='utf-8') as news:
                for line in news:
                    raw_line=line.split('\t')
                    lines.append(raw_line)
            return lines
    #获取新闻
    def get_sentences(self):
        sentences=[]
        for line in self.lines:
            sentences.append(line[0])
        return sentences
    #获取去重数据
    def get_newsenc(self):
        sentences=self.get_sentences()
        new_secences = list(set(sentences))
        new_secences.sort(key=sentences.index)
        return new_secences
    #获取源
    def get_sources(self):
        sources=[]
        for line in self.lines:
            sources.append(line[1])
        #有的source名称为公司，不能去重
        # new_sources=list(set(sources))
        # new_sources.sort(key=sources.index)
        return sources
    #获取目标
    def get_targets(self):
        targets=[]
        for line in self.lines:
            targets.append(line[2])
        return targets
    #处理成标准数据格式，以便处理 ['news_sentences',[keyword1,...]]
    def get_normData(self):
        sentences = self.get_sentences()  # 没有去重之前的句子
        new_sen = self.get_newsenc()  # 去重之后
        sources = self.get_sources()
        targets = self.get_targets()
        normData = []
        for sen in new_sen:
            data = []  # 存放每一条新闻，以及对应的source和target
            temp = []
            num = sentences.count(sen)  # 计算每条新闻的记录数目
            # 组成检索的信息
            temp.append(sources[0])
            for j in range(num):
                temp.append(targets[j])
            data.append(sen)
            data.append(temp)
            normData.append(data)
            targets = targets[num:]  # 切分列表
            sources = sources[num:]
        return normData
    def write_data(self):
        normData=self.get_normData()
        for data in normData:
            sentence=data[0].replace(" ",'')
            # sentence=data[0]
            keywords=data[1]
            #print(keywords)
            for keyword in keywords:
                if keyword:
                    temp=sentence.split(keyword)
                    split_op=" "+keyword+" "
                    sentence=split_op.join(temp)
            # final_data=re.findall(r"\w+",sentence)
            final_data=sentence.split(' ')

            with open(self.output_LabelPath,'a',encoding='utf-8') as result:
                for word in final_data:
                    if word in keywords:
                        for index in range(len(word)):
                            if index==0:
                                result.write(word[index]+' '+'B-ORG')
                                result.write('\n')
                            elif index!=0:
                                result.write(word[index]+' '+'I-ORG')
                                result.write('\n')
                    elif word not in keywords:
                            for index in range(len(word)):
                                result.write(word[index]+' '+'O')
                                result.write('\n')
            #过滤标点符号和空格
            # nor_sentence=''.join(final_data)
            with open(self.output_SplitPath,'a',encoding='utf-8') as split_result:
                for word in sentence:
                    if word!=' ':
                        split_result.write(word+' ');
            #     if keyword in sentence:
            #         sentence=sentence.replace(keyword,'')
            # with open(self.output_path,'a',encoding='utf-8') as result:
            #     for keyword in keywords:
            #         for index in range(len(keyword)):
            #             if index==0:
            #                 result.write(keyword[index]+' '+'B-ORG')
            #             elif index !=0:
            #                 result.write(keyword[index]+' '+'I-ORG')
            #             result.write('\n')
            #     for word in sentence:
            #         result.write(word+' '+'O')
            #         result.write('\n')
if __name__ == '__main__':
    proData=ProcessData()
    proData.get_paths()
    print("***正在写入数据。。。。")
    #result-label.txt  用于保存标签数据
    if 'result-label.txt' in os.listdir('data'):
        print("***result-label.txt已经存在，将会被删除")
        os.remove('data/result-label.txt')
    #result-split.txt  用于保存单字数据
    if 'result-split.txt' in os.listdir('data'):
        print("***result-split.txt已经存在，将会被删除")
        os.remove('data/result-split.txt')
    proData.write_data()
    print("***保存数据完毕")
