# モジュールのオーバーヘッド確認とチューニングその４

①memory_profiler を使用すると行単位でメモリ使用率を計測するので、
　チューニングが必要は行の特定ができる。(line_profiler のRAM版)

インストール

```
# psutil もインストールされる。
$ pip install memory_profiler
```

起動前の準備
起動前に対象モジュールの関数に @profile を付与する。(line_profiler と同じ)

起動コマンド
```
$ python -m memory_profiler before_julia_set_1.py

```