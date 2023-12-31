import flet as ft
import subprocess

# 画像一覧のビュー
class ImageDataListView(ft.UserControl):
    
    def __init__(self, dir, files, openDialog):
        super().__init__(self)
        self.dir = dir
        self.imageListView = ft.GridView(
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )
        self.column = ft.Column(
            controls=[
                ft.TextButton(
                    text=self.dir,
                    on_click=lambda _: self.open_dir(self.dir)
                ),
                self.imageListView
            ]
        )
        for file in files:
            self.add_image(file, openDialog)
    
    # 画像を1枚ずつ追加
    def add_image(self, image, openDialog):
        imageView = ImageDataView(image, openDialog)
        self.imageListView.controls.append(imageView)
    
    # フォルダを開く
    def open_dir(e, dir):
        subprocess.Popen(['start', dir], shell=True)
    
    def build(self):
        return self.column

#個別の画像ビュー
class ImageDataView(ft.UserControl):
    
    def __init__(self, image, openDialog):
        super().__init__(self)
        self.img = ft.TextButton(
            content=ft.Image(
                src=image,
                width=150,
                height=150,
                fit=ft.ImageFit.COVER,
            ),
            on_click=lambda _: self.imageClick(image, openDialog),
            style=ft.ButtonStyle(
                padding=0
            )
        )
    
    def imageClick(e, image, openDialog):
        dlg = ft.AlertDialog(
            content = ft.Image(src=image)
        )
        openDialog(dlg)
    
    def build(self):
        return self.img
