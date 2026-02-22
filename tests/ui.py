import streamlit as st

def main():
    st.set_page_config(page_title="專案架構瀏覽器", layout="wide")
    
    st.title("📂 Python 爬蟲專案架構")
    
    # 左側導覽列
    st.sidebar.header("目錄導覽")
    st.sidebar.markdown("""
    - [x] automation.log
    - [x] data_manager.py
    - [ ] main_scraper.py
    """)

    # 右側主畫面呈現 Markdown 內容
    st.subheader("目前專案結構描述")
    
    # 這裡放你的 MD 內容
    project_tree = """
    ```text
    python_project
    ├─ automation.log
    ├─ change_log.txt
    ├─ error.png
    ├─ Practice_01
    │  ├─ basic.py
    │  └─ bmi_calc.py
    ├─ Python_Course
    │  ├─ 01_print
    │  │  └─ 01_print.py
    │  ├─ 02_lists
    │  │  └─ 02_lists.py
    │  ├─ 03_dictionaries
    │  │  └─ 03_dictionaries.py
    │  ├─ 04_if_else
    │  │  └─ 04_if_else.py
    │  ├─ 05_for_loop
    │  │  └─ 05_for_loop.py
    │  ├─ 06_functions
    │  │  └─ 06_functions.py
    │  ├─ 07_classes
    │  │  ├─ 07_classes.py
    │  │  ├─ boss_model
    │  │  │  ├─ boss.py
    │  │  │  ├─ boss_v1.py
    │  │  │  ├─ boss_v2.py
    │  │  │  └─ __pycache__
    │  │  │     └─ boss.cpython-310.pyc
    │  │  └─ my_project
    │  │     ├─ A
    │  │     │  ├─ aaa.py
    │  │     │  └─ __pycache__
    │  │     │     └─ aaa.cpython-310.pyc
    │  │     ├─ bbb.py
    │  │     ├─ ccc.py
    │  │     └─ __pycache__
    │  │        └─ bbb.cpython-310.pyc
    │  ├─ 08_imports
    │  │  └─ 08_imports.py
    │  ├─ 09_try_except
    │  │  └─ 09_try_except.py
    │  └─ 10_file_handing
    │     └─ 10_file_handing.py
    ├─ README.md
    ├─ Selenium_Practice
    │  ├─ data.json
    │  ├─ my_104_hw
    │  │  ├─ 104_run_log_final.py
    │  │  ├─ 104_run_log_v1.py
    │  │  ├─ 104_run_log_v2.py
    │  │  ├─ data_manager.py
    │  │  ├─ drivers.py
    │  │  └─ __pycache__
    │  │     ├─ data_manager.cpython-310.pyc
    │  │     └─ drivers.cpython-310.pyc
    │  ├─ README.md
    │  ├─ Spring_Festival_hw
    │  │  ├─ basic_practice
    │  │  │  ├─ alert.py
    │  │  │  ├─ hovers.py
    │  │  │  ├─ iframe.py
    │  │  │  └─ shadow_root.py
    │  │  ├─ combination_practice
    │  │  │  ├─ baha_post_list.py
    │  │  │  ├─ file_manager.py
    │  │  │  ├─ logger.py
    │  │  │  └─ __pycache__
    │  │  │     ├─ file_manager.cpython-310.pyc
    │  │  │     └─ logger.cpython-310.pyc
    │  │  └─ __pycache__
    │  │     ├─ file_manager.cpython-310.pyc
    │  │     ├─ gen_log.cpython-310.pyc
    │  │     ├─ logger.cpython-310.pyc
    │  │     └─ log_manager.cpython-310.pyc
    │  └─ __pycache__
    │     ├─ conftest.cpython-310.pyc
    │     ├─ driver.cpython-310.pyc
    │     ├─ drivers.cpython-310.pyc
    │     └─ gen_json.cpython-310.pyc
    └─ web.png
    ```
    """
    st.markdown(project_tree)

    # 模擬讀取 Log 檔案
    if st.button("查看最新 Log"):
        st.code("2026-02-22 [INFO] 啟動瀏覽器...", language="text")

if __name__ == "__main__":
    main()