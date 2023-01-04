import argparse
import os
from ensembles.ensembles import Ensemble
from datetime import datetime
from pytz import timezone

def main(args):
    filepath = args.FILE_PATH
    savepath = args.RESULT_PATH
    os.makedirs(filepath, exist_ok=True)
    if os.listdir(filepath) == []:
        raise ValueError(f"{filepath}에 csv 파일을 넣어주세요.")
    os.makedirs(savepath, exist_ok=True)

    en = Ensemble(filepath=filepath)

    if args.STRATEGY == "HARD":
        print("your choice: Hard / Weighted1 None / Weighted2 None")
        strategy_title = 'Hard'
        result = en.hard()
    elif args.STRATEGY == "WEIGHTED":
        if args.WEIGHT1:
            print(f"your choice: Weighted / Weighted1 {args.WEIGHT1} / Weighted2 None")
            strategy_title = 'Weight1'+'-'.join(map(str,*args.WEIGHT1))
            result = en.weighted(*args.WEIGHT1)
        else:
            strategy_title = 'Hard'
            result = en.hard()
    
    now = datetime.now(timezone("Asia/Seoul")).strftime(f"%Y-%m-%d_%H:%M")
    result.to_csv(f'{savepath}{now}-{strategy_title}.csv',index=False)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    arg = parser.add_argument

    arg("--FILE_PATH", type=str,required=False,
        default="./ensembles_inference/",
        help='required: 앙상블 하고 싶은 csv 파일들이 있는 폴더의 경로를 입력해주세요.')
    arg('--STRATEGY', type=str, default='HARD',
        choices=['HARD', 'WEIGHTED'],
        help='optional: [HARD, WEIGHTED] 중 앙상블 전략을 선택해 주세요. (default="HARD")')
    arg('--WEIGHT1', nargs='+',default=None,
        type=lambda s: [float(item) for item in s.split(',')],
        help='optional: csv 사이의 가중치를 조정할 수 있습니다. 입력하지 않으면 Hard Voting과 같습니다.')
    arg('--WEIGHT2', nargs='+',default=None,
        type=lambda s: [float(item) for item in s.split(',')],
        help='optional: 순위의 가중치를 조정할 수 있습니다. 입력하지 않으면 정해진 metric이 작동합니다.')
    arg('--RESULT_PATH',type=str, default='./ensembles_submit/',
        help='optional: 앙상블 결과를 저장할 폴더 경로를 전달합니다. (default:"./ensembles_submit/")')
    args = parser.parse_args()

    main(args)