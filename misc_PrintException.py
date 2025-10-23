import datetime
import os


def fcolor(r,g,b,text):
    return f'\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m'
def bcolor(r,g,b,text):
    return f'\033[48;2;{r};{g};{b}m{text} \033[48;2;0;0;0m'

os.system('color')


DATE=datetime.date.today().strftime("%Y%m%d")

def print_ex(ex:Exception,filename='DevLog',folder='DevLog'):
    '''
    Print the exception information in the console and save it to a log file.
    Args:
        ex (Exception): The exception object to be logged.
        filename (str, optional): The name of the log file. Defaults to 'DevLog'.
        folder (str, optional): The folder where the log file will be saved. Defaults to 'DevLog'.
    '''
    os.makedirs(folder, exist_ok=True)
    exc_tb=ex.__traceback__
    print(f"{fcolor(255,0,0,'Traceback Error: ')}{ex}")
    with open(fr'.\{folder}\{DATE}-{filename}.txt','a') as file:
        time=datetime.datetime.now()
        file.write(f"{time.hour:02}:{time.minute:02}:{time.second:02}>>Traceback Error:{ex}"+'\n')
    while exc_tb is not None:
        exc_dir=exc_tb.tb_frame.f_code.co_filename
        exc_line=exc_tb.tb_lineno
        exc_func=exc_tb.tb_frame.f_code.co_name
        exc_str='\t'.join(list(map(str,(f"{fcolor(50,250,255,'File: ')}{exc_dir}",f"| {fcolor(255,100,200,'Line: ')}{exc_line}",f"| {fcolor(250,250,0,'Function: ')}{exc_func}"))))
        print(exc_str)
        exc_log='\t'.join(list(map(str,(f"File: {exc_dir}",f"| 'Line:{exc_line}",f"| Function:{exc_func}"))))
        with open(fr'.\{folder}\{DATE}-{filename}.txt','a') as file:
            file.write(f'{exc_log}'+'\n')
        exc_tb=exc_tb.tb_next
    print(fcolor(255,50,30,'Error End.'))

# def print_log(text:str):
#     print(text)
#     with open(fr'{LOGDIR}\{DATE}-CommonLog.txt','a') as file:
#         time=datetime.datetime.now()
#         file.write(f"{time.hour:02}:{time.minute:02}:{time.second:02}>>{text}"+'\n')