import pandas as pd
import os,re
from text2listEN import *
from cal_tfidf import *


class caltfidf():
    def __init__(self):
        self.briefintro()
        self.df = self.readdata()
        self.dict_category_id = self.gendict_category_id(self.df)
        self.dict_index_text = self.genindex_text(self.df)

    def briefintro(self):
        print('=====tifdif计算工具=====')
        print('使用说明：\n1. 数据格式要求：数据应至少包含三列，请将列名分别命名为 index，category，text\n**index列为文本id\n**category为所属类别，如果没有类别变量请全部填写1\n**text为要分析的文本\n\n2.将数据保存为xlsx格式\n\n3.将存好的csv文件与本软件放在同一个文件夹下，保证文件夹下不要有其他csv文件\n\n4.运行软件即可')
        input('press any key to continue')

    def readdata(self):
        filelist = [i for i in os.listdir('.') if '.xlsx' in i]
        if len(filelist) == 0:
            print('no csv file in document')
        else:
            try:
                df = pd.read_excel(filelist[0])
                print('csv file has been read')
                return df
            except:
                print('cannot read csv file')

    def gendict_category_id(self,df):
        '''
        用于将df_type_id转化成字典
        :param df:
        :return:dict_category_id 一个以类别为键，id列表为值的字典
        '''
        category= list(set(df['category'].values.tolist()))
        dict_category_id = {}
        for i in category:
            temp = df[df['category'].isin([i])]
            tempappleidlist = list(set(temp['index'].values.tolist()))
            dict_category_id[i] = tempappleidlist
        return dict_category_id

    def genindex_text(self,df):
        temp = df[['index','text']].drop_duplicates()
        dict_id_text = {}
        for row in temp.itertuples(index = False):
            dict_id_text[getattr(row,'index')] = text2listfull(getattr(row,'text'))
        return dict_id_text

    def cal_tfidfEN(self):
        baselistoftextlist = [[]]
        dict_idinsim_category = {}
        i = 1
        for category in self.dict_category_id:
            temptextlist = []
            for index in self.dict_category_id[category]:
                try:
                    temptextlist += self.dict_index_text[index]
                except:
                    continue
            baselistoftextlist.append(temptextlist)
            dict_idinsim_category[category] = i
            i+=1
        tfidf_model = tfidfmodel_cal(baselistoftextlist)

        dict_id_diff = {}
        for category in self.dict_category_id:
            for index in self.dict_category_id[category]:
                try:
                    textlist =self.dict_index_text[index]
                    tempsim =tfidf_model.cal_tfidf(textlist,dict_idinsim_category[category])
                    dict_id_diff[index] = 1- tempsim
                except:
                    continue
        tempdf = pd.DataFrame({'index': [k for k in dict_id_diff], 'diff': [dict_id_diff[k] for k in dict_id_diff]})
        return tempdf

if __name__ == "__main__":
    c = caltfidf()
    df = c.cal_tfidfEN()
    print('starting to calculate ...\nit may take times if the data is big')
    df.to_csv('difftable.csv', index=False)
    print('Done')










