from flask import Flask
from callers import commonvalidator as cv
import html
app = Flask(__name__)
 
@app.route('/hello/<path:name>')
def hello_name(firstname):
    #name=up.using_path(firstname)
    firstnamegood=html.escape(firstname)
    return 'Hello %s!' % firstname

def main():
    print(hello_name('A'))

if __name__ == "__main__":
    main()


if __name__ == '__main__':
   app.run()