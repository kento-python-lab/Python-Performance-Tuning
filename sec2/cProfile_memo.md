# モジュールのオーバーヘッド確認とチューニングその１

①cProfile ライブラリを使用するとモジュール内のオーバーヘッドを確認できる。

起動コマンド
```
$ python -m cProfile -s cumulative  before_julia_set_1.py
```

例)
```
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   25.144   25.144 {built-in method builtins.exec}
        1    0.050    0.050   25.144   25.144 before_julia_set_1.py:4(<module>)
        1    1.191    1.191   25.094   25.094 before_julia_set_1.py:24(calc_pure_python)
        1    0.000    0.000   23.595   23.595 before_julia_set_1.py:14(measure_time)
        1   16.729   16.729   23.595   23.595 before_julia_set_1.py:64(calculate_z_serial_purepython)
 34219980    6.867    0.000    6.867    0.000 {built-in method builtins.abs}
  2002000    0.292    0.000    0.292    0.000 {method 'append' of 'list' objects}
        1    0.015    0.015    0.015    0.015 {built-in method builtins.sum}
        4    0.001    0.000    0.001    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 before_julia_set_1.py:13(timefn)
        1    0.000    0.000    0.000    0.000 functools.py:44(update_wrapper)
        4    0.000    0.000    0.000    0.000 {built-in method time.time}

以下略
```

②profile.stats オプションを使用することで profile.stats ファイルを生成できる。

起動コマンド
```
$ python -m cProfile -o profile.stats  before_julia_set_1.py
```

profile.stats はPythonで読み込むことができる。

```
$ python
> import pstats
> p = pstats.Stats('profile.stats')
> p.sort_stats('cumulative')
> <pstats.Stats object at 0x00000299728D9278>
> p.print_stats()
Sun Jul 15 21:42:21 2018    profile.stats

         36222017 function calls in 27.094 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   27.094   27.094 {built-in method builtins.exec}
        1    0.051    0.051   27.094   27.094 before_julia_set_1.py:4(<module>)
        1    1.218    1.218   27.044   27.044 before_julia_set_1.py:24(calc_pure_python)
        1    0.000    0.000   25.514   25.514 before_julia_set_1.py:14(measure_time)
        1   18.297   18.297   25.514   25.514 before_julia_set_1.py:64(calculate_z_serial_purepython)
 34219980    7.217    0.000    7.217    0.000 {built-in method builtins.abs}
  2002000    0.296    0.000    0.296    0.000 {method 'append' of 'list' objects}
        1    0.015    0.015    0.015    0.015 {built-in method builtins.sum}
        4    0.001    0.000    0.001    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 before_julia_set_1.py:13(timefn)

以下略
```

profile.stats から呼び出し側の情報を表示することもできる。
print_callers() 関数を使用することで呼び出し元を特定できるので、コストの高い呼び出し元を絞り込むことができる。

