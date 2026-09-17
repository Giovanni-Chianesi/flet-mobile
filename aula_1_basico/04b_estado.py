# Mudança do Estado da Page Light/Dark

import flet as ft

def main(page: ft.Page):
    # Configs Iniciais
    page.title="Modo Claro/Escuro"
    page.theme_mode = ft.ThemeMode.LIGHT # Inicia o modo Claro
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER # Centraliza Tudo
    
    # Função que redesenha toda a tela se o tema for trocado
    def construir_tela():
        page.controls.clear() # Limpa a tela antes de recriar o app
        
        escuro = page.theme_mode == ft.ThemeMode.DARK # Modo Dark
        
        # Define o ícone cores e texto de acordo com o tema atual
        icone = ft.Icon(
            ft.Icons.LIGHT_MODE if escuro else ft.Icons.DARK_MODE,
            size=60,
            color=ft.Colors.AMBER if escuro else ft.Colors.BLUE_200,
        )
        text = ft.Text(
            "Modo Escuro ativado" if escuro else "Modo Claro Ativado",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE if escuro else ft.Colors.BLACK,
        )
        botao = ft.ElevatedButton(
            "Ativar Modo Claro" if escuro else "Ativar Modo Escuro",
            on_click=alternar_tema,
        )
        
        # Cor de fundo da tela
        page.bgcolor = ft.Colors.BLACK if escuro else ft.Colors.WHITE
        
        # Adiciona os elementos centralizados
        page.add(
            ft.Column(
                [ft.Container(height=60), icone, text, botao],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )
        
        page.update()
        
    def alternar_tema(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        
        # Forma tradicional
        # if page.theme_mode == ft.ThemeMode.LIGHT:
        #     page.theme_mode = ft.ThemeMoed.DARK
        # else:
        #     page.theme_mode = ft.ThemeMode.LIGHT
        
        construir_tela() # Usado toda vez que usuário clicar para reconstruir
    construir_tela() # Chama a tela pela primeira vez
    
# Inicia o aplicativo
ft.app(target=main)
