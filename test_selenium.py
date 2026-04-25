from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from monitor.models import Incidente
import time

URL_HOME           = "/"
URL_LOGIN          = "/login/"
URL_HISTORICO      = "/historico/"
URL_REGISTRAR      = "/registrar-novo/"
URL_INCIDENTES     = "/incidentes-ativos/"
URL_CADASTRO_ALUNO = "/cadastro/"
URL_LOGOUT         = "/logout/"

CAMPO_USUARIO  = "username"
CAMPO_SENHA    = "password"
BOTAO_SUBMIT   = "button[type='submit']"

ADMIN_USER  = "ti_teste"
ADMIN_EMAIL = "ti@cesar.school"
ADMIN_PASS  = "senha_ti_123"


def configurar_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    browser.implicitly_wait(5)
    return browser


def criar_admin():
    return User.objects.create_superuser(
        username=ADMIN_USER,
        email=ADMIN_EMAIL,
        password=ADMIN_PASS
    )

def criar_aluno():
    user, created = User.objects.get_or_create(username="aluno_teste")
    if created:
        user.set_password("senha_aluno_123")
        user.save()
    return user


class SCRUM19_VisualizarStatusSistemas(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = configurar_browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.aluno = criar_aluno()
        Incidente.objects.create(
            sistema='Portal do Aluno',
            status='Funcionando',
            descricao='Teste para Aluno',
            resolvido=False
        )

    def _fazer_login_aluno(self):
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)

        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys("aluno_teste")
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys("senha_aluno_123")
        time.sleep(1)
        
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2) 

    def test_aluno_visualiza_status_na_home(self):
        """Aluno logado deve ver o status dos sistemas na página inicial."""
        self._fazer_login_aluno()

        self.browser.get(self.live_server_url + URL_HOME)
        time.sleep(1)
        
        corpo = self.browser.find_element(By.TAG_NAME, "body").text.lower()

        self.assertIn("status", corpo, "O Aluno não conseguiu ver a seção de status.")
        
        termos_esperados = ["funcionando", "operando normalmente", "portal do aluno"]
        tem_status = any(termo in corpo for termo in termos_esperados)
        
        self.assertTrue(tem_status, "O Aluno não encontrou indicadores de status na página.")
        time.sleep(2) 