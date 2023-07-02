# cal-prop-cea
propulsion performance calcuration using NASA-CEA

## 概要
NASA-CEAを組み込んだ解析ソフトを作りたい。そこで、RocketCEAを使って実験データからグラフが出せるようにする。

## 導入方法
以下のモジュールを使って環境を構築した。
- **Anaconda**  
  自分の他のPython環境と競合しそうなひとは、Anacondaなど、仮想環境が作れるものを入れる。まあ初めての人も、Anacondaは便利なので入れてみよう。  
  pythonは3.9  
  **WSLでUbuntuを入れるのが最も簡単説ある．．**  
- **Rocket CEA**
  1. まず、gfortranコンパイラを入れる。以下サイトを参考にするが、**RocketCEAの導入**は行わない。  
  https://makkiblog.com/rocketcea_intro/  
  https://rocketcea.readthedocs.io/en/latest/installgfortran.html#link-installgfortran
  2. 次に、公式ドキュメントのクイックスタートの**Anaconda Windows Batch File**を見ながら諸々のモジュールのインストールを行う。
  https://rocketcea.readthedocs.io/en/latest/quickstart.html  
  たぶんエラーが起こるので、以下のサイトを参考に対処する。  
  https://qiita.com/ina111/items/4e09711b9121db90dbaa  
  https://github.com/sonofeft/RocketCEA/issues/11  
  https://visualstudio.microsoft.com/ja/visual-cpp-build-tools/  
  私は諸々エラーが出て公式クイックスタートの通りにできなかったので、optionなしの`pip install rocketcea`で入れた。そうすると、[こちら](https://github.com/sonofeft/RocketCEA/issues/11#issuecomment-665428405)のエラーがでたので、コメントを参考に \.libs フォルダにある .dll ファイルをrocketceaフォルダ直下に移動することで解決した。
  3. **動作確認**  
  `python -c "from rocketcea.cea_obj import CEA_Obj; C=CEA_Obj(oxName='LOX', fuelName='LH2'); print(C.get_Isp())"`
  と打って、`374.30361765576265`と出ればOK
- **Git hub**
- **Visual Studio Code**
- Windows WSL 導入メモ
  https://learn.microsoft.com/ja-jp/windows/wsl/install
  https://rocketcea.readthedocs.io/en/latest/quickstart.html#windows-10-with-wsl
  https://tenshoku-miti.com/takepon/windows-vscode-ternimal-ubuntu/
  https://qiita.com/setonao/items/28749762c0bc1fbbf502
