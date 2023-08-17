import pandas as pd
from tqdm import tqdm
from glob import glob
import sys 

if __name__ == "__main__":
    all_df = pd.DataFrame()
    for i in tqdm(glob(sys.argv[1] + "/*.csv")):
        etc = pd.read_csv(i, encoding="utf-8-sig", index_col=0)
        all_df = pd.concat([all_df, etc], axis=0)
        

    all_df = all_df.sort_values(["확인용", "단어일련번호"]).reset_index(drop=True)
    all_df.to_csv(sys.argv[1] + "/complete_data.csv", encoding="utf-8-sig", index=False)