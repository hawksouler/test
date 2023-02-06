import pandas as pd


class Save_Excel(object):
    
    
    def __init__(self, data, columns):
        self.df = pd.DataFrame(data, columns = columns)
    
    
    def w_Excel(self, file_name):
        self.df.to_excel('C:\\Users\\DELL\\Desktop\\' + file_name + '.xlsx' , index=False)
        
if __name__ == '__main__':
    text = Save_Excel([['腾讯', '北京'], ['阿里巴巴', '杭州'], ['字节跳动', '北京']],['company_name', 'local'])
    text.w_Excel('test')
    print('successful')
        
