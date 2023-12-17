from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/app.py', methods=['POST'])
def submit_form():
    target = request.form['target']

    # Perform penetration testing logic here (replace this with your actual logic)

    # Redirect to the thank_you.html page with the target as a parameter
    return redirect(f'thank_you.html?target={target}')

if __name__ == '__main__':
    app.run(debug=True)
