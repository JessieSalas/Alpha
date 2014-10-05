import facebook as Facebook
api_key = '432563250143448'
secret  = 'f66ac09131f938a46a706a5575fedf38'


def generate_session_from_onetime_code(fb, code):
    fb.auth_token = code
    return fb.auth.getSession()

code = generate_session_from_onetime_code(Facebook,"http://www.facebook.com/code_gen.php?v=1.0&api_key=" + api_key)

print generate_session_from_onetime_code(fb, code)

session_key = 'your infinite Session key of user'

fb = Facebook(api_key, secret)
fb.session_key = session_key

