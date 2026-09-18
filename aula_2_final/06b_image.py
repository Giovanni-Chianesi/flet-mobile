# Exibidor de foto da máquina

import os
import tkinter as tk
from tkinter import filedialog

import flet as ft


def main(page: ft.Page):
    page.title = "Escolher Foto"
    page.bgcolor = "#1B1F3B"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    caminho_input = ft.TextField(
        label="Caminho da imagem",
        hint_text="Ex.: C:\\fotos\\minha_foto.jpg",
        width=360,
    )

    placeholder = ft.Container(
        width=220,
        height=220,
        border_radius=16,
        bgcolor="#232A4D",
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=52, color="#5C7CFA"),
    )

    coluna_imagem = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[placeholder],
    )

    def mostrar_imagem(caminho: str):
        if not caminho or not os.path.exists(caminho):
            placeholder.content = ft.Icon(ft.Icons.ERROR_OUTLINE, size=52, color="#FF6B6B")
            page.update()
            return

        coluna_imagem.controls = [
            ft.Container(
                width=220,
                height=220,
                border_radius=16,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Image(
                    src=caminho,
                    width=220,
                    height=220,
                    fit=ft.BoxFit.COVER,
                ),
            )
        ]
        page.update()

    def abrir_arquivo():
        root = tk.Tk()
        root.withdraw()
        caminho = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[
                ("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp"),
                ("Todos os arquivos", "*.*"),
            ],
        )
        root.destroy()

        if caminho:
            caminho_input.value = caminho
            mostrar_imagem(caminho)
            page.update()

    def escolher_foto(e):
        caminho = caminho_input.value.strip()
        if caminho:
            mostrar_imagem(caminho)
            return

        abrir_arquivo()

    botao = ft.Button("Escolher foto", on_click=escolher_foto, icon=ft.Icons.PHOTO_LIBRARY)
    botao.bgcolor = "#5C7CFA"
    botao.color = "#161B33"

    botao_arquivo = ft.Button("Procurar no PC", on_click=lambda e: abrir_arquivo())
    botao_arquivo.bgcolor = "#3949AB"
    botao_arquivo.color = "#FFFFFF"

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[botao, botao_arquivo],
        ),
        caminho_input,
        coluna_imagem,
    )

ft.run(main)