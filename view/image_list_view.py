import flet as ft

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
        for file in files:
            self.add_image(file, openDialog)
    
    # 画像を1枚ずつ追加
    def add_image(self, image, openDialog):
        imageView = ImageDataView(image, openDialog)
        self.imageListView.controls.append(imageView)
    
    def build(self):
        return ft.Column(
            controls=[
                ft.Text(self.dir),
                self.imageListView
            ]
        )

#個別の画像ビュー
class ImageDataView(ft.UserControl):
    
    def __init__(self, image, openDialog):
        super().__init__(self)
        self.img = ft.TextButton(
            content=ft.Image(
                src=image,
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
            ),
            on_click=lambda _: self.imageClick(image, openDialog)
        )
    
    def imageClick(e, image, openDialog):
        dlg = ft.AlertDialog(
            content = ft.Image(src=image)
        )
        openDialog(dlg)
    
    def build(self):
        return self.img
