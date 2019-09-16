import os, json
import binascii

from cgi import parse_header, parse_multipart
from urlparse import parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from Crypto import Random
from Crypto.Cipher import AES

# ------------------------------
# DEFINE Encryption Class
class Cryptor(object):
	'''
	Provide encryption and decryption function that works with crypto-js.
	https://code.google.com/p/crypto-js/

	Padding implemented as per RFC 2315: PKCS#7 page 21
	http://www.ietf.org/rfc/rfc2315.txt

	The key to make pycrypto work with crypto-js are:
	1. Use MODE_CFB.  For some reason, crypto-js decrypted result from MODE_CBC
	   gets truncated
	2. Use Pkcs7 padding as per RFC 2315, the default padding used by CryptoJS
	3. On the JS side, make sure to wrap ciphertext with CryptoJS.lib.CipherParams.create()
	'''

	# AES-256 key (32 bytes)
	KEY = "01ab38d5e05c92aa098921d9d4626107133c7e2ab0e4849558921ebcc242bcb0"
	BLOCK_SIZE = 16

	@classmethod
	def _pad_string(cls, in_string):
		'''Pad an input string according to PKCS#7'''
		in_len = len(in_string)
		pad_size = cls.BLOCK_SIZE - (in_len % cls.BLOCK_SIZE)
		return in_string.ljust(in_len + pad_size, chr(pad_size))

	@classmethod
	def _unpad_string(cls, in_string):
		'''Remove the PKCS#7 padding from a text string'''
		in_len = len(in_string)
		pad_size = ord(in_string[-1])
		if pad_size > cls.BLOCK_SIZE:
			raise ValueError('Input is not padded or padding is corrupt')
		return in_string[:in_len - pad_size]

	@classmethod
	def generate_iv(cls, size=16):
		return Random.get_random_bytes(size)

	@classmethod
	def encrypt(cls, in_string, in_key, in_iv=None):
		'''
		Return encrypted string.
		@in_string: Simple str to be encrypted
		@key: hexified key
		@iv: hexified iv
		'''
		key = binascii.a2b_hex(in_key)

		if in_iv is None:
			iv = cls.generate_iv()
			in_iv = binascii.b2a_hex(iv)
		else:
			iv = binascii.a2b_hex(in_iv)

		aes = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
		return in_iv, aes.encrypt(cls._pad_string(in_string))

	@classmethod
	def decrypt(cls, in_encrypted, in_key, in_iv):
		'''
		Return encrypted string.
		@in_encrypted: Base64 encoded
		@key: hexified key
		@iv: hexified iv
		'''
		key = binascii.a2b_hex(in_key)
		iv = binascii.a2b_hex(in_iv)
		aes = AES.new(key, AES.MODE_CFB, iv, segment_size=128)

		decrypted = aes.decrypt(binascii.a2b_base64(in_encrypted).rstrip())
		return cls._unpad_string(decrypted)


# ------------------------------
# DEFINE HTTP Handler
class EncryptHandler(BaseHTTPRequestHandler):
	'''
	Simple webserver that server index.html and static "*.html" and "*.js" files,
	which special "/encrypt" URL that would return a JSON with encrypted data
	'''

	PORT_NUMBER = 8087
	SCRIPT_PATH = os.path.dirname(__file__)

	def _return_http_code(self, http_code):
		self.send_response(http_code)
		self.end_headers()

	def _return_file(self, in_file):
		''' '''
		if os.path.exists(in_file):
			with open(in_file) as f:
				self.send_response(200)
				if in_file.endswith(".html"):
					self.send_header('Content-type',"text/html")
				elif in_file.endswith(".js"):
					self.send_header('Content-type',"text/javascript")
				else:
					self.send_header('Content-type',"text/plain")
				self.end_headers()
				self.wfile.write(f.read())
		else:
			self._return_http_code(404)

	def _return_json(self, in_dict):
		'''Send JSON back to client from a dictionary'''
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		self.wfile.write(json.dumps(in_dict))

	def do_GET(self):
		'''
		Serve static .html and .js files
		'''
		request_path = self.path
		if request_path == "/":
			self._return_file("index.html")
		elif request_path.endswith(".html") or request_path.endswith(".js"):
			self._return_file(self.SCRIPT_PATH + request_path)
		else:
			self._return_http_code(404)

		return

	def parse_POST(self):
		'''
		parse POST body
		'''
		ctype, pdict = parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			postvars = parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
			postvars = {}
		return postvars

	def do_POST(self):
		'''
		Perform the encryption in Python
		'''
		if self.path == "/encrypt":
			postvars = self.parse_POST()
			if postvars:
				to_encrypt = ''.join(postvars["to_encrypt"])
				iv, encrypted = Cryptor.encrypt(to_encrypt, Cryptor.KEY)
				result = {
					"key": Cryptor.KEY,
					"iv": iv,
					"ciphertext": binascii.b2a_base64(encrypted).rstrip()
				}
				#print "Encrypt result: %s" % result
				self._return_json(result)
			else:
				print "Error: POST received no data."
				self._return_http_code(500)
		else:
			self._return_http_code(404)

		return



# ------------------------------
# START WEB SERVER
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', EncryptHandler.PORT_NUMBER), EncryptHandler)
	print 'Started httpserver on port ' , EncryptHandler.PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
