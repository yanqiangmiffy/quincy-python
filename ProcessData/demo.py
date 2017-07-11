import os
class ProcessData:
    def __init__(self):
        self.input_path='data/news.txt'
        self.output_path='data/result.txt'
        self.lines=self.get_lines()
    #获取所有行，用‘\t’分割数据
    def get_lines(self):
        lines=[]
        with open(self.input_path, 'r', encoding='utf-8') as news:
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
            sentence=data[0]
            keywords=data[1]
            for keyword in keywords:
                if keyword in sentence:
                    sentence=sentence.replace(keyword,'')
            with open(self.output_path,'a',encoding='utf-8') as result:
                for keyword in keywords:
                    for index in range(len(keyword)):
                        if index==0:
                            result.write(keyword[index]+' '+'B-ORG')
                        elif index !=0:
                            result.write(keyword[index]+' '+'I-ORG')
                        result.write('\n')
                for word in sentence:
                    result.write(word+' '+'O')
                    result.write('\n')
if __name__ == '__main__':
    proData=ProcessData()
    print("***正在写入数据。。。。")
    if 'result.txt' in os.listdir('data'):
        print("***result.txt已经存在，将会被删除")
        os.remove('data/result.txt')
    proData.write_data()
    print("***保存数据完毕")