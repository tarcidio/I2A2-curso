#Library to GUI
import flet as ft
#Libraries to API connection
import os
import requests
import json


#Request funciton 1: create a header to request
def create_header():
  return {
      "Authorization": f"Bearer {API_KEY}",
      "Content-Type": "application/json"
  }

#Request funciton 2: create a body message to request
def create_body_message(id_modelo, historic):
  body_message = {"model": id_modelo, "messages": historic}
  return json.dumps(body_message)


class User():

  def __init__(self, name, isBot: bool):
    self.name = name
    if isBot:
      self.align = ft.alignment.center_left
    else:
      self.align = ft.alignment.center_right
    self.isBot = isBot


class Message():

  def __init__(self, user: User, text: str):
    self.user = user
    self.text = text


class ChatMessage(ft.ResponsiveRow):

  def __init__(self, message: Message):
    super().__init__()
    self.vertical_alignment = ft.CrossAxisAlignment.START
    avatar = ft.CircleAvatar(
          content=ft.Text(self.get_initials(message.user.name)),
          color=ft.colors.WHITE,
          bgcolor=self.get_avatar_color(message.user.name),
        )
    message_place = ft.Column(
        [
          ft.Text(message.user.name, weight=ft.FontWeight.BOLD),
          ft.Text(message.text, selectable=True),
        ],
        tight=True,
        spacing=5,
    )
    #self.controls = [avatar, message_place]
    self.controls = [message_place]
    #if not message.user.isBot:
    #  self.controls = [message_place, avatar]

  def get_initials(self, user_name: str):
    return user_name[:1].capitalize()

  def get_avatar_color(self, user_name: str):
    colors_lookup = [
        ft.colors.AMBER,
        ft.colors.BLUE,
        ft.colors.BROWN,
        ft.colors.CYAN,
        ft.colors.GREEN,
        ft.colors.INDIGO,
        ft.colors.LIME,
        ft.colors.ORANGE,
        ft.colors.PINK,
        ft.colors.PURPLE,
        ft.colors.RED,
        ft.colors.TEAL,
        ft.colors.YELLOW,
    ]
    return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
  #Request variables
  HEADERS = create_header()
  LINK = "https://api.openai.com/v1/chat/completions"
  ID_MODEL = "gpt-3.5-turbo"
  BOT_ON = True
  #GUI variables
  user = User('', False)
  user_bot = User('Eliza Bot', True)
  chat = ft.ListView(
      expand=True,
      spacing=10,
      auto_scroll=True,
  )

  chatBox = ft.Container(
      content = chat,
      border=ft.border.all(1, ft.colors.OUTLINE),
      border_radius=5,
      padding=10,
      expand=True
  )
  
  historic = [{
      "role":
      "system",
      "content":
      "Tente responder minhas perguntas como se você fosse o meu terapeuta virtual"
  }]

  def send_message_click(e):
    #Publish user message
    publish_message(ChatMessage(Message(user, new_message.value)))
    content_user = new_message.value
    #Reset text field
    new_message.value = ""
    #Update
    page.update()

    if BOT_ON:
      historic.append({"role": "user", "content": content_user})
      body_message = create_body_message(ID_MODEL, historic)
      #Request  API
      requisicao = requests.post(LINK, headers=HEADERS, data=body_message)
      resposta = requisicao.json()
      mensagem = resposta["choices"][0]["message"]["content"]
      historic.append({"role": "assistant", "content": mensagem})
    else:
      mensagem = "Estou desligada"

    #Publish API message
    publish_message(ChatMessage(Message(user_bot, mensagem)))
    #Update
    page.update()

  new_message = ft.TextField(
      hint_text="Escreva uma mensagem...",
      autofocus=True,
      shift_enter=True,
      min_lines=1,
      max_lines=5,
      filled=True,
      expand=True,
      on_submit=send_message_click,
  )

  def publish_message(chat_message: ChatMessage):
    chat.controls.append(chat_message)
    page.update()

  which_your_name = ft.TextField()

  def join_click(e):
    if not which_your_name.value:
      which_your_name.error_text = "Não é permitido nome branco"
      page.update()
    else:
      user.name = which_your_name.value
      #Clen Screen
      page.clean()
      #page.update()
      send = ft.IconButton(
          icon=ft.icons.SEND_ROUNDED,
          tooltip="Send message",
          on_click=send_message_click,
      )
      page.vertical_alignment = ft.MainAxisAlignment.END
      page.padding = 10
      page.add(chatBox, ft.Row([new_message, send]))

  which_your_name = ft.TextField(label="Qual seu nome?",
                                 shift_enter=True,
                                 on_submit=join_click)

  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.padding = 200
  page.add(
      ft.Container(content=ft.Text("Bem vindo(a)!",
                                   color=ft.colors.WHITE,
                                   size=20),
                   alignment=ft.alignment.center),
      ft.Container(content=which_your_name, ),
      ft.Container(content=ft.ElevatedButton(text="Entre no chat",
                                             on_click=join_click),
                   alignment=ft.alignment.center))


ft.app(main)

#Quero saber como treinar meu chat para responder de maneira mais perosnalizada
#Fazer a interface
#Perguntar o nome do usuário antes dele usar o chat
#Criar elementos antes e um add antes e colher a informação
#Colocar texto do usuário do lado direito

#Colocar imagens

#Melhorar o text field: ficar maior e colocar o nome do usuario no campo
#Colocar botao do sendo do lado direito
#Deixar o plano de fundo de outra cor

#talvez mudar a fonte do bem vindo mais nao consegui



#Avatar
#Alterar caracteristicas do bot
#Subir na nuvem
#Colocar nome do lado do texto
