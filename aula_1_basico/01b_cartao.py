# Cartão de apresentação pessoal

import flet as ft

def main(page: ft.Page):
    page.title = "Cartão de apresentação"
    
    # Ajuste do tamanho da tela
    page.window.width = 320
    page.window.height = 600
    
    # Define as cores da tela
    page.bgcolor = "#2B1B3D"
    
    # Ajusta para centralizar os elementos
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Padding
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)
    
    # Criação dos elementos da página
    page.add( # Palavra em Destaque
        ft.Text(
            "Avenida Itamarai 1665",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="#C01707",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text( # Outra palavra
            "Drogaria Leão que eu gosto de montão!",
            size=14,
            color="#EDA0A0",
            text_align=ft.TextAlign.CENTER,
        ),
    )
# Inicia a aplicação
ft.run(main)