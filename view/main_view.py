import flet as ft
import glob
import os
import tkinter as tk
import tkinter.filedialog
from .alert_view import AlertView
from .image_list_view import ImageDataListView

dirs = {}       # {フォルダ名, ファイル一覧}
index = [0,0]   # 読込みしたファイルの位置記録用 [フォルダの位置, ファイルの位置]

def main(page):
    
    page.title = "画像一覧表示"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    
    alart = AlertView()
    main_view = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    # 表示画像の追加
    def addImage():
        global dirs
        global index
        print('フォルダの数：' + str(len(dirs)))
        start = index[1]
        next_flg = True
        # フォルダ毎に画像を読み取る
        for i in range(index[0], len(dirs)):
            dir = list(dirs.keys())[i]
            print('フォルダ名：' + dir)
            files = dirs.get(dir)
            print('ファイルの数：' + str(len(files)))
            
            count = 0
            for j in range(start, len(files)):
                count += 1
                if count >= 100:
                    index[1] = j   # ファイルの位置記録
                    next_flg = False
                    break
            
            if next_flg:
                index[0] += 1   # フォルダを進める
                index[1] = 0
            else:
                imageList = ImageDataListView(dir, files[start:index[1]], openDialog)
                # 途中から読み込む場合はフォルダ名の部分は削除
                if start > 0:
                    imageList.column.controls.pop(0)
                addImageList(imageList)
                main_view.controls.append(add_button)
                page.update()
                break
            
            imageList = ImageDataListView(dir, files[start:], openDialog)
            # 途中から読み込む場合はフォルダ名の部分は削除
            if start > 0:
                imageList.column.controls.pop(0)
            addImageList(imageList)
            start = 0
            
    def addImageList(imageList: ImageDataListView):
        main_view.controls.append(imageList)
        page.update()
        
    def getButtonClick(e):
        root = tk.Tk()
        root.attributes('-topmost', True) #ダイアログを最前面に表示
        root.withdraw()
        
        # フォルダ選択
        target_dir = tkinter.filedialog.askdirectory(mustexist=True)
        main_view.controls = [] # 表示項目の初期化
        global dirs
        global index
        dirs = getFiles(target_dir)
        index = [0, 0]
        addImage()
        
        root.mainloop()
    
    #プレビュー表示用　画像をアラートで表示させる
    def openDialog(dlg:ft.AlertDialog):
        page.dialog = dlg
        dlg.open = True
        page.update()

    def addButtonClick(e):
        main_view.controls.pop()
        addImage()
    
    get_button = ft.ElevatedButton("フォルダを選択", icon=ft.icons.FOLDER_OUTLINED, on_click=getButtonClick)
    add_button = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls = [ft.ElevatedButton("さらに読み込む", icon=ft.icons.ADD_OUTLINED, on_click=addButtonClick)]
    )
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
                ext = ext.lower()
                # 画像ファイルをフォルダ毎にセット
                if ext == ".jpg" or ext == ".png" or ext == ".jpeg" or ext == ".bmp":
                    dirname = os.path.dirname(file)
                    dirs.setdefault(dirname, []).append(file)
            
        return dirs