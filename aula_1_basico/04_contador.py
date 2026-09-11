import flet as ft

def main(page: ft.Page):
    
    # Título da Janela
    page.title = "Contador"
    
    # Cor de fundo 
    page.bgcolor="#3D0E0E"
    
    # Define tamanho da Janela
    page.window.width = 320
    page.window.height = 600
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Texto que exibe o valor atual
    page.padding= ft.Padding(top=60, bottom=60, left=0, right=0)
    
    contador = ft.Text("0", size=40, color="#FF6B6B", weight=ft.FontWeight.BOLD)
    
    # Váriavel para guardar a contagem
    valor=0
    
    # Funcionalidades
    def somar(e):
        # Uso do "nonlocal para dizer ao Python: quero alterar o valor da váriavel "valor" que foi criada na função
        # "main" sem ter que criar a váriavel
        nonlocal valor
        valor +=1 # Atualização do contador (Mesmo que: "valor = valor + 1" )
        contador.value = str(valor)
        page.update()
        
    def subtrair(e):
        nonlocal valor
        valor -=1 # Atualização do contador (Mesmo que: "valor = valor - 1" )
        contador.value = str(valor)
        page.update()
        
    def resetar(e):
        nonlocal valor
        valor = 0 # Zera a váriavel
        contador.value = str(valor)
        page.update()
        
    # Montagem da página do app
    page.add(
        ft.Row(
            alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(ft.Icons.REMOVE, on_click=subtrair, icon_color="#FF6B6B"),
                contador,
                ft.IconButton(ft.Icons.ADD, on_click=somar, icon_color="#FF6B6B"),
            ],
        ),
        ft.Row(
            alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.TextButton(
                    "resetar",
                    icon=ft.Icons.RESTART_ALT,
                    on_click=resetar,
                    style=ft.ButtonStyle(color="#FFB4B4"),
                ),
            ],
        ),
    )

ft.run(main)