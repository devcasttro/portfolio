from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = 'qwer@1234'

mail_settings = {
    "MAIL_SERVER": 'smtp.zoho.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA")
}

app.config.update(mail_settings)

mail = Mail(app)


class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )

        msg = Message(
            subject = f'Contato do Portfólio feito por {formContato.nome}',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = ['lucas.castro@inovacaocastro.com.br', 'castrolucas131@gmail.com', app.config.get("MAIL_USERNAME")],
            body = f''' 
            
            {formContato.nome} com o e-mail {formContato.email}, te enviou a seguinte mensagem:

            {formContato.mensagem}

            '''
        )

        mail.send(msg) # Realiza o envio do e-mail

        flash('Mensagem enviada com sucesso!')

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)