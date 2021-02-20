#名詞(タグ)抽出→API化 
#21/02/20 21:30 fastAPIで実装
import MeCab
import subprocess
import pandas as pd
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# txt = "婚活パーティー的なマッチング"


#テキストを入れたら、その文の名詞を抽出
cmd = 'echo `mecab-config --dicdir`"/mecab-ipadic-neologd"'
path = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                        shell=True).communicate()[0]).decode('utf-8')
m = MeCab.Tagger("-d {0}".format(path))


def parse_text(text: str):
    parsed_text = m.parse(text).split('\n')
    parsed_results = pd.Series(parsed_text).str.split('[,\t]').tolist()
    df = pd.DataFrame.from_records(parsed_results)
    columns = ['tags', 'type', 'sub_type', '4', '5', '6',"7","8","9","10"]
    df.columns = columns
    return df.query("word != 'EOS'").query("word != ''")


def norn_extraction(txt):
    df = parse_text(txt)
    df_noun = df[df["type"]=="名詞"].reset_index(drop=True) #品詞が名詞のものだけ抽出
    json_noun = df_noun.iloc[:,:1].to_json() #単語だけに
    # print(json_noun)
    return json_noun

# norn_extraction(txt)


@app.post('/maketag')
#パラメータはtitle : ?title="タイトル"
def Maketag(title:str):
    # URLパラメータ
    response = {}
    tags = norn_extraction(title)
    return tags

if __name__ == '__main__':
    uvicorn.run(app)
