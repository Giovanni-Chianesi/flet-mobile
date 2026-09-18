# GeoLocalizador

import flet as ft
import httpx

try:
    import flet_geolocator as fg
except ModuleNotFoundError:
    raise SystemExit(
        "Pacote não encontrado. Instale com: "
        "C:\\Users\\Dev_2o_Ano\\AppData\\Local\\Programs\\Python\\Python313\\python.exe -m pip install flet-geolocator"
    )

try:
    Botao = ft.ElevatedButton
except AttributeError:
    Botao = ft.Button


def main(page: ft.Page):
    page.title = "Meu Endereço"
    page.bgcolor = "#101B2D"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    geo = fg.Geolocator()

    if hasattr(page, "services"):
        page.services.append(geo)

    botao = Botao("Obter meu endereço")
    botao.bgcolor = "#4C8BF5"
    botao.color = "#0B1622"

    cartao_endereco = ft.Container(visible=False)

    def linha(rotulo: str, valor: str | None) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Text(rotulo, color="#7F9BC2", width=100),
                ft.Text(valor or "-", color="#E8F0FB", expand=True),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def mostrar_erro(titulo: str, mensagem: str, extras=None):
        if extras is None:
            extras = []

        cartao_endereco.content = ft.Column(
            spacing=6,
            controls=[
                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, color="#4C8BF5"),
                ft.Text(mensagem, color="#E8F0FB"),
                *extras,
            ],
        )
        cartao_endereco.visible = True
        botao.disabled = False
        page.update()

    async def obter_local(e):
        botao.disabled = True
        cartao_endereco.visible = False
        page.update()

        try:
            await geo.request_permission()
            posicao = await geo.get_current_position()
            if posicao is None:
                raise ValueError("posição nula")
        except Exception:
            mostrar_erro(
                "Não foi possível obter a localização",
                "Verifique se a permissão de localização está ativada no dispositivo.",
            )
            return

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resposta = await client.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={"format": "jsonv2", "lat": posicao.latitude, "lon": posicao.longitude},
                    headers={"User-Agent": "meu-app-flet/1.0"},
                )
                resposta.raise_for_status()
                dados = resposta.json()
        except Exception:
            mostrar_erro(
                "Localização encontrada",
                "Não foi possível consultar o endereço, mas suas coordenadas estão disponíveis.",
                extras=[
                    linha("Latitude", str(posicao.latitude)),
                    linha("Longitude", str(posicao.longitude)),
                ],
            )
            return

        endereco = dados.get("address", {})
        if not endereco:
            mostrar_erro(
                "Localização encontrada",
                "Endereço não identificado para estas coordenadas.",
                extras=[
                    linha("Latitude", str(posicao.latitude)),
                    linha("Longitude", str(posicao.longitude)),
                ],
            )
            return

        rua = endereco.get("road")
        numero = endereco.get("house_number")
        rua_numero = f"{rua}, {numero}" if rua and numero else (rua or "-")

        bairro = endereco.get("suburb") or endereco.get("neighbourhood")
        cidade = endereco.get("city") or endereco.get("town") or endereco.get("village")
        estado = endereco.get("state")
        cep = endereco.get("postcode")
        pais = endereco.get("country")

        cartao_endereco.content = ft.Column(
            spacing=6,
            controls=[
                ft.Text("Endereço encontrado", size=16, weight=ft.FontWeight.BOLD, color="#4C8BF5"),
                linha("Rua", rua_numero),
                linha("Bairro", bairro),
                linha("Cidade", cidade),
                linha("Estado", estado),
                linha("CEP", cep),
                linha("País", pais),
            ],
        )
        cartao_endereco.visible = True
        botao.disabled = False
        page.update()

    botao.on_click = obter_local

    page.add(
        ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[botao]),
        cartao_endereco,
    )


ft.run(main)