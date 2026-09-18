# 

import json
import os

import flet as ft
import httpx

API = "https://jsonplaceholder.typicode.com/todos"
STORAGE_FILE = "tarefas_local.json"

PRIORITY_COLOR = {"alta": "#FF6B6B", "media": "#F2C94C", "baixa": "#6FCF97"}
PRIORITY_LABEL = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}
PRIORITY_ORDER = {"alta": 0, "media": 1, "baixa": 2}

BG_LISTA = "#161B33"
BG_NOVA = "#241B3D"
BG_DETALHE = "#1B2E3D"
BG_DESTAQUE = "#5C7CFA"

Btn = ft.ElevatedButton if hasattr(ft, "ElevatedButton") else ft.Button


def storage_path():
    return os.path.join(os.path.dirname(__file__), STORAGE_FILE)


def load_local_tasks():
    path = storage_path()
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


async def save_local_tasks(tasks):
    path = storage_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False)


async def main(page: ft.Page):
    page.title = "App de Tarefas Online"
    page.bgcolor = "#161B33"

    tasks = []
    next_id = 1
    search_query = ""
    view_name = "lista"
    selected_task = None

    page.snack_bar = ft.SnackBar(content=ft.Text(""))
    page.dialog = None

    def show_message(msg: str):
        page.snack_bar.content = ft.Text(msg)
        page.snack_bar.open = True
        page.update()

    def tarefas_visiveis():
        termo = search_query.strip().lower()
        filtradas = [t for t in tasks if termo in t["title"].lower()]
        return sorted(filtradas, key=lambda t: PRIORITY_ORDER[t["priority"]])

    async def salvar_local():
        await save_local_tasks(tasks)

    async def carregar_inicial():
        nonlocal tasks, next_id

        dados_locais = load_local_tasks()
        if dados_locais:
            tasks = dados_locais
            next_id = max((t["id"] for t in tasks), default=0) + 1
            return

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resposta = await client.get(API, params={"_limit": 8})
                resposta.raise_for_status()
                dados = resposta.json()

            tasks = [
                {
                    "id": i,
                    "title": item["title"],
                    "description": "Tarefa importada da API.",
                    "priority": "media",
                    "done": bool(item["completed"]),
                }
                for i, item in enumerate(dados, start=1)
            ]
            next_id = max((t["id"] for t in tasks), default=0) + 1
            await salvar_local()
        except Exception:
            tasks = []
            show_message("Sem conexão — iniciando com lista vazia.")

    def build_task_row(t):
        def ir_para_detalhe(e):
            nonlocal selected_task
            selected_task = t
            view_name = "detalhe"
            render()

        async def alternar_concluida(e):
            t["done"] = bool(e.control.value)
            await salvar_local()
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    await client.patch(f"{API}/{t['id']}", json={"completed": t["done"]})
            except Exception:
                pass
            render()

        return ft.Container(
            padding=12,
            border_radius=10,
            bgcolor="#232A4D",
            content=ft.Row(
                controls=[
                    ft.Checkbox(value=t["done"], on_change=alternar_concluida, active_color=BG_DESTAQUE),
                    ft.Container(width=10, height=10, border_radius=5, bgcolor=PRIORITY_COLOR[t["priority"]]),
                    ft.Text(t["title"], expand=True, color="#6E7695" if t["done"] else "#E9ECFB"),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#8892C4"),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            on_click=ir_para_detalhe,
        )

    def render():
        nonlocal view_name, selected_task

        page.controls.clear()

        if view_name == "lista":
            contador = ft.Text(
                value=f"{sum(1 for t in tasks if t['done'])} de {len(tasks)} tarefas concluídas",
                color="#8892C4",
                size=13,
            )

            campo_busca = ft.TextField(
                label="Buscar por título",
                value=search_query,
                width=320,
                on_change=lambda e: (
                    setattr(__import__("builtins"), "_search", e.control.value),
                    _apply_search(e.control.value),
                ),
            )

            def _apply_search(value):
                nonlocal search_query
                search_query = value
                render()

            lista = ft.ListView(expand=True, spacing=8, width=340)
            for t in tarefas_visiveis():
                lista.controls.append(build_task_row(t))

            page_controls = [
                ft.Column(
                    controls=[
                        contador,
                        campo_busca,
                        lista,
                    ],
                    spacing=10,
                    expand=True,
                )
            ]

            page.controls.extend(page_controls)
            page.floating_action_button = ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                on_click=lambda e: (setattr(__import__("builtins"), "_view", "nova"), set_view("nova")),
                bgcolor=BG_DESTAQUE,
            )

        elif view_name == "nova":
            titulo = ft.TextField(label="Título", width=320)
            descricao = ft.TextField(label="Descrição", multiline=True, min_lines=3, width=320)
            prioridade = ft.Dropdown(
                width=320,
                value="media",
                options=[
                    ft.DropdownOption("alta", "Alta"),
                    ft.DropdownOption("media", "Média"),
                    ft.DropdownOption("baixa", "Baixa"),
                ],
            )

            async def salvar_nova(e):
                nonlocal next_id, view_name
                if not titulo.value.strip():
                    titulo.error_text = "Informe um título"
                    page.update()
                    return

                nova = {
                    "id": next_id,
                    "title": titulo.value.strip(),
                    "description": descricao.value.strip(),
                    "priority": prioridade.value,
                    "done": False,
                }

                tasks.append(nova)
                next_id += 1
                await salvar_local()
                try:
                    async with httpx.AsyncClient(timeout=10) as client:
                        await client.post(API, json={"title": nova["title"], "completed": False, "userId": 1})
                except Exception:
                    pass

                view_name = "lista"
                render()
                show_message("Tarefa criada com sucesso!")

            page.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("Nova tarefa", size=22, weight=ft.FontWeight.BOLD, color="#D6E8F0"),
                        titulo,
                        descricao,
                        ft.Text("Prioridade:", color="#D8CFF2"),
                        prioridade,
                        Btn("Salvar", on_click=salvar_nova, bgcolor=BG_DESTAQUE, color="#161B33"),
                        ft.TextButton("Voltar", on_click=lambda e: (set_view("lista"))),
                    ],
                    spacing=12,
                    width=360,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        elif view_name == "detalhe":
            if selected_task is None:
                page.controls.append(ft.Text("Tarefa não encontrada", color="#D6E8F0"))
            else:
                t = selected_task

                async def excluir_tarefa(e):
                    nonlocal view_name, selected_task
                    tasks[:] = [x for x in tasks if x["id"] != t["id"]]
                    await salvar_local()
                    try:
                        async with httpx.AsyncClient(timeout=10) as client:
                            await client.delete(f"{API}/{t['id']}")
                    except Exception:
                        pass
                    selected_task = None
                    view_name = "lista"
                    render()
                    show_message("Tarefa excluída.")

                async def editar_tarefa(e):
                    nonlocal view_name
                    view_name = "editar"
                    render()

                if view_name == "detalhe":
                    page.controls.append(
                        ft.Column(
                            controls=[
                                ft.Text(t["title"], size=22, weight=ft.FontWeight.BOLD, color="#D6E8F0"),
                                ft.Row(
                                    controls=[
                                        ft.Container(width=12, height=12, border_radius=6, bgcolor=PRIORITY_COLOR[t["priority"]]),
                                        ft.Text(f"Prioridade {PRIORITY_LABEL[t['priority']]}", color="#A9C7D6"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Text(t["description"] or "(sem descrição)", color="#D6E8F0", text_align=ft.TextAlign.CENTER),
                                ft.Row(
                                    controls=[
                                        Btn("Editar", on_click=editar_tarefa, bgcolor=BG_DESTAQUE, color="#161B33"),
                                        Btn("Excluir", on_click=excluir_tarefa, bgcolor="#FF6B6B", color="#1B2E3D"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.TextButton("Voltar", on_click=lambda e: (set_view("lista"))),
                            ],
                            spacing=12,
                            width=360,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    )

        elif view_name == "editar":
            if selected_task is None:
                view_name = "lista"
                render()
                return

            t = selected_task
            titulo = ft.TextField(label="Título", value=t["title"], width=320)
            descricao = ft.TextField(label="Descrição", value=t["description"], multiline=True, min_lines=3, width=320)
            prioridade = ft.Dropdown(
                width=320,
                value=t["priority"],
                options=[
                    ft.DropdownOption("alta", "Alta"),
                    ft.DropdownOption("media", "Média"),
                    ft.DropdownOption("baixa", "Baixa"),
                ],
            )

            async def salvar_editar(e):
                nonlocal view_name, selected_task
                if not titulo.value.strip():
                    titulo.error_text = "Informe um título"
                    page.update()
                    return

                t["title"] = titulo.value.strip()
                t["description"] = descricao.value.strip()
                t["priority"] = prioridade.value

                await salvar_local()
                try:
                    async with httpx.AsyncClient(timeout=10) as client:
                        await client.put(f"{API}/{t['id']}", json={"title": t["title"], "completed": t["done"], "userId": 1})
                except Exception:
                    pass

                selected_task = t
                view_name = "detalhe"
                render()
                show_message("Tarefa atualizada!")

            page.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("Editar tarefa", size=22, weight=ft.FontWeight.BOLD, color="#D6E8F0"),
                        titulo,
                        descricao,
                        ft.Text("Prioridade:", color="#D8CFF2"),
                        prioridade,
                        Btn("Salvar alterações", on_click=salvar_editar, bgcolor=BG_DESTAQUE, color="#161B33"),
                        ft.TextButton("Voltar", on_click=lambda e: (set_view("detalhe"))),
                    ],
                    spacing=12,
                    width=360,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    def set_view(name):
        nonlocal view_name
        view_name = name
        render()

    await carregar_inicial()
    render()

ft.run(main)