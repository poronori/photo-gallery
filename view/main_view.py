import flet as ft
import glob
import os
import tkinter as tk
import tkinter.filedialog
from .alert_view import AlertView
from .image_list_view import ImageDataListView


def main(page):
    
    page.title = "画像一覧表示"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    alart = AlertView()
    main_view = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    def addImageList(imageList: ImageDataListView):
        main_view.controls.append(imageList)
        page.update()
        
    def getButtonClick(e):
        root = tk.Tk()
        root.attributes('-topmost', True) #ダイアログを最前面に表示
        root.withdraw()
        # フォルダ選択
        target_dir = tkinter.filedialog.askdirectory(mustexist=True)
        dirs = getFiles(target_dir)
        
        for key, value in dirs.items():
            imageList = ImageDataListView(key, value, openDialog)
            addImageList(imageList)
    
    def openDialog(dlg:ft.AlertDialog):
        page.dialog = dlg
        dlg.open = True
        page.update()

    get_button = ft.ElevatedButton("フォルダを選択", icon=ft.icons.CLOUD_CIRCLE, on_click=getButtonClick)
    page.add(
        ft.Column(
            expand=True,
            controls=
            [
                get_button,
                main_view
            ]
        )
    )
    page.add(alart)
    page.dialog = alart
    page.update()
    # dir配下の画像ファイルをフォルダ毎に取得
    def getFiles(dir):
        # フォルダの読込み
        files = glob.glob(dir + '/**', recursive=True)
        dirs = {}  #辞書型でフォルダ毎にファイルパスを保持
        for file in files:
            if os.path.isfile(file):
                # 拡張子を取得
                root, ext = os.path.splitext(file)
                # 画像ファイルをフォルダ毎にセット
                if ext == ".jpg" or ext == ".png" or ext == ".jpeg" or ext == ".bmp":
                    dirname = os.path.dirname(file)
                    dirs.setdefault(dirname, []).append(file)
            
        return dirs