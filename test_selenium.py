from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
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
URL_GERENCIAR      = "/gerenciar/"

CAMPO_USUARIO  = "username"
CAMPO_SENHA    = "password"
BOTAO_SUBMIT        = "button[type='submit']"
BOTAO_ENVIAR_FORM   = "button.btn-enviar"

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


# -------------------------------------------------------
# HISTÓRIA 1 - MEMBRO DE TI REGISTRA NOVO INCIDENTE
# -------------------------------------------------------
class SCRUM_Historia1_RegistrarIncidente(StaticLiveServerTestCase):
    """
    História 1:
    Como membro da equipe de TI, gostaria de registrar um novo incidente
    no sistema, para informar a comunidade acadêmica sobre instabilidades.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = configurar_browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        # Recria admin e limpa cookies a cada teste para garantir sessão limpa
        self.admin = criar_admin()
        self.browser.delete_all_cookies()

    def tearDown(self):
        User.objects.all().delete()
        Incidente.objects.all().delete()

    def _fazer_login_admin(self):
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys(ADMIN_USER)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys(ADMIN_PASS)
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)

    def test_ti_registra_incidente_instavel(self):
        """Membro de TI registra incidente instável e ele aparece no dashboard."""
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_INCIDENTES)
        time.sleep(1)
        Select(self.browser.find_element(By.NAME, 'sistema')).select_by_visible_text('Lyceum')
        time.sleep(1)
        Select(self.browser.find_element(By.NAME, 'status')).select_by_visible_text('Instável')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'descricao').send_keys('Sistema com lentidão desde as 14h.')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_ENVIAR_FORM).click()
        time.sleep(2)
        self.assertIn(URL_HOME, self.browser.current_url)
        corpo = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Lyceum', corpo)
        time.sleep(2)

    def test_ti_registra_incidente_fora_do_ar(self):
        """Membro de TI registra incidente fora do ar e indicador vermelho aparece."""
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_INCIDENTES)
        time.sleep(1)
        Select(self.browser.find_element(By.NAME, 'sistema')).select_by_visible_text('Portal do Aluno')
        time.sleep(1)
        Select(self.browser.find_element(By.NAME, 'status')).select_by_visible_text('Fora do Ar')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'descricao').send_keys('Portal completamente fora do ar.')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_ENVIAR_FORM).click()
        time.sleep(2)
        pontos_vermelhos = self.browser.find_elements(By.CSS_SELECTOR, '.ponto.vermelho')
        self.assertGreater(len(pontos_vermelhos), 0)
        time.sleep(2)

    def test_ti_registra_incidente_instavel_indicador_amarelo(self):
        """Incidente instável aparece com indicador amarelo no dashboard."""
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_INCIDENTES)
        time.sleep(1)
        Select(self.browser.find_element(By.NAME, 'sistema')).select_by_visible_text('Chamada')
        time.sleep(1)
        Select(self.browser.find_element(By.NAME, 'status')).select_by_visible_text('Instável')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'descricao').send_keys('Chamada instável.')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_ENVIAR_FORM).click()
        time.sleep(2)
        pontos_amarelos = self.browser.find_elements(By.CSS_SELECTOR, '.ponto.amarelo')
        self.assertGreater(len(pontos_amarelos), 0)
        time.sleep(2)


# -------------------------------------------------------
# HISTÓRIA 2 - TELA DE LOGIN PARA ALUNO E ADMIN
# -------------------------------------------------------
class SCRUM_Historia2_TelaLogin(StaticLiveServerTestCase):
    """
    História 2:
    Criação de uma tela de login para o usuário logar
    como um aluno ou um ADMIN entrar no sistema.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = configurar_browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.admin = criar_admin()
        self.aluno = criar_aluno()
        self.browser.delete_all_cookies()

    def tearDown(self):
        User.objects.all().delete()

    def test_tela_login_e_a_primeira_tela(self):
        """A tela de login é a primeira tela que o usuário vê."""
        self.browser.get(self.live_server_url + URL_HOME)
        time.sleep(1)
        self.assertIn(URL_LOGIN, self.browser.current_url)
        time.sleep(2)

    def test_aluno_consegue_fazer_login(self):
        """Aluno comum consegue fazer login e acessar o dashboard."""
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys('aluno_teste')
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys('senha_aluno_123')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)
        self.assertIn(URL_HOME, self.browser.current_url)
        time.sleep(2)

    def test_admin_consegue_fazer_login_e_ve_botoes_exclusivos(self):
        """Admin consegue fazer login e vê botões exclusivos no dashboard."""
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys(ADMIN_USER)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys(ADMIN_PASS)
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)
        corpo = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Cadastrar Usuário', corpo)
        self.assertIn('Gerenciar Incidentes', corpo)
        time.sleep(2)

    def test_aluno_nao_ve_botoes_de_admin(self):
        """Aluno não vê botões exclusivos de admin no dashboard."""
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys('aluno_teste')
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys('senha_aluno_123')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)
        corpo = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Cadastrar Usuário', corpo)
        self.assertNotIn('Gerenciar Incidentes', corpo)
        time.sleep(2)

    def test_login_incorreto_exibe_erro(self):
        """Login com credenciais erradas exibe mensagem de erro."""
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys('usuario_errado')
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys('senha_errada')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)
        corpo = self.browser.find_element(By.TAG_NAME, 'body').text.lower()
        self.assertIn('incorretos', corpo)
        time.sleep(2)

    def test_nome_usuario_aparece_na_navbar(self):
        """Nome do usuário logado aparece no canto superior da tela."""
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys(ADMIN_USER)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys(ADMIN_PASS)
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)
        username_elemento = self.browser.find_element(By.CSS_SELECTOR, '.username')
        self.assertIn(ADMIN_USER, username_elemento.text)
        time.sleep(2)


