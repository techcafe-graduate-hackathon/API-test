import MeCab
import subprocess
import pandas as pd
txt = "婚活パーティー的なマッチング"


#テキストを入れたら、その文の名詞を抽出
cmd = 'echo `mecab-config --dicdir`"/mecab-ipadic-neologd"'
path = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                        shell=True).communicate()[0]).decode('utf-8')
m = MeCab.Tagger("-d {0}".format(path))


def parse_text(text: str):
    parsed_text = m.parse(text).split('\n')
    parsed_results = pd.Series(parsed_text).str.split('[,\t]').tolist()
    df = pd.DataFrame.from_records(parsed_results)
    columns = ['word', 'type', 'sub_type', '4', '5', '6',"7","8","9","10"]
    df.columns = columns
    return df.query("word != 'EOS'").query("word != ''")
    

def norn_extraction(txt):
    df = parse_text(txt)
    df_noun = df[df["type"]=="名詞"].reset_index(drop=True) #品詞が名詞のものだけ抽出
    array_noun = df_noun.iloc[:,:1].values #単語だけに
    # print(array_noun)
    return array_noun

norn_extraction(txt)
