# Botões Legais eba

import flet as ft

def main(page: ft.Page):
    page.title = "Árvore de controles" # Título que aparece na janela
    
    # Ajuste do tamanho da tela
    page.window.width = 320 # Largura
    page.window.height = 600 # Altura
    
    # Define as cores do fundo da tela
    page.bgcolor = "#0B3D3A"
    
    # Centraliza os elementos na página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Padding
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)
    
    # Container principal que representa o "cartão" visual
    cartao = ft.Container(
        # Conteúdo do cartão organizado em coluna (um item embaixo do outro)
        content=ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Centralizado dentro do cartão
            controls=[
                # Título do cartão: texto maior, negrito e cor de destaque
                ft.Text(
                    "Título do cartão",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#1FE0C4",
                ),
                # Texto discritivo (abaixo do título)
                ft.Text("Descrição do cartão", color="#CFEFE9"),
            
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            "Ação 1",
                            bgcolor="#1FE0C4",
                            color="#0B3D3A",
                        ), # Botãozin de destaque
                        ft.OutlinedButton("Ação 2"), # Botão secundário
                    ]
                ),
            ]
        ),       
        padding=16, # Espaçamento interno entre o conteúdo
        bgcolor="#123C3C", # Cor de fundo ("Row" - Arranjo em linha)
        border_radius=12, # Arrendodamento das beirada
    )
    # Adiciona o cartão à página
    page.add(cartao)

ft.run(main)