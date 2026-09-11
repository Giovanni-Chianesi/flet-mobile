# Grade de Produtos

import flet as ft

def card_produto(nome, preco):
    return ft.Container(
        width=140,
        height=140,
        padding=12,
        bgcolor="#FFF3E0",  # Cor de fundo do cartão
        border_radius=12,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
            controls=[
                ft.Icon(ft.Icons.SHOPPING_BAG, size=32, color="#E65100"),  # Ícone
                ft.Text(nome, weight=ft.FontWeight.BOLD, color="#4E342E"),  # Nome
                ft.Text(f"R$ {preco:.2f}", color="#6D4C41"),  # Preço
            ],
        ),
    )

def main(page: ft.Page):
    # Título da Janela
    page.title = "Prateleira"

    # Cor de fundo da página inteira
    page.bgcolor = "#2E1A47"

    # Centraliza os controles
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Define o tamanho da tela
    page.window.width = 320
    page.window.height = 600

    # Padding
    page.padding = ft.Padding(top=60, right=0, bottom=0, left=0)

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
            #scroll=ft.ScrollMode.HIDDEN,  # permite rolar horizontalmente, mas esconde a barra de rolagem
            alignment=ft.MainAxisAlignment.CENTER,  # centraliza os cartões na linha
            # Gera um card_produto para cada item da lista de produtos
            controls=[card_produto(nome, preco) for nome, preco in produtos],
        )
    )

# Inicia a aplicação, chamando a função main() como ponto de entrada
ft.run(main)