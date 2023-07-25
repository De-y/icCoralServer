import icapi, prisma, os, dotenv
from flask import Flask, render_template, request, jsonify
from prisma.models import User

db = prisma.Prisma()
db.connect()
prisma.register(db)

dotenv.load_dotenv()

app = Flask(__name__, template_folder='./pages/', static_folder='./assets/')
PRIV_KEY = os.getenv('PRIVATE_KEY')

@app.route('/', methods=['GET'])
def main():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/api/get_name', methods=['POST'])
def get_name():
    """
        Logs into Infinite Campus through the icapi and then creates your user account, if any unique detail existed, then it'll return a 400 status code.
    """
    student = icapi.User(request.form['username'], request.form['password'], "https://nspcsa.infinitecampus.org/campus/portal/students/coral.jsp")
    name = student.getInformation()['firstName'] + ' ' + student.getInformation()['lastName']

    try:
        User.prisma().create(data={'ic_verified': True, 'username': str(request.form['discord_username']), 'name': name})
    except:
        return 400
    
    return 200

@app.route('/api/getinfo', methods=['POST'])
def get_info():
    data = request.json
    username = data['username']
    privkey = data['authorization']
    if privkey == PRIV_KEY:
        user = User.prisma().find_first(where={'username': username})
        if user is not None and user.ic_verified == True:
            print('I am here')
            return True
        return "405"
    return "405"

if __name__ == "__main__":
    app.run(debug=True, port=3000)