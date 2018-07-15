# モジュールのオーバーヘッド確認とチューニングその２

①snakeviz を使用すると、cProfile の出力した統計結果を視覚化できる。
　図を見るだけでコストの高い関数が一目でわかる。

インストール
```
$ pip install snakeviz
```

起動コマンド
```
$ snakeviz profile.stats
```

以下、実行時の参考画像
<div align="center">
  <img src="https://github.com/Kento75/Python-Performance-Tuning/blob/master/sec2/img/snakebiz_1.PNG" />
  <br>
  <img src="https://github.com/Kento75/Python-Performance-Tuning/blob/master/sec2/img/snakebiz_2.PNG" />
</div>
