import re
import time
def split_word(input_file, output_path):
    with open(input_file, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            final_data=re.findall(r"\w+",line)
            sentence=''.join(final_data)
            with open(output_path,'a',encoding='utf-8') as file:
                for word in sentence:
                    file.write(word+' ')
if __name__ == '__main__':
    input_path='data/single/全量文本 - 计算机行业.txt'
    output_path='data/single/result-split.txt'
    print("正在写入数据，请稍等。。。。")
    start_time=time.time()
    split_word(input_path,output_path)
    end_time=time.time()
    cost_time=end_time-start_time
    print("写入数据完毕，请稍等一共耗时：{}秒".format(cost_time))