import time
import pandas as pd
import hanlp
import torch
import random
import os
import numpy as np
from tqdm import tqdm
from hanlp_restful import HanLPClient


def seed_everything(seed=2022):
    '''
    设置整个开发环境的seed
    '''
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # some cudnn methods can be random even after fixing the seed
    # unless you tell it to be deterministic
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


seed_everything()

"""
Restful 方式，不能一直调用
"""
# HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='mul')  # auth不填则匿名，zh中文，mul多语种
# s = time.time()
# print(HanLP.tokenize("2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。阿婆主来到北京立方庭参观自然语义科技公司。"))
# print(f"分词耗时{time.time()-s}s")


"""
专业级：本地模型
"""
def Pro_tokenize():
    mul_tokenizer = hanlp.load(hanlp.pretrained.tok.UD_TOK_MMINILMV2L12)
    df_zlib = pd.read_csv('zlib_index_books.csv', header=None)
    df_title = df_zlib.iloc[:, :2].astype(str)
    df_title.columns = ["id", "title"]
    df_title["title_token"] = None
    print("分词中……\n")
    # df_title = df_title.head()
    total = len(df_title)
    for i in tqdm(range(total)):
        try:
            title = df_title["title"][i]
            batch_token_lis = mul_tokenizer(title)
            df_title["title_token"][i] = batch_token_lis
        except Exception as e:
            print(e)
    print(len(df_title))
    df_title.to_csv("title_token.csv")
    print("分词结果保存完成……")


if __name__ == '__main__':
    Pro_tokenize()
