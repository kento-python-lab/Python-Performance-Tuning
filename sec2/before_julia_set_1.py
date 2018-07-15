"""
ジュリア集合作成器
（PILを使用した画像描画を除く）
"""
from functools import wraps
import time

# グローバル定数
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f'@timefn: { fn.__name__ } took { str(t2 -t1) } seconds')
        return result
    return measure_time


def calc_pure_python(desired_width, max_iterations):
    """
    複素数の座標リスト zs と、複素数のパラメータリスト cs を作り、
    ジュリア集合を作って表示する。
    """
    x_step = (float(x2 - x1) / float(desired_width))
    y_step = (float(y1 - y2) / float(desired_width))
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    # 座標リストを作り、各点を初期条件にする
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    print('Length of x: ', len(x))
    print('Total elements: ', len(zs))
    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_time = time.time()
    secs = end_time - start_time
    print(f'{ calculate_z_serial_purepython.__name__ } took { secs } seconds')

    # 固定値 1000~2のグリッドを、繰り返し上限300回としたときの値
    # 正当性チェック
    assert sum(output) == 33219980


# CPU バウンドの計算関数
@timefn
@profile
def calculate_z_serial_purepython(maxiter, zs, cs):
    """
    ジュリア漸化式を使用して output リストを計算する
    """
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1

        output[i] = n

    return output


if __name__ == '__main__':
    # ジュリア集合を計算する
    calc_pure_python(desired_width=1000, max_iterations=300)
