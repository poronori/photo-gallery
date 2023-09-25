import flet as ft

# アラート表示用クラス
class AlertView(ft.UserControl) :
    
    dlg = ft.AlertDialog(
            modal=True,
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def __init__(self):
        super().__init__(self)
        AlertView.dlg.actions = [ft.TextButton("Cancel", on_click=AlertView.close)]
    
    def build(self) :
        return self.dlg
    
    @staticmethod
    def open(text) :
        AlertView.dlg.title = ft.Text(text)
        AlertView.dlg.open = True
        AlertView.dlg.update()
        
    @staticmethod
    def close(e) :
        AlertView.dlg.open = False
        AlertView.dlg.update()
    