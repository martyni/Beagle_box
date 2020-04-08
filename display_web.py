from bottle import route, run, template, request, default_app
import HTMLParser
from display_code import DISP_COLS, DISP_ROWS, CHAT_FILE

HTML_PARSER = HTMLParser.HTMLParser()
DISPLAY_SIZE = DISP_COLS * DISP_ROWS + 1
MAIN_URL = "/display"

def read_message():
    with open(CHAT_FILE) as chat_file:
        message = chat_file.read()
        message = message.replace('\n','<br>')
        print(message)
    return message

def get_app(message):
    return '''
    <head>
      <title>Bootstrap Example</title>
        <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
              <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
                </head>
       <!-- Latest compiled and minified CSS -->
       <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
       
       <!-- Optional theme -->
       <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
       
       <!-- Latest compiled and minified JavaScript -->
       <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

        <div class="container">
        <div class="w-100">{message}
        <form action="{main_url}" method="post">
            <div class="form-group"><div class="row">

            <label for="text">Text</label>
            <input name="text" type="text" class="form-control" id="text" maxlength="{display_size}" placeholder="{placeholder}"/>
            <button value="Update" type="submit" class="btn btn-promary" >Update</button>
            </div>
            </div>
        </form>
        </div>
        </div>
    '''.format(
            display_size=DISPLAY_SIZE - 1,
            main_url=MAIN_URL,
            message=message,
            placeholder=read_message().replace('<br>','')
            )

def write_message(message):
    with open(CHAT_FILE,"w") as chat_file:
        chat_file.write(message)
    return message


def spill_over(message, half):

    return message[:half] + "\n</br>\n" + message[half:-1]



@route('/hello/<name>')
def hello(name):
    message = "Hello {}".format(name)
    return write_message(message) + get_app()

@route(MAIN_URL)
def login():
    return get_app(read_message())


@route(MAIN_URL, method='POST')
def do_login():
    text = request.forms.get('text')
    print(text)
    half = DISPLAY_SIZE / 2
    if len(text) > half:
        text = '\n'.join(
                [
            text[0:half], 
            text[half:DISPLAY_SIZE]
                ]
            )
    print(text)
    write_message(text)
    return get_app(read_message())


application = default_app()
from paste import httpserver
httpserver.serve(application, host='0.0.0.0', port=8080)
