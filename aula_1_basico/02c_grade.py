# Carrosel eba

import flet as ft

def main(page: ft.Page)
    page.title="Prateleira"
    
    page.window.width = 320
    page.window.height = 600
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)
    
    # Tupla
    produtos = [
        ("Caneta", 3.5),
        ("Caderno", 12.9),
        ("Mochila", 89.9),
        ("Estojo", 24.9),
        ("Régua", 5.0),
        ("Borracha", 2.5),
    ]    
    
    page.add(
        ft.Row(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    
def card_produto(nome, preco):
    return ft.Container(
        width=140,
        height=140,
        padding=12,
        bgcolor="#fff3E0",
        border_radius=12,
        content=ft.Column(
            # Alinhamento horizontal
            alignment=ft.MainAxisAlignment.CENTER,
            # Alinhamento vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.icons.SHOPPING_BAG, size=22, color="#E65100")
                ft.Text(nome, weight=ft.FontWeight.BOLD, color="#4E342E"),
                ft.Text(f"R$ {preco:.2f}", color="#6D4C41")
            ]
        )
        
    )