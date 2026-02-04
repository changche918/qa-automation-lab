# sys.path.append(os.path.dirname(os.path.abspath(__file__))) 範例
# sys.path.append('.') 範例
import sys
import os
from my_project.bbb import saveFolder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('.')

click = saveFolder('my_folder')
click.clickFolder()