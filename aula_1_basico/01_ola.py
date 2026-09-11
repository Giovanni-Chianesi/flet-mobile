# Básico "Hello World"

import flet as ft

def main(page: ft.Page):
    page.title = "Meu Primeiro App Flet"
    page.add(ft.Text("Olá, Mundinho!"))

ft.run(main)