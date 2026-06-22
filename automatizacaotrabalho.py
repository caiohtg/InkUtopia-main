import pytest
from playwright.sync_api import Page, expect

BASE_URL = "file:///C:/Users/Windows10/Downloads/InkUtopia-main/src"

# ===== TESTES DE LOGIN =====
def test_login_page_carrega(page: Page):
    page.goto(f"{BASE_URL}/pages/login.html")
    expect(page.locator("h1")).to_contain_text("ENTRAR")

def test_login_campos_visiveis(page: Page):
    page.goto(f"{BASE_URL}/pages/login.html")
    expect(page.locator("input#email")).to_be_visible()
    expect(page.locator("input#password")).to_be_visible()
    expect(page.locator('button[type="submit"]')).to_be_visible()

# ===== TESTES DE CADASTRO DO TATUADOR =====
def test_perfil_tatuador_carrega(page: Page):
    page.goto(f"{BASE_URL}/pages/perfilArtista.html")
    expect(page.locator("#artistName")).to_be_visible()

def test_aba_agenda_visivel(page: Page):
    page.goto(f"{BASE_URL}/pages/perfilArtista.html")
    page.click("text=Agenda")
    expect(page.locator("#scheduleTab")).to_be_visible()

def test_configuracoes_tatuador(page: Page):
    page.goto(f"{BASE_URL}/pages/perfilArtista.html")
    page.click("text=Configurações")
    expect(page.locator(".form-input").first).to_be_visible()