```
> p.print_callers()
   Ordered by: cumulative time

Function                                                                                   was called by...
                                                                                               ncalls  tottime  cumtime
{built-in method builtins.exec}                                                            <-
before_julia_set_1.py:4(<module>)                                                          <-       1    0.051   27.094  {built-in method builtins.exec}
before_julia_set_1.py:24(calc_pure_python)                                                 <-       1    1.218   27.044  before_julia_set_1.py:4(<module>)
before_julia_set_1.py:14(measure_time)                                                     <-       1    0.000   25.514  before_julia_set_1.py:24(calc_pure_python)
before_julia_set_1.py:64(calculate_z_serial_purepython)                                    <-       1   18.297   25.514  before_julia_set_1.py:14(measure_time)
{built-in method builtins.abs}                                                             <- 34219980    7.217    7.217  before_julia_set_1.py:64(calculate_z_serial_purepython)
{method 'append' of 'list' objects}                                                        <- 2002000    0.296    0.296  before_julia_set_1.py:24(calc_pure_python)
{built-in method builtins.sum}                                                             <-       1    0.015    0.015  before_julia_set_1.py:24(calc_pure_python)
{built-in method builtins.print}                                                           <-       1    0.000    0.000  before_julia_set_1.py:14(measure_time)
                                                                                                    3    0.000    0.000  before_julia_set_1.py:24(calc_pure_python)
before_julia_set_1.py:13(timefn)                                                           <-       1    0.000    0.000  before_julia_set_1.py:4(<module>)
C:\Users\kento\AppData\Local\Programs\Python\Python36\lib\functools.py:44(update_wrapper)  <-       1    0.000    0.000  before_julia_set_1.py:13(timefn)
{built-in method time.time}                                                                <-       2    0.000    0.000  before_julia_set_1.py:14(measure_time)
                                                                                                    2    0.000    0.000  before_julia_set_1.py:24(calc_pure_python)
<frozen importlib._bootstrap>:997(_handle_fromlist)                                        <-       1    0.000    0.000  before_julia_set_1.py:4(<module>)
{built-in method builtins.len}                                                             <-       2    0.000    0.000  before_julia_set_1.py:24(calc_pure_python)
                                                                                                    2    0.000    0.000  before_julia_set_1.py:64(calculate_z_serial_purepython)
{built-in method builtins.getattr}                                                         <-       7    0.000    0.000  C:\Users\kento\AppData\Local\Programs\Python\Python36\lib\functools.py:44(update_wrap
per)

以下略
```

print_callees() 関数を使用することでどの関数を呼び出しているのかを表示できる。

```
> p.print_callees()
   Ordered by: cumulative time

Function                                                                                   called...
                                                                                               ncalls  tottime  cumtime
{built-in method builtins.exec}                                                            ->       1    0.051   27.094  before_julia_set_1.py:4(<module>)
before_julia_set_1.py:4(<module>)                                                          ->       1    0.000    0.000  <frozen importlib._bootstrap>:997(_handle_fromlist)
                                                                                                    1    0.000    0.000  before_julia_set_1.py:13(timefn)
                                                                                                    1    1.218   27.044  before_julia_set_1.py:24(calc_pure_python)
before_julia_set_1.py:24(calc_pure_python)                                                 ->       1    0.000   25.514  before_julia_set_1.py:14(measure_time)
                                                                                                    2    0.000    0.000  {built-in method builtins.len}
                                                                                                    3    0.000    0.000  {built-in method builtins.print}
                                                                                                    1    0.015    0.015  {built-in method builtins.sum}
                                                                                                    2    0.000    0.000  {built-in method time.time}
                                                                                              2002000    0.296    0.296  {method 'append' of 'list' objects}
before_julia_set_1.py:14(measure_time)                                                     ->       1   18.297   25.514  before_julia_set_1.py:64(calculate_z_serial_purepython)
                                                                                                    1    0.000    0.000  {built-in method builtins.print}
                                                                                                    2    0.000    0.000  {built-in method time.time}
before_julia_set_1.py:64(calculate_z_serial_purepython)                                    -> 34219980    7.217    7.217  {built-in method builtins.abs}
                                                                                                    2    0.000    0.000  {built-in method builtins.len}
{built-in method builtins.abs}                                                             ->
{method 'append' of 'list' objects}                                                        ->
{built-in method builtins.sum}                                                             ->
{built-in method builtins.print}                                                           ->
before_julia_set_1.py:13(timefn)                                                           ->       1    0.000    0.000  C:\Users\kento\AppData\Local\Programs\Python\Python36\lib\functools.py:44(update_wrap
per)
                                                                                                    1    0.000    0.000  C:\Users\kento\AppData\Local\Programs\Python\Python36\lib\functools.py:74(wraps)
C:\Users\kento\AppData\Local\Programs\Python\Python36\lib\functools.py:44(update_wrapper)  ->       7    0.000    0.000  {built-in method builtins.getattr}
                                                                                                    5    0.000    0.000  {built-in method builtins.setattr}
                                                                                                    1    0.000    0.000  {method 'update' of 'dict' objects}

以下略
```
