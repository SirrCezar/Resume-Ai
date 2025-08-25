# Resume AI 🤖

### Criei isso pra parar de sofrer com edital.

Eu estava cansado de perder horas lendo documentos gigantes pra achar meia dúzia de informações importantes. Decidi que um robô podia fazer isso por mim. E foi assim que nasceu o Resume AI (um nome com toda certeza original).

A ideia é simples: você entrega um PDF pra ele, e ele te devolve um resumo em Word, já todo preenchido nos lugares certos. Chega de Ctrl+C, Ctrl+V.

<img width="818" height="709" alt="Captura de tela de 2025-08-24 21-33-06" src="https://github.com/user-attachments/assets/18089097-c93f-4cea-bc8a-7d06ed8bfa5f" />

## O que ele faz, na prática?

É um fluxo bem direto:

1.  **Você joga um PDF pra ele.**
2.  O script lê o texto todo do arquivo.
3.  Ele manda esse texto pra uma Inteligência Artificial e com base em um contexto do que você precisa (Um arquivo simples .txt que você pode criar e configurar)
4.  A IA responde tudo bonitinho, já separado e organizado.
5.  O script pega essa resposta e preenche um modelo de Word (`.docx`) que a gente deixou pronto.

No final, você tem seu arquivo `.docx` preenchido sem ter lido uma linha do edital.

## 🛠️ Tecnologias Utilizadas

Para fazer essa automação acontecer, eu usei as seguintes ferramentas e bibliotecas:

  * **🐍 Python 3.8+**: A linguagem que move todo o projeto.
  * **🎨 Tkinter**: Para construir a interface gráfica de forma simples e nativa do Python.
  * **📄 PyPDF (`pypdf`)**: A biblioteca responsável por abrir os arquivos PDF e extrair todo o texto de dentro deles.
  * **🤖 OpenAI Client (`openai`)**: Usei o cliente da OpenAI para me comunicar com a **API da DeepSeek**. Ele serve como uma ponte universal para conversar com a IA.
  * **📝 python-docx**: É a ferramenta que me permite criar e editar os arquivos `.docx`. É ela que pega os dados da IA e preenche o nosso template do Word.
  * **🔑 python-dotenv**: Para gerenciar a chave da API de forma segura, carregando-a a partir de um arquivo `.env` sem expor no código.

## 🚀 Como rodar aí na sua máquina

Sem segredo. É só seguir o passo a passo:

#### 1\. Clona o projeto

```bash
git clone https://github.com/seu-usuario/resume-ai.git
cd resume-ai
```

#### 2\. Cria um ambiente virtual (boa prática, né?)

```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No Mac/Linux
python -m venv venv
source venv/bin/activate
```

#### 3\. Instala o que precisa

Crie um arquivo chamado **`requirements.txt`** com o seguinte conteúdo:

```txt
python-docx
pypdf
openai
python-dotenv
```

Depois, rode o comando no terminal:

```bash
pip install -r requirements.txt
```

#### 4\. Configura tua chave da API

  * Na pasta do projeto, crie um arquivo chamado **`.env`**.
  * Dentro dele, escreva isso e cole a sua chave:
    ```
    DEEPSEEK_API_KEY="aqui_vai_sua_chave_secreta_da_deepseek"
    ```

#### 5\. Pronto\! Agora é só rodar

```bash
python app_ui.py
```

## 🎨 Deixando com a sua cara

A beleza do negócio é que você pode adaptar tudo pra sua necessidade. As duas peças principais pra mexer são:

#### 1\. O Cérebro da IA (`contexto.txt`)

Esse arquivo é a alma do robô. É nele que você "conversa" com a IA e define o que ela deve procurar. Quer que ela busque o "prazo de entrega"? É só adicionar essa instrução lá.

#### 2\. O Molde do Documento (`RESUMO_SMP.docx`)

Esse é o seu template do Word. Utilize um modelo que você já tem e apenas adicione placeholders como [Data de Entrega] ou [Orgão Responsável]

**A regra é simples:** o nome da "chave" que você pediu pra IA no `contexto.txt` tem que ser **exatamente** o mesmo nome que você usa dentro dos colchetes `[ ]` no Word. Se não for igual, ele não vai saber onde preencher.

-----

Isso aqui resolveu um problemão pra mim, e espero que resolva o seu também. Se achar algum bug ou tiver uma ideia pra melhorar, abre uma *issue* lá no GitHub. Tamo junto\!