# -------------------------------------------------------
# HISTÓRIA 3 - ADMIN CADASTRA NOVO ALUNO
# -------------------------------------------------------
class SCRUM_Historia3_CadastrarAluno(StaticLiveServerTestCase):
    """
    História 3:
    Como ADMIN, gostaria de criar um cadastro de um aluno novo
    usando Email + Senha.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = configurar_browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.admin = criar_admin()
        self.browser.delete_all_cookies()

    def tearDown(self):
        User.objects.all().delete()

    def _fazer_login_admin(self):
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys(ADMIN_USER)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys(ADMIN_PASS)
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)

    def test_admin_acessa_tela_de_cadastro(self):
        """Admin consegue acessar a tela de cadastro de usuários."""
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_CADASTRO_ALUNO)
        time.sleep(1)
        self.assertIn(URL_CADASTRO_ALUNO, self.browser.current_url)
        time.sleep(2)

    def test_admin_cadastra_novo_aluno_com_sucesso(self):
        """Admin preenche email e senha e cadastra um novo aluno com sucesso."""
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_CADASTRO_ALUNO)
        time.sleep(1)
        self.browser.find_element(By.NAME, 'email').send_keys('novo@cesar.school')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password1').send_keys('senha123')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password2').send_keys('senha123')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_ENVIAR_FORM).click()
        time.sleep(2)
        corpo = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('cadastrado com sucesso', corpo)
        self.assertTrue(User.objects.filter(username='novo@cesar.school').exists())
        time.sleep(2)

    def test_cadastro_senhas_diferentes_exibe_erro(self):
        """Senhas diferentes exibem mensagem de erro no cadastro."""
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_CADASTRO_ALUNO)
        time.sleep(1)
        self.browser.find_element(By.NAME, 'email').send_keys('erro@cesar.school')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password1').send_keys('senha123')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password2').send_keys('diferente456')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_ENVIAR_FORM).click()
        time.sleep(2)
        corpo = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('não coincidem', corpo)
        time.sleep(2)

    def test_cadastro_email_duplicado_exibe_erro(self):
        """Tentar cadastrar email já existente exibe mensagem de erro."""
        User.objects.create_user(username='existente@cesar.school', password='senha123')
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_CADASTRO_ALUNO)
        time.sleep(1)
        self.browser.find_element(By.NAME, 'email').send_keys('existente@cesar.school')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password1').send_keys('qualquer123')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password2').send_keys('qualquer123')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_ENVIAR_FORM).click()
        time.sleep(2)
        corpo = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Já existe', corpo)
        time.sleep(2)

    def test_novo_aluno_cadastrado_consegue_fazer_login(self):
        """Aluno cadastrado pelo admin consegue fazer login no sistema."""
        self._fazer_login_admin()
        self.browser.get(self.live_server_url + URL_CADASTRO_ALUNO)
        time.sleep(1)
        self.browser.find_element(By.NAME, 'email').send_keys('novinho@cesar.school')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password1').send_keys('senha456')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password2').send_keys('senha456')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)

        # Logout via URL direta com POST simulado — limpa cookies
        self.browser.delete_all_cookies()
        time.sleep(1)

        # Login com novo aluno
        self.browser.get(self.live_server_url + URL_LOGIN)
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_USUARIO).send_keys('novinho@cesar.school')
        time.sleep(1)
        self.browser.find_element(By.NAME, CAMPO_SENHA).send_keys('senha456')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, BOTAO_SUBMIT).click()
        time.sleep(2)
        self.assertIn(URL_HOME, self.browser.current_url)
        time.sleep(2)
        