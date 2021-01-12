# MedTravel

AILab

Important links for the project ⬇️

- [Docs](https://instecchihuahua-my.sharepoint.com/personal/l16550545_chihuahua2_tecnm_mx/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fl16550545%5Fchihuahua2%5Ftecnm%5Fmx%2FDocuments%2FMedTravel&originalPath=aHR0cHM6Ly9pbnN0ZWNjaGlodWFodWEtbXkuc2hhcmVwb2ludC5jb20vOmY6L2cvcGVyc29uYWwvbDE2NTUwNTQ1X2NoaWh1YWh1YTJfdGVjbm1fbXgvRXZLTnlQUGxHZnRLaEhnVmVEdE9Fd1FCb3NkcTRIS3QtZHlJSUtpYXR4MTIwdz9ydGltZT1oYUU3QW5PeTJFZw)

- [Requirements](https://docs.google.com/document/d/1JblDgISOdw1_QR6QKgmp1FKlSLg8fkYq0PVs30nJd54/edit)

- [Sendgrid](https://app.sendgrid.com/)
# TODO:

- Simple frontend design
- Rewrite web app architecture
- Review the main AR OpenCV module
- deploy

# How to?

To run the project: 

```bash
git clone repo
```

```bash
cd repo
```
Create a new venv
```bash
python -m venv venv
```
Activate venv
```bash
venv\Scripts\activate
```
Install the dependencies
```
pip install -r requirements.txt
```
Create 'FLASK_APP' env
```bash
$env:FLASK_APP="\src\medtravel.py"
$env:FLASK_DEBUG=1
```
Open your browser on localhost:5000

to use email functionality...
* [Create a sendgrid account](https://sendgrid.com/)
* Get your API Key.
* Create a new sender with an email address
* Configure env variables
```bash
$env:SENDGRID_API_KEY='your api key'
$env:FROM_EMAIL='sender email'
$env:TO_EMAIL='email address that will receive the emails'
$env:FLASKY_ADMIN=1 
```

Enjoy!

# about...

Developed with ❤️ by TnT
