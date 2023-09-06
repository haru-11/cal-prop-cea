# cal-prop-cea
propulsion performance calcuration using NASA-CEA  

## 概要
NASA-CEAを組み込んだ解析ソフトを作りたい。そこで、RocketCEAを使って実験データからグラフが出せるようにする。  
現在のところ，キーエンスのwaveloggerから吐き出されるcsvファイルのみ対応している．

## 導入方法
以下のモジュールを使って環境を構築した。
- **Anaconda**  
  自分の他のPython環境と競合しそうなひとは、Anacondaなど、仮想環境が作れるものを入れる。まあ初めての人も、Anacondaは便利なので入れてみよう。  
  pythonは3.9  
  WSLでUbuntuを入れるのが最も簡単説ある．.  
- **Rocket CEA**  
  1. まず、gfortranコンパイラを入れる。以下サイトを参考にするが、**RocketCEAの導入**は行わない。
     - https://makkiblog.com/rocketcea_intro/
     - https://rocketcea.readthedocs.io/en/latest/installgfortran.html#link-installgfortran
  2. 次に、公式ドキュメントのクイックスタートの**Anaconda Windows Batch File**を見ながら諸々のモジュールのインストールを行う。
     - https://rocketcea.readthedocs.io/en/latest/quickstart.html  
  3. たぶんエラーが起こるので、以下のサイトを参考に対処する。
     - https://qiita.com/ina111/items/4e09711b9121db90dbaa
     - https://github.com/sonofeft/RocketCEA/issues/11
     - https://visualstudio.microsoft.com/ja/visual-cpp-build-tools/
  4. 私は諸々エラーが出て公式クイックスタートの通りにできなかったので、optionなしの`pip install rocketcea`で入れた。そうすると、[こちら](https://github.com/sonofeft/RocketCEA/issues/11#issuecomment-665428405)のエラーがでたので、コメントを参考に \.libs フォルダにある .dll ファイルをrocketceaフォルダ直下に移動することで解決した。
  5. **動作確認**  
  `python -c "from rocketcea.cea_obj import CEA_Obj; C=CEA_Obj(oxName='LOX', fuelName='LH2'); print(C.get_Isp())"`
  と打って、`374.30361765576265`と出ればOK
- **Git hub**
  - アカウント作成
  - ワークスペースへのアクセス権限をharu-11に申請
    - 申請方法は，何らかの手段を使ってusernameを伝えてください
    - これをすると，pushやbranchの機能を使えるようになる
- **Visual Studio Code**
  - エディタはこれがおすすめです．
  - `code`コマンドで，CLIからコードを開くことができる．（例：`code main.py`）
- Windows WSLにrocketceaを導入するときに参考にしたサイト
  - https://learn.microsoft.com/ja-jp/windows/wsl/install
  - https://rocketcea.readthedocs.io/en/latest/quickstart.html#windows-10-with-wsl
  - https://tenshoku-miti.com/takepon/windows-vscode-ternimal-ubuntu/
  - https://qiita.com/setonao/items/28749762c0bc1fbbf502

## 使用方法（データ整理と時系列グラフ出力）  
- `main.py`の１と２のパスを設定する．  
- `Gen_data`の3の変数を確認し，必要があれば変更する．WAVELOGGERで取得するデータ数やデータの種類によって変わる．  
- `Gen_graphs`で作りたいグラフの設定を行う．よく使うであろうグラフはあらかじめ出力するようになっている．  
- `python main.py`のコマンドを実行  
## 使用方法（result_ave.csvファイルから，累計推進剤使用量のグラフ出力）
- `Gen_graphs`の下の方の関数をいい感じにいじるとcsvから横軸が累計推進剤使用量のグラフが作れる．  
- 実行は`python Gen_graphs.py`

## 生成物  
- 各種グラフ  
- result_allと書いてあるcsvは，元のcsvからバルブの開+/-設定秒間のデータを抜き出したものである．処理したcsvファイルの個数だけファイルができる．
- result_aveは，定常区間の各性能の平均値を取得したものである．一つのファイルの中に処理したファイルの個数だけできる．
