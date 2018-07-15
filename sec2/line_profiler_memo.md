# モジュールのオーバーヘッド確認とチューニングその３

①line_profiler を使用すると各関数を行単位で計測するので、
　チューニングが必要は行の特定ができる。

インストール
※  コンパイラが必要になるので以下のURLから取得してインストールする。
　　https://www.visualstudio.com/ja/downloads

<div align="center">
  <img src="https://github.com/Kento75/Python-Performance-Tuning/blob/master/sec2/img/build_tool_for_windows1.PNG" />
  <img src="https://github.com/Kento75/Python-Performance-Tuning/blob/master/sec2/img/build_tool_for_windows2.PNG" />
</div>

```
# エラーが出るがインストールはできる。
$ pip install line_profiler
$ git clone https://github.com/rkern/line_profiler.git
```

起動前の準備
起動前に対象モジュールの関数に @profile を付与する。

起動コマンド
```
$ python line_profiler/kernprof.py -l -v before_julia_set_1.py

Length of x:  1000
Total elements:  1000000
@timefn: calculate_z_serial_purepython took 247.3246467113495 seconds
calculate_z_serial_purepython took 247.3246467113495 seconds
Wrote profile results to before_julia_set_1.py.lprof
Timer unit: 3.9474e-07 s

Total time: 153.627 s
File: before_julia_set_1.py
Function: calculate_z_serial_purepython at line 64

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    64                                           @timefn
    65                                           @profile
    66                                           def calculate_z_serial_purepython(maxiter, zs, cs):
    67                                               """
    68                                               ジュリア漸化式を使用して output リストを計算する
    69                                               """
    70         1      20439.0  20439.0      0.0      output = [0] * len(zs)
    71   1000001    2438583.0      2.4      0.6      for i in range(len(zs)):
    72   1000000    2369382.0      2.4      0.6          n = 0
    73   1000000    2854705.0      2.9      0.7          z = zs[i]
    74   1000000    2726279.0      2.7      0.7          c = cs[i]
    75  34219980  153251167.0      4.5     39.4          while abs(z) < 2 and n < maxiter:
    76  33219980  125811355.0      3.8     32.3              z = z * z + c
    77  33219980   96665442.0      2.9     24.8              n += 1
    78
    79   1000000    3047055.0      3.0      0.8          output[i] = n
    80
    81         1          6.0      6.0      0.0      return output

```