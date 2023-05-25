import subprocess
import time
from datetime import datetime

def server_info():
    while True:
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")          # 現在時刻
        temp       = run_shell_command("vcgencmd measure_temp")      # CPU温度
        clock      = run_shell_command("vcgencmd measure_clock arm") # CPU周波数
        volts      = run_shell_command("vcgencmd measure_volts")     # CPU電圧
        memory_cpu = run_shell_command("vcgencmd get_mem arm")       # CPUのメモリ使用量
        memory_gpu = run_shell_command("vcgencmd get_mem gpu")       # GPUのメモリ使用量

        # 結果表示
        return date, temp, clock, volts, memory_cpu, memory_gpu
    

# シェルコマンドを実行する関数
def run_shell_command(command_str):
    proc = subprocess.run(command_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    result = proc.stdout.split("=")
    return result[1].replace('\n', '')

if __name__ == '__main__':
    main()