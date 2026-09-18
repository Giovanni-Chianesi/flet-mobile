# Lista com 3 dicts de tarefas (`id`, `title`, `done`)

import flet as ft
import httpx

def main(page: ft.Page):
    # Título que aparece na Janela
    page.title = "Tarefas da API"

    # Cor de fundo da página
    page.bgcolor = "#101B2D"

    # Centraliza horizontalmente
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Padding vertical de 60px (topo e base)
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Lista onde os títulos das tarefas buscadas na API serão exibidos
    lista_view = ft.ListView(expand=True, spacing=6, width=320)

    async def carregar(e):
        # "async def": esta função usa "await" para não travar o app enquanto
        # espera a resposta da rede (entraremos em detalhes no próximo bloco)
        lista_view.controls.clear()
        async with httpx.AsyncClient() as client:
            resposta = await client.get(
                "https://jsonplaceholder.typicode.com/todos", params={"_limit": 10}
            )
            dados = resposta.json()  # texto JSON -> lista de dicts Python (json.loads por baixo dos panos)
        for tarefa in dados:
            lista_view.controls.append(ft.Text(f"• {tarefa['title']}", color="#CDE0F2"))
        page.update()

    page.add(
        ft.ElevatedButton("Carregar tarefas", on_click=carregar, bgcolor="#4C8BF5", color="#0B1622"),
        lista_view,
    )

ft.run(main)