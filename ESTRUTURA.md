## Arquitetura do Projeto

### Na raiz do projeto
`requirements.txt` - Bibliotecas que o servidor de produção vai precisar instalar.

`manage.py`: Usado para rodar o servidor(python manage.py runserver).

### Pasta `setup/` (Painel de Controle)
`settings.py`: Onde configuramos o banco de dados, senhas, fuso horário e avisamos ao Django quais apps estão instalados.

`urls.py`: O "roteador" principal. Recebe o link que o usuário digitou e direciona para o lugar certo.

`wsgi.py ` e `asgi.py`:  São configurados para o servidor em nuvem. Não editaremos eles.

### Pasta `monitor/` (Nosso App)
Aqui é onde toda lógica de, *monitoramento, incidentes e cálculos* do sistema fica. Onde aplicamos MVT na prática.

`models.py`: **("M" do MVT):** Nosso banco de dados! Vai ser aqui onde, *escrevemos as regras das tabelas (Sistema e incidentes)* usando classes em Python.

`views.py`: **("V" do MVT)**: É aqui onde o Python vai buscar o banco de dados, faz cálculos matemáticos e envia o resultado para as telas.

`urls.py`: Rotas locais, diz qual função do `views.py` deve ser executada.

`admin.py`: Onde vamos registrar as nossas tabelas para que elas apareçam no painel de administrador nativo do Django.

### Front-end **("T" do MVT e o Design)**

`templates/`: Onde vão ficar nossos arquivos `.html` (Interface visual do usuário).
- `base.html` - Esqueleto principal (header e background) todas as outras telas vão herdar para não repetirmos código.

`static/`: Guardamos coisas estáticas, como o `CSS(style.css)`, imagens e logos.
