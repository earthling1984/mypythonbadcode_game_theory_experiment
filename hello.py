from flask import Flask
from callers import commonvalidator
import html
app = Flask(__name__)
 
@app.route('/hello/<path:name>')
def hello_name(firstname):
    name=commonvalidator.using_path(firstname)
    #firstnamegood=html.escape(firstname)
    return 'Hello %s!' % fname

def main():
    print(hello_name('A'))

if __name__ == "__main__":
    main()


if __name__ == '__main__':
   app.run()